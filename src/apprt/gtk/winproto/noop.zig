const std = @import("std");
const Allocator = std.mem.Allocator;
const c = @import("../c.zig").c;
const Config = @import("../../../config.zig").Config;
const input = @import("../../../input.zig");

const log = std.log.scoped(.winproto_noop);

pub const App = struct {
    pub fn init(
        _: Allocator,
        _: *c.GdkDisplay,
        _: [:0]const u8,
        _: *const Config,
    ) !?App {
        return null;
    }

    pub fn deinit(self: *App, alloc: Allocator) void {
        _ = self;
        _ = alloc;
    }

    pub fn eventMods(
        _: *App,
        _: ?*c.GdkDevice,
        _: c.GdkModifierType,
    ) ?input.Mods {
        return null;
    }
};

pub const Window = struct {
    pub fn init(
        _: Allocator,
        _: *App,
        _: *c.GtkWindow,
        _: *const Config,
    ) !Window {
        return .{};
    }

    pub fn deinit(self: Window, alloc: Allocator) void {
        _ = self;
        _ = alloc;
    }

    pub fn updateConfigEvent(
        _: *Window,
        _: *const Config,
    ) !void {}

    pub fn resizeEvent(_: *Window) !void {}

    pub fn syncAppearance(_: *Window) !void {}

    /// This returns true if CSD is enabled for this window. This
    /// should be the actual present state of the window, not the
    /// desired state.
    pub fn clientSideDecorationEnabled(self: Window) bool {
        _ = self;
        return true;
    }
};
