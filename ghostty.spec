# https://github.com/ziglang/zig/pull/22357
%bcond lib  0
%bcond test 1

# needed to get rid of a header informing the user the application is compiled in debug mode
%global _zig_release_mode   fast
%global library             libghostty
%global project_id          com.mitchellh.ghostty
%global project_summary     Fast, native, feature-rich terminal emulator pushing modern features

%global build_options %{shrink:
    --summary all
    -Doptimize=ReleaseFast
    -fno-sys=glslang
    -fsys=simdutf
    -fsys=gtk4-layer-shell
    -Dflatpak=false
    -Dfont-backend=fontconfig_freetype
    -Drenderer=opengl
    -Dgtk-x11=true
    -Dgtk-wayland=true
    -Dpie=true
    -Demit-docs=true
    -Dversion-string={{{git_custom_internal_version}}}
    -Dstrip=false
    -Dsentry=false
    -Demit-terminfo=false
    -Demit-termcap=false
}

%global gtk_options %{shrink:
    %{build_options}
    -Dapp-runtime=gtk
}

%global lib_options %{shrink:
    %{build_options}
    -Dapp-runtime=none
}

Name:           ghostty
Version:        {{{git_custom_package_version}}}
Release:        {{{git_custom_release}}}%{?dist}
Summary:        %{project_summary}

License:        MIT

URL:            https://ghostty.org/
Source0:        {{{git_repo_pack}}}

ExclusiveArch:  %{zig_arches}
ExcludeArch:    %{ix86}

BuildRequires:  (zig >= {{{zig_min_version}}} with zig < {{{zig_max_version}}})
BuildRequires:  zig-rpm-macros >= 0.13.0-4
BuildRequires:  git, gcc, pkg-config
BuildRequires:  fdupes, desktop-file-utils, libappstream-glib, pandoc-cli
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
BuildRequires:  gtk4-layer-shell-devel
BuildRequires:  libX11-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  blueprint-compiler

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
{{{git_repo_setup_macro}}}
ZIG_GLOBAL_CACHE_DIR=%{_zig_cache_dir} ./nix/build-support/fetch-zig-cache.sh

%build
%zig_build %{gtk_options}
./zig-out/bin/%{name} +version

%if %{with lib}
%zig_build %{lib_options}
%endif

%install
%zig_install %{gtk_options}

%if %{with lib}
%zig_install %{lib_options}
%endif

%fdupes %{buildroot}%{_datadir}

%check
%if %{with test}
%zig_test
%endif

appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/%{project_id}.desktop

%files
%license LICENSE
%{_bindir}/%{name}
%{_datadir}/applications/%{project_id}.desktop
%{_datadir}/kio/servicemenus/%{project_id}.desktop
%{_datadir}/locale/*/LC_MESSAGES/%{project_id}.mo
%{_iconsdir}/hicolor/*/apps/%{project_id}.png
%{_mandir}/man{1,5}/%{name}.*
%{_metainfodir}/*.xml

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
