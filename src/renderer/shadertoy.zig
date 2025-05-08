const std = @import("std");
const builtin = @import("builtin");
const assert = std.debug.assert;
const Allocator = std.mem.Allocator;
const ArenaAllocator = std.heap.ArenaAllocator;
const glslang = @import("glslang");
const spvcross = @import("spirv_cross");
const configpkg = @import("../config.zig");

const log = std.log.scoped(.shadertoy);

/// The target to load shaders for.
pub const Target = enum { glsl, msl };

/// Load a set of shaders from files and convert them to the target
/// format. The shader order is preserved.
pub fn loadFromFiles(
    alloc_gpa: Allocator,
    paths: configpkg.RepeatablePath,
    target: Target,
) ![]const [:0]const u8 {
    var list = std.ArrayList([:0]const u8).init(alloc_gpa);
    defer list.deinit();
    errdefer for (list.items) |shader| alloc_gpa.free(shader);

    for (paths.value.items) |item| {
        const path, const optional = switch (item) {
            .optional => |path| .{ path, true },
            .required => |path| .{ path, false },
        };

        const shader = loadFromFile(alloc_gpa, path, target) catch |err| {
            if (err == error.FileNotFound and optional) {
                continue;
            }

            return err;
        };
        log.info("loaded custom shader path={s}", .{path});
        try list.append(shader);
    }

    return try list.toOwnedSlice();
}

/// Load a single shader from a file and convert it to the target language
/// ready to be used with renderers.
pub fn loadFromFile(
    alloc_gpa: Allocator,
    path: []const u8,
    target: Target,
) ![:0]const u8 {
    var arena = ArenaAllocator.init(alloc_gpa);
    defer arena.deinit();
    const alloc = arena.allocator();

    // Load the shader file
    const cwd = std.fs.cwd();
    const file = try cwd.openFile(path, .{});
    defer file.close();

    // Read it all into memory -- we don't expect shaders to be large.
    var buf_reader = std.io.bufferedReader(file.reader());
    const src = try buf_reader.reader().readAllAlloc(
        alloc,
        4 * 1024 * 1024, // 4MB
    );

    // Convert to full GLSL
    const glsl: [:0]const u8 = glsl: {
        var list = std.ArrayList(u8).init(alloc);
        try glslFromShader(list.writer(), src);
        try list.append(0);
        break :glsl list.items[0 .. list.items.len - 1 :0];
    };

    // Convert to SPIR-V
    const spirv: []const u8 = spirv: {
        // SpirV pointer must be aligned to 4 bytes since we expect
        // a slice of words.
        var list = std.ArrayListAligned(u8, @alignOf(u32)).init(alloc);
        var errlog: SpirvLog = .{ .alloc = alloc };
        defer errlog.deinit();
        spirvFromGlsl(list.writer(), &errlog, glsl) catch |err| {
            if (errlog.info.len > 0 or errlog.debug.len > 0) {
                log.warn("spirv error path={s} info={s} debug={s}", .{
                    path,
                    errlog.info,
                    errlog.debug,
                });
            }

            return err;
        };
        break :spirv list.items;
    };

    // Convert to MSL
    return switch (target) {
        // Important: using the alloc_gpa here on purpose because this
        // is the final result that will be returned to the caller.
        .glsl => try glslFromSpv(alloc_gpa, spirv),
        .msl => try mslFromSpv(alloc_gpa, spirv),
    };
}

/// Convert a ShaderToy shader into valid GLSL.
///
/// ShaderToy shaders aren't full shaders, they're just implementing a
/// mainImage function and don't define any of the uniforms. This function
/// will convert the ShaderToy shader into a valid GLSL shader that can be
/// compiled and linked.
pub fn glslFromShader(writer: anytype, src: []const u8) !void {
    const prefix = @embedFile("shaders/shadertoy_prefix.glsl");
    try writer.writeAll(prefix);
    try writer.writeAll("\n\n");
    try writer.writeAll(src);
}

/// Convert a GLSL shader into SPIR-V assembly.
pub fn spirvFromGlsl(
    writer: anytype,
    errlog: ?*SpirvLog,
    src: [:0]const u8,
) !void {
    // So we can run unit tests without fear.
    if (builtin.is_test) try glslang.testing.ensureInit();

    const c = glslang.c;
    const input: c.glslang_input_t = .{
        .language = c.GLSLANG_SOURCE_GLSL,
        .stage = c.GLSLANG_STAGE_FRAGMENT,
        .client = c.GLSLANG_CLIENT_VULKAN,
        .client_version = c.GLSLANG_TARGET_VULKAN_1_2,
        .target_language = c.GLSLANG_TARGET_SPV,
        .target_language_version = c.GLSLANG_TARGET_SPV_1_5,
        .code = src.ptr,
        .default_version = 100,
        .default_profile = c.GLSLANG_NO_PROFILE,
        .force_default_version_and_profile = 0,
        .forward_compatible = 0,
        .messages = c.GLSLANG_MSG_DEFAULT_BIT,
        .resource = c.glslang_default_resource(),
    };

    const shader = try glslang.Shader.create(&input);
    defer shader.delete();

    shader.preprocess(&input) catch |err| {
        if (errlog) |ptr| ptr.fromShader(shader) catch {};
        return err;
    };
    shader.parse(&input) catch |err| {
        if (errlog) |ptr| ptr.fromShader(shader) catch {};
        return err;
    };

    const program = try glslang.Program.create();
    defer program.delete();
    program.addShader(shader);
    program.link(
        c.GLSLANG_MSG_SPV_RULES_BIT |
            c.GLSLANG_MSG_VULKAN_RULES_BIT,
    ) catch |err| {
        if (errlog) |ptr| ptr.fromProgram(program) catch {};
        return err;
    };
    program.spirvGenerate(c.GLSLANG_STAGE_FRAGMENT);
    const size = program.spirvGetSize();
    const ptr = try program.spirvGetPtr();
    const ptr_u8: [*]u8 = @ptrCast(ptr);
    const slice_u8: []u8 = ptr_u8[0 .. size * 4];
    try writer.writeAll(slice_u8);
}

/// Retrieve errors from spirv compilation.
pub const SpirvLog = struct {
    alloc: Allocator,
    info: [:0]const u8 = "",
    debug: [:0]const u8 = "",

    pub fn deinit(self: *const SpirvLog) void {
        if (self.info.len > 0) self.alloc.free(self.info);
        if (self.debug.len > 0) self.alloc.free(self.debug);
    }

    fn fromShader(self: *SpirvLog, shader: *glslang.Shader) !void {
        const info = try shader.getInfoLog();
        const debug = try shader.getDebugInfoLog();
        self.info = "";
        self.debug = "";
        if (info.len > 0) self.info = try self.alloc.dupeZ(u8, info);
        if (debug.len > 0) self.debug = try self.alloc.dupeZ(u8, debug);
    }

    fn fromProgram(self: *SpirvLog, program: *glslang.Program) !void {
        const info = try program.getInfoLog();
        const debug = try program.getDebugInfoLog();
        self.info = "";
        self.debug = "";
        if (info.len > 0) self.info = try self.alloc.dupeZ(u8, info);
        if (debug.len > 0) self.debug = try self.alloc.dupeZ(u8, debug);
    }
};

/// Convert SPIR-V binary to MSL.
pub fn mslFromSpv(alloc: Allocator, spv: []const u8) ![:0]const u8 {
    return try spvCross(alloc, spvcross.c.SPVC_BACKEND_MSL, spv, null);
}

/// Convert SPIR-V binary to GLSL..
pub fn glslFromSpv(alloc: Allocator, spv: []const u8) ![:0]const u8 {
    // Our minimum version for shadertoy shaders is OpenGL 4.2 because
    // Spirv-Cross generates binding locations for uniforms which is
    // only supported in OpenGL 4.2 and above.
    //
    // If we can figure out a way to NOT do this then we can lower this
    // version.
    const GLSL_VERSION = 420;

    const c = spvcross.c;
    return try spvCross(alloc, c.SPVC_BACKEND_GLSL, spv, (struct {
        fn setOptions(options: c.spvc_compiler_options) error{SpvcFailed}!void {
            if (c.spvc_compiler_options_set_uint(
                options,
                c.SPVC_COMPILER_OPTION_GLSL_VERSION,
                GLSL_VERSION,
            ) != c.SPVC_SUCCESS) {
                return error.SpvcFailed;
            }
        }
    }).setOptions);
}

fn spvCross(
    alloc: Allocator,
    backend: spvcross.c.spvc_backend,
    spv: []const u8,
    comptime optionsFn_: ?*const fn (c: spvcross.c.spvc_compiler_options) error{SpvcFailed}!void,
) ![:0]const u8 {
    // Spir-V is always a multiple of 4 because it is written as a series of words
    if (@mod(spv.len, 4) != 0) return error.SpirvInvalid;

    // Compiler context
    const c = spvcross.c;
    var ctx: c.spvc_context = undefined;
    if (c.spvc_context_create(&ctx) != c.SPVC_SUCCESS) return error.SpvcFailed;
    defer c.spvc_context_destroy(ctx);

    // It would be better to get this out into an output parameter to
    // show users but for now we can just log it.
    c.spvc_context_set_error_callback(ctx, @ptrCast(&(struct {
        fn callback(_: ?*anyopaque, msg_ptr: [*c]const u8) callconv(.c) void {
            const msg = std.mem.sliceTo(msg_ptr, 0);
            std.log.warn("spirv-cross error message={s}", .{msg});
        }
    }).callback), null);

    // Parse the Spir-V binary to an IR
    var ir: c.spvc_parsed_ir = undefined;
    if (c.spvc_context_parse_spirv(
        ctx,
        @ptrCast(@alignCast(spv.ptr)),
        spv.len / 4,
        &ir,
    ) != c.SPVC_SUCCESS) {
        return error.SpvcFailed;
    }

    // Build our compiler to GLSL
    var compiler: c.spvc_compiler = undefined;
    if (c.spvc_context_create_compiler(
        ctx,
        backend,
        ir,
        c.SPVC_CAPTURE_MODE_TAKE_OWNERSHIP,
        &compiler,
    ) != c.SPVC_SUCCESS) {
        return error.SpvcFailed;
    }

    // Setup our options if we have any
    if (optionsFn_) |optionsFn| {
        var options: c.spvc_compiler_options = undefined;
        if (c.spvc_compiler_create_compiler_options(compiler, &options) != c.SPVC_SUCCESS) {
            return error.SpvcFailed;
        }

        try optionsFn(options);

        if (c.spvc_compiler_install_compiler_options(compiler, options) != c.SPVC_SUCCESS) {
            return error.SpvcFailed;
        }
    }

    // Compile the resulting string. This string pointer is owned by the
    // context so we don't need to free it.
    var result: [*:0]const u8 = undefined;
    if (c.spvc_compiler_compile(compiler, @ptrCast(&result)) != c.SPVC_SUCCESS) {
        return error.SpvcFailed;
    }

    return try alloc.dupeZ(u8, std.mem.sliceTo(result, 0));
}

/// Convert ShaderToy shader to null-terminated glsl for testing.
fn testGlslZ(alloc: Allocator, src: []const u8) ![:0]const u8 {
    var list = std.ArrayList(u8).init(alloc);
    defer list.deinit();
    try glslFromShader(list.writer(), src);
    return try list.toOwnedSliceSentinel(0);
}

test "spirv" {
    const testing = std.testing;
    const alloc = testing.allocator;

    const src = try testGlslZ(alloc, test_crt);
    defer alloc.free(src);

    var buf: [4096 * 4]u8 = undefined;
    var buf_stream = std.io.fixedBufferStream(&buf);
    const writer = buf_stream.writer();
    try spirvFromGlsl(writer, null, src);
}

test "spirv invalid" {
    const testing = std.testing;
    const alloc = testing.allocator;

    const src = try testGlslZ(alloc, test_invalid);
    defer alloc.free(src);

    var buf: [4096 * 4]u8 = undefined;
    var buf_stream = std.io.fixedBufferStream(&buf);
    const writer = buf_stream.writer();

    var errlog: SpirvLog = .{ .alloc = alloc };
    defer errlog.deinit();
    try testing.expectError(error.GlslangFailed, spirvFromGlsl(writer, &errlog, src));
    try testing.expect(errlog.info.len > 0);
}

test "shadertoy to msl" {
    const testing = std.testing;
    const alloc = testing.allocator;

    const src = try testGlslZ(alloc, test_crt);
    defer alloc.free(src);

    var spvlist = std.ArrayListAligned(u8, @alignOf(u32)).init(alloc);
    defer spvlist.deinit();
    try spirvFromGlsl(spvlist.writer(), null, src);

    const msl = try mslFromSpv(alloc, spvlist.items);
    defer alloc.free(msl);
}

test "shadertoy to glsl" {
    const testing = std.testing;
    const alloc = testing.allocator;

    const src = try testGlslZ(alloc, test_crt);
    defer alloc.free(src);

    var spvlist = std.ArrayListAligned(u8, @alignOf(u32)).init(alloc);
    defer spvlist.deinit();
    try spirvFromGlsl(spvlist.writer(), null, src);

    const glsl = try glslFromSpv(alloc, spvlist.items);
    defer alloc.free(glsl);

    // log.warn("glsl={s}", .{glsl});
}

const test_crt = @embedFile("shaders/test_shadertoy_crt.glsl");
const test_invalid = @embedFile("shaders/test_shadertoy_invalid.glsl");
