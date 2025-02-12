# ghostty ships some submodules that wrap around existing libraries to provide a nicer experience within zig
# those submodules rely on headers provided by vendored versions of their respective library
# they will never be compiled or included in the final binary with the exception of glslang,and spirv-cross
#
# Zig only dependencies are vendored all other dependencies will be resolved from the system
# in future releases.
%global utfcpp_version 4.0.5
%global iterm2_color_commit db227d159adc265818f2e898da0f70ef8d7b580e
%global z2d_commit 4638bb02a9dc41cc2fb811f092811f6a951c752a
%global spirv_cross_commit 476f384eb7d9e48613c45179e502a15ab95b6b49
%global libvaxis_commit1 6d729a2dc3b934818dffe06d2ba3ce02841ed74b
%global libvaxis_commit2 dc0a228a5544988d4a920cfb40be9cd28db41423
%global glslang_version 14.2.0
%global highway_version 1.1.0
%global libxev_commit 31eed4e337fed7b0149319e5cdbb62b848c24fbd
%global imgui_commit e391fe2e66eb1c96b1624ae8444dc64c23146ef4
%global wuffs_version 0.4.0-alpha.9
%global ziglyph_commit b89d43d1e3fb01b6074bc1f7fc980324b04d26a5
%global zf_commit ed99ca18b02dda052e20ba467e90b623c04690dd
%global zigimg_commit 3a667bdb3d7f0955a5a51c8468eac83210c1439e
%global zg_version 0.13.2
%global zig_gobject_version 0.2.2
%global zig_wayland_commit fbfe3b4ac0b472a27b1f1a67405436c58cbee12d
%global wayland_commit 9cb3d7aa9dc995ffafdbdef7ab86a949d0fb0e7d
%global wayland_protocols_commit 258d8f88f2c8c25a830c6316f87d23ce1a0f12d9
%global plasma_protocols_commit db525e8f9da548cffa2ac77618dd0fbe7f511b86
# These aren't needed for compiling on linux however these are not marked as lazy
# thus required to be valid zig packages
%global zig_objc_commit 9b8ba849b0f58fe207ecd6ab7c147af55b17556e
%global zig_js_commit d0b8b0a57c52fbc89f9d9fecba75ca29da7dd7d1

# needed to get rid of a header informing the user the application is compiled in debug mode
%global _zig_release_mode fast
%global library             libghostty
%global project_id          com.mitchellh.ghostty
%global project_summary     Fast, native, feature-rich terminal emulator pushing modern features

%global build_options %{shrink: \
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
    -Dsentry=false \
    -Demit-terminfo=false \
    -Demit-termcap=false \
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
Summary:        %{project_summary}

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
# zig-gobject:              0BSD
# zig-wayland:              MIT
# wayland:                  MIT
# wayland-protocols:        MIT
# plasma-wayland-protocols  LGPL-2.1-only
# iTerm2-Color-Schemes:     MIT
# pkg/utfcpp:               BSL-1.0
# pkg/spirv-cross:          Apache-2.0
# pkg/glslang:              BSD-2-Clause AND BSD-3-Clause AND GPL-3.0-or-later AND Apache-2.0
# pkg/highway:              Apache-2.0
# pkg/cimgui:               MIT
# pkg/wuffs:                Apache-2.0 AND MIT
# vendor/glad               (WTFPL OR CC0-1.0) AND Apache-2.0
License:        MIT AND 0BSD AND MPL-2.0 AND LGPL-2.1-only AND BSL-1.0 AND Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND GPL-3.0-or-later AND Apache-2.0 AND (WTFPL OR CC0-1.0)

URL:            https://ghostty.org/
Source0:        {{{git_repo_pack}}}

Source10:       https://github.com/nemtrif/utfcpp/archive/refs/tags/v%{utfcpp_version}/utfcpp-%{utfcpp_version}.tar.gz
Source11:       https://github.com/mbadolato/iTerm2-Color-Schemes/archive/%{iterm2_color_commit}/iTerm2-Color-Schemes-%{iterm2_color_commit}.tar.gz
Source12:       https://github.com/vancluever/z2d/archive/%{z2d_commit}/z2d-%{z2d_commit}.tar.gz
Source13:       https://github.com/KhronosGroup/SPIRV-Cross/archive/%{spirv_cross_commit}/SPIRV-Cross-%{spirv_cross_commit}.tar.gz
# zf requires a different version of libvaxis than ghostty
Source14:       https://github.com/rockorager/libvaxis/archive/%{libvaxis_commit1}/libvaxis-%{libvaxis_commit1}.tar.gz
Source15:       https://github.com/rockorager/libvaxis/archive/%{libvaxis_commit2}/libvaxis-%{libvaxis_commit2}.tar.gz
Source16:       https://github.com/KhronosGroup/glslang/archive/refs/tags/%{glslang_version}/glslang-%{glslang_version}.tar.gz
Source17:       https://github.com/google/highway/archive/refs/tags/%{highway_version}/highway-%{highway_version}.tar.gz
Source18:       https://github.com/mitchellh/libxev/archive/%{libxev_commit}/libxev-%{libxev_commit}.tar.gz
Source19:       https://github.com/ocornut/imgui/archive/%{imgui_commit}/imgui-%{imgui_commit}.tar.gz
Source20:       https://github.com/google/wuffs/archive/refs/tags/v%{wuffs_version}/wuffs-%{wuffs_version}.tar.gz
Source21:       https://deps.files.ghostty.org/ziglyph-%{ziglyph_commit}.tar.gz
Source22:       https://github.com/natecraddock/zf/archive/%{zf_commit}/zf-%{zf_commit}.tar.gz
Source23:       https://github.com/zigimg/zigimg/archive/%{zigimg_commit}/zigimg-%{zigimg_commit}.tar.gz
Source24:       https://codeberg.org/atman/zg/archive/v%{zg_version}.tar.gz#/zg-%{zg_version}.tar.gz
Source25:       https://github.com/ianprime0509/zig-gobject/releases/download/v%{zig_gobject_version}/bindings-gnome47.tar.zst
Source26:       https://github.com/mitchellh/zig-objc/archive/%{zig_objc_commit}/zig-objc-%{zig_objc_commit}.tar.gz
Source27:       https://github.com/mitchellh/zig-js/archive/%{zig_js_commit}/zig-js-%{zig_js_commit}.tar.gz
Source28:       https://codeberg.org/ifreund/zig-wayland/archive/%{zig_wayland_commit}.tar.gz#/zig-wayland-%{zig_wayland_commit}.tar.gz
Source29:       https://deps.files.ghostty.org/wayland-%{wayland_commit}.tar.gz#/ghostty-wayland-%{wayland_commit}.tar.gz
Source30:       https://deps.files.ghostty.org/wayland-protocols-%{wayland_protocols_commit}.tar.gz#/ghostty-wayland-protocols-%{wayland_protocols_commit}.tar.gz
Source31:       https://github.com/KDE/plasma-wayland-protocols/archive/%{plasma_protocols_commit}/plasma-wayland-protocols-%{plasma_protocols_commit}.tar.gz

%global source_setup %{lua: \
    for i = 10, 31 do \
        print(" -a " .. i) \
    end \
}

Provides:       bundled(utfcpp) = %{utfcpp_version}
Provides:       bundled(z2d) = %{z2d_commit}
Provides:       bundled(SPIRV-Cross) = %{spirv_cross_commit}
Provides:       bundled(libvaxis) = %{libvaxis_commit1}
Provides:       bundled(libvaxis) = %{libvaxis_commit2}
Provides:       bundled(glslang) = %{glslang_version}
Provides:       bundled(highway) = %{highway_version}
Provides:       bundled(libxev) = %{libxev_commit}
Provides:       bundled(imgui) = %{imgui_commit}
Provides:       bundled(wuffs) = %{wuffs_version}
Provides:       bundled(ziglyph) = %{ziglyph_commit}
Provides:       bundled(zf) = %{zf_commit}
Provides:       bundled(zigimg) = %{zigimg_commit}
Provides:       bundled(zg) = %{zg_version}
Provides:       bundled(zig-gobject) = %{zig_gobject_version}
Provides:       bundled(zig-objc) = %{zig_objc_commit}
Provides:       bundled(zig-js) = %{zig_js_commit}
Provides:       bundled(zig-wayland) = %{zig_wayland_commit}
Provides:       bundled(wayland) = %{wayland_commit}
Provides:       bundled(wayland-protocols) = %{wayland_protocols_commit}
Provides:       bundled(plasma-wayland-protocols) = %{plasma_protocols_commit}
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
BuildRequires:  git, gcc, pkg-config, fdupes, desktop-file-utils
BuildRequires:  pkgconfig(simdutf) >= 5.2.8

# font backend
BuildRequires:  pkgconfig(bzip2)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(zlib-ng)
BuildRequires:  pkgconfig(oniguruma)
BuildRequires:  pkgconfig(libxml-2.0)
# app runtime
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  libX11-devel
# docs
BuildRequires:  pandoc-cli

Requires:       %{name}-terminfo = %{version}-%{release}
Requires:       %{name}-shell-integration = %{version}-%{release}
Requires:       %{name}-themes = %{version}-%{release}

%description
Ghostty is a terminal emulator that differentiates itself by being
fast, feature-rich, and native. While there are many excellent
terminal emulators available, they all force you to choose between
speed, features, or native UIs. Ghostty provides all three.

%if %{with lib}

%package -n %{library}
Summary:        Terminal library for %{name}

%description -n %{library}
%{project_summary}.

%{summary}.

%package -n %{library}-static
Summary:        Static terminal libary for %{name}

%description -n %{library}-static
%{project_summary}.

%{summary}.

%package -n %{library}-devel
Summary:        Development files for %{library}
BuildArch:      noarch
Requires:       %{library}

%description -n %{library}-devel
%{project_summary}.

%{summary}.

%endif

%package        bash-completion
Summary:        Bash completion for %{name}
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       bash-completion
Supplements:    (%{name} = %{version}-%{release} and bash-completion)

%description    bash-completion
%{project_summary}.

%{summary}.

%package        zsh-completion
Summary:        Zsh completion for %{name}
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       zsh
Supplements:    (%{name} = %{version}-%{release} and zsh)

%description    zsh-completion
%{project_summary}.

%{summary}.

%package        fish-completion
Summary:        Fish completion for %{name}
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       fish
Supplements:    (%{name} = %{version}-%{release} and fish)

%description    fish-completion
%{project_summary}.

%{summary}.

%package        shell-integration
Summary:        Shell integration scripts for %{name}
BuildArch:      noarch

%description    shell-integration
%{project_summary}.

%{summary}.

%package        neovim-plugin
Summary:        Neovim plugin for %{name}
BuildArch:      noarch
Supplements:    (%{name} = %{version}-%{release} and neovim)

%description    neovim-plugin
%{project_summary}.

%{summary}.

%package        vim-plugin
Summary:        Vim plugin for %{name}
BuildArch:      noarch
Supplements:    (%{name} = %{version}-%{release} and vim)

%description    vim-plugin
%{project_summary}.

%{summary}.

%package        bat-syntax
Summary:        Bat syntax for %{name}
BuildArch:      noarch
Supplements:    (%{name} = %{version}-%{release} and bat)

%description    bat-syntax
%{project_summary}.

%{summary}.

%package        nautilus
Summary:        Nautilus extension for %{name}
BuildArch:      noarch
Supplements:    (%{name} = %{version}-%{release} and nautilus)

%description    nautilus
%{project_summary}.

%{summary}.

%package        terminfo
Summary:        Terminfo files for %{name}
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       ncurses-base

%description    terminfo
%{project_summary}.

%{summary}.

%package        themes
Summary:        Themes for %{name}
BuildArch:      noarch

%description    themes
%{project_summary}.

%{summary}.

%package        docs
Summary:        Documentation for %{name}
BuildArch:      noarch
Enhances:       %{name} = %{version}-%{release}

%description    docs
%{project_summary}.

%{summary}.

%prep
{{{git_repo_setup_macro}}} %{source_setup}

# Put all packages in the cache
%zig_fetch utfcpp-%{utfcpp_version}
%zig_fetch iTerm2-Color-Schemes-%{iterm2_color_commit}
%zig_fetch z2d-%{z2d_commit}
%zig_fetch SPIRV-Cross-%{spirv_cross_commit}
%zig_fetch libvaxis-%{libvaxis_commit1}
%zig_fetch libvaxis-%{libvaxis_commit2}
%zig_fetch glslang-%{glslang_version}
%zig_fetch highway-%{highway_version}
%zig_fetch libxev-%{libxev_commit}
%zig_fetch imgui-%{imgui_commit}
%zig_fetch wuffs-%{wuffs_version}
%zig_fetch ziglyph
%zig_fetch zf-%{zf_commit}
%zig_fetch zigimg-%{zigimg_commit}
%zig_fetch zg
%zig_fetch bindings
%zig_fetch zig-objc-%{zig_objc_commit}
%zig_fetch zig-js-%{zig_js_commit}
%zig_fetch zig-wayland
%zig_fetch wayland-main
%zig_fetch wayland-protocols-main
%zig_fetch plasma-wayland-protocols-%{plasma_protocols_commit}

# stubbing some packages that aren't needed
# this will not be needed once zig implements finer dependency management
# https://github.com/ziglang/zig/pull/19975
#   libxml2
mkdir %{_zig_cache_dir}/p/122032442d95c3b428ae8e526017fad881e7dc78eab4d558e9a58a80bfbd65a64f7d
#   libpng
mkdir %{_zig_cache_dir}/p/1220aa013f0c83da3fb64ea6d327f9173fa008d10e28bc9349eac3463457723b1c66
#   zlib
mkdir %{_zig_cache_dir}/p/1220fed0c74e1019b3ee29edae2051788b080cd96e90d56836eea857b0b966742efb
#   freetype
mkdir %{_zig_cache_dir}/p/1220b81f6ecfb3fd222f76cf9106fecfa6554ab07ec7fdc4124b9bb063ae2adf969d
#   harfbuzz
mkdir %{_zig_cache_dir}/p/1220b8588f106c996af10249bfa092c6fb2f35fbacb1505ef477a0b04a7dd1063122
#   fontconfig
mkdir %{_zig_cache_dir}/p/12201149afb3326c56c05bb0a577f54f76ac20deece63aa2f5cd6ff31a4fa4fcb3b7
#   oniguruma
mkdir %{_zig_cache_dir}/p/1220c15e72eadd0d9085a8af134904d9a0f5dfcbed5f606ad60edc60ebeccd9706bb
#   pixels
mkdir %{_zig_cache_dir}/p/12207ff340169c7d40c570b4b6a97db614fe47e0d83b5801a932dcd44917424c8806
#   sentry-native
mkdir %{_zig_cache_dir}/p/1220446be831adcca918167647c06c7b825849fa3fba5f22da394667974537a9c77e
#   breakpad
mkdir %{_zig_cache_dir}/p/12207fd37bb8251919c112dcdd8f616a491857b34a451f7e4486490077206dc2a1ea

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
%{_datadir}/%{name}/shell-integration/

%files neovim-plugin
%{_datadir}/nvim/site/{compiler,ftdetect,ftplugin,syntax}/%{name}.vim

%files vim-plugin
%{_datadir}/vim/vimfiles/{compiler,ftdetect,ftplugin,syntax}/%{name}.vim

%files bat-syntax
%{_datadir}/bat/syntaxes/%{name}.sublime-syntax

%files nautilus
%{_datadir}/nautilus-python/extensions/%{name}.py

%files terminfo
%{_datadir}/terminfo/g/%{name}
%{_datadir}/terminfo/x/xterm-%{name}

%files themes
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/themes/

%files docs
%docdir %{_datadir}/%{name}/doc
%doc README.md
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/doc/

%changelog
* {{{git_custom_date}}} Arvin Verain <arvinverain@proton.me> - {{{git_custom_package_version}}}-{{{git_custom_release}}}
- Tip build from git main
