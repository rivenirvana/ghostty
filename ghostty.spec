# ghostty ships some submodules that wrap around existing libraries to provide a nicer experience within zig
# those submodules rely on headers provided by vendored versions of their respective library
# they will never be compiled or included in the final binary with the exception of glslang,and spirv-cross
#
# Zig only dependencies are vendored all other dependencies will be resolved from the system
# in future releases.

# unbundled https://github.com/ghostty-org/ghostty/pull/4520
%global fontconfig_version 2.14.2
# unbundled https://github.com/ghostty-org/ghostty/pull/4205
%global harfbuzz_version 8.4.0
%global utfcpp_version 4.0.5
%global iterm2_color_commit 4762ad5bd6d3906e28babdc2bda8a967d63a63be
%global z2d_commit 4638bb02a9dc41cc2fb811f092811f6a951c752a
%global spirv_cross_commit 476f384eb7d9e48613c45179e502a15ab95b6b49
%global libvaxis_commit1 6d729a2dc3b934818dffe06d2ba3ce02841ed74b
%global libvaxis_commit2 dc0a228a5544988d4a920cfb40be9cd28db41423
%global sentry_version 0.7.8
%global glslang_version 14.2.0
# unbundled https://github.com/ghostty-org/ghostty/pull/4543
%global freetype_version 2.13.2
%global freetype_dash_version %{lua x = string.gsub(macros['freetype_version'], "%.", "-"); print(x)}
# unbundled https://github.com/ghostty-org/ghostty/pull/4534
%global oniguruma_version 6.9.9
%global highway_version 1.1.0
%global libxev_commit db6a52bafadf00360e675fefa7926e8e6c0e9931
%global imgui_commit e391fe2e66eb1c96b1624ae8444dc64c23146ef4
%global breakpad_commit b99f444ba5f6b98cac261cbb391d8766b34a5918
%global wuffs_version 0.4.0-alpha.9
%global pixels_commit d843c2714d32e15b48b8d7eeb480295af537f877
%global ziglyph_commit b89d43d1e3fb01b6074bc1f7fc980324b04d26a5
%global zf_commit ed99ca18b02dda052e20ba467e90b623c04690dd
%global zigimg_commit 3a667bdb3d7f0955a5a51c8468eac83210c1439e
%global zg_version 0.13.2
%global zig_wayland_commit 0823d9116b80d65ecfad48a2efbca166c7b03497
%global wayland_commit 9cb3d7aa9dc995ffafdbdef7ab86a949d0fb0e7d
%global wayland_protocols_commit 258d8f88f2c8c25a830c6316f87d23ce1a0f12d9
%global plasma_wayland_protocols_commit db525e8f9da548cffa2ac77618dd0fbe7f511b86
# These aren't needed for compiling on linux however these are not marked as lazy
# thus required to be valid zig packages
%global zig_objc_commit 9b8ba849b0f58fe207ecd6ab7c147af55b17556e
%global zig_js_commit d0b8b0a57c52fbc89f9d9fecba75ca29da7dd7d1

# needed to get rid of a header informing the user the application is compiled in debug mode
%global _zig_release_mode fast
%global library             libghostty
%global project_id          com.mitchellh.ghostty
%global project_description %{expand:
Ghostty is a terminal emulator that differentiates itself by being
fast, feature-rich, and native. While there are many excellent
terminal emulators available, they all force you to choose between
speed, features, or native UIs. Ghostty provides all three.
}

%global build_options %{shrink: \
    --summary all \
    -Doptimize=ReleaseFast \
    -fno-sys=glslang \
    -fsys=simdutf \
    -Dflatpak=false \
    -Dfont-backend=fontconfig_freetype \
    -Drenderer=opengl \
    -Dgtk-adwaita=true \
    -Dgtk-x11=true \
    -Dgtk-wayland=true \
    -Dpie=true \
    -Demit-docs=true \
    -Dversion-string={{{git_custom_internal_version}}} \
    -Dstrip=false \
}

%global gtk_options %{shrink: \
    %{build_options} \
    -Dapp-runtime=gtk \
}

%global lib_options %{shrink: \
    %{build_options} \
    -Dapp-runtime=none \
}

# libghostty is considered unstable so don't ship it yet
# BUG: zig fails to assign a build-id to shared objects
# https://github.com/ziglang/zig/pull/22357
%bcond lib 0

Name:           ghostty
Version:        {{{git_custom_package_version}}}
Release:        {{{git_custom_release}}}%{?dist}
Summary:        Fast, native, feature-rich terminal emulator pushing modern features

# ghostty:                  MIT
# libvaxis:                 MIT
# libxev:                   MIT
# zig-objc:                 MIT
# zig-js:                   MIT
# z2d:                      MPL-2.0
# zf:                       MIT
# zigimg:                   MIT
# ziglyph:                  MIT
# zg:                       MIT
# zig-wayland               MIT
# wayland                   MIT
# wayland-protocols         MIT
# plasma-wayland-protocols  LGPL-2.1-only
# iTerm2-Color-Schemes:     MIT
# pkg/fontconfig:           HPND AND LicenseRef-Fedora-Public-Domain AND Unicode-DFS-2016
# pkg/harfbuzz:             MIT-Modern-Variant
# pkg/utfcpp:               BSL-1.0
# pkg/spirv-cross:          Apache-2.0
# pkg/sentry:               MIT
# pkg/glslang:              BSD-2-Clause AND BSD-3-Clause AND GPL-3.0-or-later AND Apache-2.0
# pkg/freetype:             (FTL OR GPL-2.0-or-later) AND BSD-3-Clause AND MIT AND MIT-Modern-Variant AND LicenseRef-Fedora-Public-Domain AND Zlib)
# pkg/oniguruma:            BSD-2-Clause
# pkg/highway:              Apache-2.0
# pkg/cimgui:               MIT
# pkg/breakpad:             MIT AND BSD-2-Clause AND BSD-3-Clause AND BSD-4-Clause AND Apache-2.0 AND MIT AND curl AND APSL-2.0 AND ClArtistic AND Unicode-3.0 AND LicenseRef-Fedora-Public-Domain AND (GPL-2.0-or-later WITH Autoconf-exception-generic)
# pkg/wuffs:                Apache-2.0 AND MIT
# pkg/wuffs/pixels:         CC0-1.0
# vendor/glad               (WTFPL OR CC0-1.0) AND Apache-2.0
License:        MIT AND MIT-Modern-Variant AND Zlib AND curl AND MPL-2.0 AND HPND AND LicenseRef-Fedora-Public-Domain AND Unicode-DFS-2016 AND Unicode-3.0 AND BSL-1.0 AND Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND BSD-4-Clause AND (FTL OR GPL-2.0-or-later) AND APSL-2.0 AND ClArtistic AND GPL-3.0-or-later AND (GPL-2.0-or-later WITH Autoconf-exception-generic) AND OFL-1.1 AND (WTFPL OR CC0-1.0) AND LGPL-2.1-only AND CC0-1.0

URL:            https://ghostty.org/
Source0:        {{{git_repo_archive}}}

Source10:       https://deps.files.ghostty.org/fontconfig-%{fontconfig_version}.tar.gz
# unbundling in process https://github.com/ghostty-org/ghostty/pull/4205
Source11:       https://github.com/harfbuzz/harfbuzz/archive/refs/tags/%{harfbuzz_version}/harfbuzz-%{harfbuzz_version}.tar.gz
Source12:       https://github.com/nemtrif/utfcpp/archive/refs/tags/v%{utfcpp_version}/utfcpp-%{utfcpp_version}.tar.gz
Source13:       https://github.com/mbadolato/iTerm2-Color-Schemes/archive/%{iterm2_color_commit}/iTerm2-Color-Schemes-%{iterm2_color_commit}.tar.gz
Source14:       https://github.com/vancluever/z2d/archive/%{z2d_commit}/z2d-%{z2d_commit}.tar.gz
Source15:       https://github.com/KhronosGroup/SPIRV-Cross/archive/%{spirv_cross_commit}/SPIRV-Cross-%{spirv_cross_commit}.tar.gz
# zf requires a different version of libvaxis than ghostty
Source16:       https://github.com/rockorager/libvaxis/archive/%{libvaxis_commit1}/libvaxis-%{libvaxis_commit1}.tar.gz
Source17:       https://github.com/rockorager/libvaxis/archive/%{libvaxis_commit2}/libvaxis-%{libvaxis_commit2}.tar.gz
# sentry is only used for catching errors and not for uploading
# PR to disable it https://github.com/ghostty-org/ghostty/pull/3934
Source18:       https://github.com/getsentry/sentry-native/archive/refs/tags/%{sentry_version}/sentry-native-%{sentry_version}.tar.gz
Source19:       https://github.com/KhronosGroup/glslang/archive/refs/tags/%{glslang_version}/glslang-%{glslang_version}.tar.gz
Source20:       https://github.com/freetype/freetype/archive/refs/tags/VER-%{freetype_dash_version}.tar.gz#/freetype2-%{freetype_dash_version}.tar.gz
Source21:       https://github.com/kkos/oniguruma/archive/refs/tags/v%{oniguruma_version}/oniguruma-%{oniguruma_version}.tar.gz
Source22:       https://github.com/google/highway/archive/refs/tags/%{highway_version}/highway-%{highway_version}.tar.gz
Source23:       https://github.com/mitchellh/libxev/archive/%{libxev_commit}/libxev-%{libxev_commit}.tar.gz
Source24:       https://github.com/ocornut/imgui/archive/%{imgui_commit}/imgui-%{imgui_commit}.tar.gz
Source25:       https://github.com/getsentry/breakpad/archive/%{breakpad_commit}/sentry-breakpad-%{breakpad_commit}.tar.gz
Source26:       https://github.com/google/wuffs/archive/refs/tags/v%{wuffs_version}/wuffs-%{wuffs_version}.tar.gz
Source27:       https://github.com/make-github-pseudonymous-again/pixels/archive/%{pixels_commit}/pixels-%{pixels_commit}.tar.gz
Source28:       https://deps.files.ghostty.org/ziglyph-%{ziglyph_commit}.tar.gz
Source29:       https://github.com/natecraddock/zf/archive/%{zf_commit}/zf-%{zf_commit}.tar.gz
Source30:       https://github.com/zigimg/zigimg/archive/%{zigimg_commit}/zigimg-%{zigimg_commit}.tar.gz
Source31:       https://codeberg.org/atman/zg/archive/v%{zg_version}.tar.gz#/zg-v%{zg_version}.tar.gz
Source32:       https://codeberg.org/ifreund/zig-wayland/archive/%{zig_wayland_commit}.tar.gz#/zig-wayland-%{zig_wayland_commit}.tar.gz
Source33:       https://deps.files.ghostty.org/wayland-%{wayland_commit}.tar.gz
Source34:       https://deps.files.ghostty.org/wayland-protocols-%{wayland_protocols_commit}.tar.gz
Source35:       https://invent.kde.org/libraries/plasma-wayland-protocols/-/archive/%{plasma_wayland_protocols_commit}/plasma-wayland-protocols-%{plasma_wayland_protocols_commit}.tar.gz
Source36:       https://github.com/mitchellh/zig-objc/archive/%{zig_objc_commit}/zig-objc-%{zig_objc_commit}.tar.gz
Source37:       https://github.com/mitchellh/zig-js/archive/%{zig_js_commit}/zig-js-%{zig_js_commit}.tar.gz

%global source_setup %{lua: \
    for i = 10, 37 do \
        print(" -a " .. i) \
    end \
}

Provides:       bundled(fontconfig) = %{fontconfig_version}
Provides:       bundled(harfbuzz) = %{harfbuzz_version}
Provides:       bundled(utfcpp) = %{utfcpp_version}
Provides:       bundled(z2d) = %{z2d_commit}
Provides:       bundled(SPIRV-Cross) = %{spirv_cross_commit}
Provides:       bundled(libvaxis) = %{libvaxis_commit1}
Provides:       bundled(libvaxis) = %{libvaxis_commit2}
Provides:       bundled(sentry-native) = %{sentry_version}
Provides:       bundled(glslang) = %{glslang_version}
Provides:       bundled(freetype2) = %{freetype_version}
Provides:       bundled(oniguruma) = %{oniguruma_version}
Provides:       bundled(highway) = %{highway_version}
Provides:       bundled(libxev) = %{libxev_commit}
Provides:       bundled(imgui) = %{imgui_commit}
Provides:       bundled(breakpad) = %{breakpad_commit}
Provides:       bundled(wuffs) = %{wuffs_version}
Provides:       bundled(pixels) = %{pixels_commit}
Provides:       bundled(ziglyph) = %{ziglyph_commit}
Provides:       bundled(zf) = %{zf_commit}
Provides:       bundled(zigimg) = %{zigimg_commit}
Provides:       bundled(zg) = %{zg_version}
Provides:       bundled(zig-wayland) = %{zig_wayland_commit}
Provides:       bundled(wayland-devel) = %{wayland_commit}
Provides:       bundled(wayland-protocols-devel) = %{wayland_protocols_commit}
Provides:       bundled(plasma-wayland-protocols) = %{plasma_wayland_protocols_commit}
Provides:       bundled(zig-objc) = %{zig_objc_commit}
Provides:       bundled(zig-js) = %{zig_js_commit}
# only the generated output is vendored
Provides:       bundled(glad2) = 2.0.0

# the fonts are included with ghostty and are embedded directly into the executable
# https://github.com/ghostty-org/ghostty/blob/v1.0.0/src/font/embedded.zig
# CodeNewRoman              OFL-1.1
# GeistMono                 OFL-1.1
# Inconsolata               OFL-1.1
# JetBrainsMono             OFL-1.1
# JuliaMono                 OFL-1.1
# KawkabMono                OFL-1.1
# Lilex                     OFL-1.1
# MonaspaceNeon             OFL-1.1
# NotoEmoji                 OFL-1.1
# CozetteVector             MIT
# NerdFont                  MIT AND OFL-1.1
Provides:       bundled(font(JetBrainsMonoNerdFont)) = 2.3.0
# the rest are used for test cases and NOT included in the final executable
# see comment in 'src/font/embedded.zig'
Provides:       bundled(font(NotoEmoji)) = 2.034
Provides:       bundled(font(KawkabMono)) = 0.501
Provides:       bundled(font(Lilex)) = 2.200
Provides:       bundled(font(CodeNewRoman)) = 2.000
Provides:       bundled(font(Inconsolata)) = 3.001
Provides:       bundled(font(GeistMono)) = 1.2.0
Provides:       bundled(font(JetBrainsMono)) = 2.3.0
Provides:       bundled(font(JuliaMono)) = 0.055
Provides:       bundled(font(CozetteVector)) = 1.22.2
Provides:       bundled(font(MonaspaceNeon)) = 1.000

ExclusiveArch:  %{zig_arches}
ExcludeArch:    %{ix86}

BuildRequires:  (zig >= {{{zig_min_version}}} with zig < {{{zig_max_version}}})
BuildRequires:  zig-rpm-macros >= 0.13.0-4
BuildRequires:  git, pandoc, fdupes, desktop-file-utils
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(zlib-ng)
BuildRequires:  pkgconfig(oniguruma)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(simdutf) >= 5.2.8
# app runtime
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  libX11-devel
BuildRequires:  wayland-devel
BuildRequires:  wayland-protocols-devel

Requires:       %{name}-terminfo = %{version}-%{release}
Requires:       %{name}-shell-integration = %{version}-%{release}
Requires:       %{name}-themes = %{version}-%{release}

%description
%{project_description}

%if %{with lib}

%package -n %{library}
Summary:        %{name} terminal library

%description -n %{library}
%{project_description}

%{summary}.

%package -n %{library}-static
Summary:        Static %{name} terminal libary

%description -n %{library}-static
%{project_description}

%{summary}.

%package -n %{library}-devel
Summary:        Development files for %{library}
BuildArch:      noarch
Requires:       %{library}

%description -n %{library}-devel
%{project_description}

%{summary}.

%endif

%package        bash-completion
Summary:        Bash completion for %{name}
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       bash-completion
Supplements:    (%{name} = %{version}-%{release} and bash-completion)

%description    bash-completion
%{project_description}

%{summary}.

%package        zsh-completion
Summary:        Zsh completion for %{name}
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       zsh
Supplements:    (%{name} = %{version}-%{release} and zsh)

%description    zsh-completion
%{project_description}

%{summary}.

%package        fish-completion
Summary:        Fish completion for %{name}
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       fish
Supplements:    (%{name} = %{version}-%{release} and fish)

%description    fish-completion
%{project_description}

%{summary}.

%package        shell-integration
Summary:        Shell integration scripts for %{name}
BuildArch:      noarch

%description    shell-integration
%{project_description}

%{summary}.

%package        nautilus
Summary:        %{name} extension for Nautilus
BuildArch:      noarch
Supplements:    (%{name} = %{version}-%{release} and nautilus)

%description    nautilus
%{project_description}

%{summary}.

%package        neovim-plugin
Summary:        Neovim plugin for %{name}
BuildArch:      noarch
Supplements:    (%{name} = %{version}-%{release} and neovim)

%description    neovim-plugin
%{project_description}

%{summary}.

%package        vim-plugin
Summary:        Vim plugin for %{name}
BuildArch:      noarch
Supplements:    (%{name} = %{version}-%{release} and vim)

%description    vim-plugin
%{project_description}

%{summary}.

%package        bat-syntax
Summary:        Bat syntax for %{name}
BuildArch:      noarch
Supplements:    (%{name} = %{version}-%{release} and bat)

%description    bat-syntax
%{project_description}

%{summary}.

%package        terminfo
Summary:        Terminfo files for %{name}
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       ncurses-base

%description    terminfo
%{project_description}

%{summary}.

%package        themes
Summary:        Themes for %{name}
BuildArch:      noarch

%description    themes
%{project_description}

%{summary}.

%package        docs
Summary:        Documentation for %{name}
BuildArch:      noarch
Enhances:       %{name} = %{version}-%{release}

%description    docs
%{project_description}

%{summary}.

%prep
{{{git_repo_setup_macro}}} %{source_setup}

# Put all packages in the cache
%zig_fetch fontconfig-%{fontconfig_version}
%zig_fetch harfbuzz-%{harfbuzz_version}
%zig_fetch utfcpp-%{utfcpp_version}
%zig_fetch iTerm2-Color-Schemes-%{iterm2_color_commit}
%zig_fetch z2d-%{z2d_commit}
%zig_fetch SPIRV-Cross-%{spirv_cross_commit}
%zig_fetch libvaxis-%{libvaxis_commit1}
%zig_fetch libvaxis-%{libvaxis_commit2}
%zig_fetch sentry-native-%{sentry_version}
%zig_fetch glslang-%{glslang_version}
%zig_fetch freetype-VER-%{freetype_dash_version}
%zig_fetch oniguruma-%{oniguruma_version}
%zig_fetch highway-%{highway_version}
%zig_fetch libxev-%{libxev_commit}
%zig_fetch imgui-%{imgui_commit}
%zig_fetch breakpad-%{breakpad_commit}
%zig_fetch wuffs-%{wuffs_version}
%zig_fetch pixels-%{pixels_commit}
%zig_fetch ziglyph
%zig_fetch zf-%{zf_commit}
%zig_fetch zigimg-%{zigimg_commit}
%zig_fetch zg
%zig_fetch zig-wayland
%zig_fetch wayland-main
%zig_fetch wayland-protocols-main
%zig_fetch plasma-wayland-protocols-%{plasma_wayland_protocols_commit}
%zig_fetch zig-objc-%{zig_objc_commit}
%zig_fetch zig-js-%{zig_js_commit}

# stubbing some packages that aren't needed
#   libxml2
mkdir %{_zig_cache_dir}/p/122032442d95c3b428ae8e526017fad881e7dc78eab4d558e9a58a80bfbd65a64f7d
#   libpng
mkdir %{_zig_cache_dir}/p/1220aa013f0c83da3fb64ea6d327f9173fa008d10e28bc9349eac3463457723b1c66
#   zlib
mkdir %{_zig_cache_dir}/p/1220fed0c74e1019b3ee29edae2051788b080cd96e90d56836eea857b0b966742efb

%build
# Building GTK frontend
%zig_build %{gtk_options}

# print out the build config
./zig-out/bin/%{name} +version

%if %{with lib}
# Building libghostty
%zig_build %{lib_options}
%endif

%install
%zig_install %{gtk_options}

%if %{with lib}
%zig_install %{lib_options}
%endif

%fdupes %{buildroot}%{_datadir}

%check
%zig_test

desktop-file-validate %{buildroot}%{_datadir}/applications/%{project_id}.desktop

%files
%license LICENSE
%{_bindir}/%{name}
%{_datadir}/applications/%{project_id}.desktop
%{_datadir}/kio/servicemenus/%{project_id}.desktop
%{_iconsdir}/hicolor/*/apps/%{project_id}.png
%{_mandir}/man{1,5}/%{name}.*

%if %{with lib}
%files -n %{library}
%{_libdir}/%{library}.so

%files -n %{library}-static
%{_libdir}/%{library}.a

%files -n %{library}-devel
%{_includedir}/%{name}.h
%endif

%files bash-completion
%{bash_completions_dir}/%{name}.bash

%files zsh-completion
%{zsh_completions_dir}/_%{name}

%files fish-completion
%{fish_completions_dir}/%{name}.fish

%files shell-integration
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/shell-integration/bash/bash-preexec.sh
%{_datadir}/%{name}/shell-integration/bash/%{name}.bash
%{_datadir}/%{name}/shell-integration/elvish/lib/%{name}-integration.elv
%{_datadir}/%{name}/shell-integration/fish/vendor_conf.d/%{name}-shell-integration.fish
%{_datadir}/%{name}/shell-integration/zsh/.zshenv
%{_datadir}/%{name}/shell-integration/zsh/%{name}-integration

%files nautilus
%{_datadir}/nautilus-python/extensions/%{project_id}.py

%files neovim-plugin
%{_datadir}/nvim/site/{compiler,ftdetect,ftplugin,syntax}/%{name}.vim

%files vim-plugin
%{_datadir}/vim/vimfiles/{compiler,ftdetect,ftplugin,syntax}/%{name}.vim

%files bat-syntax
%{_datadir}/bat/syntaxes/%{name}.sublime-syntax

%files terminfo
%{_datadir}/terminfo/g/%{name}
%{_datadir}/terminfo/x/xterm-%{name}
%{_datadir}/terminfo/%{name}.term{cap,info}

%files themes
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/themes/*

%files docs
%docdir %{_datadir}/%{name}/doc
%doc README.md PACKAGING.md CONTRIBUTING.md TODO.md
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/doc/%{name}.{1,5}.{md,html}

%changelog
* {{{git_custom_date}}} Arvin Verain <arvinverain@proton.me> - {{{git_custom_package_version}}}-{{{git_custom_release}}}
- Tip build from git main
