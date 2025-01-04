%bcond test 1

%if 0%{?fedora} == 40
%bcond simdutf 0
%else
%bcond simdutf 1
%endif

%global debug_package %{nil}
%global project_id          com.mitchellh.ghostty
%global project_description %{expand:
Ghostty is a terminal emulator that differentiates itself by being fast,
feature-rich, and native. While there are many excellent terminal emulators
available, they all force you to choose between speed, features, or native UIs.
Ghostty provides all three.
}

%global _build_options %{shrink:
    --summary all \
    -Doptimize=ReleaseFast \
    -Dpie=true \
    -Dgtk-x11=true \
    -Demit-docs=true \
    -Dversion-string={{{git_custom_internal_version}}} \
    %{?with_simdutf:-fsys=simdutf}
}

Name:           ghostty
Version:        {{{git_custom_package_version}}}
Release:        {{{git_custom_release}}}%{?dist}
Summary:        Fast, native, feature-rich terminal emulator pushing modern features

License:        MIT AND OFL-1.1
URL:            https://ghostty.org/
Source0:        {{{git_repo_archive}}}

ExclusiveArch:  %{zig_arches}
ExcludeArch:    i686

BuildRequires:  (zig >= {{{zig_min_version}}} with zig < {{{zig_max_version}}})
BuildRequires:  zig-rpm-macros >= 0.13.0-4
BuildRequires:  git, pandoc, fdupes, desktop-file-utils
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(oniguruma)
BuildRequires:  pkgconfig(zlib-ng)

%if %{with test}
BuildRequires:  hostname
%endif

%if %{with simdutf}
BuildRequires:  pkgconfig(simdutf) >= 4.0.9
%else
Provides:       bundled(simdutf) = 4.0.9
%endif

Provides:       bundled(font(CodeNewRoman)) = 2.000
Provides:       bundled(font(CozetteVector)) = 1.22.2
Provides:       bundled(font(GeistMono)) = 1.2.0
Provides:       bundled(font(Inconsolata)) = 3.001
Provides:       bundled(font(JetBrainsMonoNerdFont)) = 2.3.0
Provides:       bundled(font(JetBrainsMonoNoNF)) = 2.3.0
Provides:       bundled(font(JuliaMono)) = 0.055
Provides:       bundled(font(KawkabMono)) = 0.501
Provides:       bundled(font(Lilex)) = 2.200
Provides:       bundled(font(MonaspaceNeon)) = 1.000
Provides:       bundled(font(NotoColorEmoji)) = 2.034
Provides:       bundled(font(NotoEmoji)) = 2.034

Provides:       bundled(glslang) = 14.2.0
Provides:       bundled(spirv-cross) = 13.1.1

Requires:       %{name}-terminfo = %{version}-%{release}
Requires:       %{name}-shell-integration = %{version}-%{release}
Suggests:       %{name}-bash-completion = %{version}-%{release}
Suggests:       %{name}-fish-completion = %{version}-%{release}
Suggests:       %{name}-zsh-completion = %{version}-%{release}
Suggests:       %{name}-themes = %{version}-%{release}
Suggests:       %{name}-extras = %{version}-%{release}
Suggests:       %{name}-doc = %{version}-%{release}

%description
%{project_description}

%package        terminfo
Summary:        Terminfo files for %{name}
License:        MIT
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       ncurses-base
Supplements:    %{name} = %{version}-%{release}

%description    terminfo
%{project_description}

%{summary}.

%package        shell-integration
Summary:        Shell integration scripts for %{name}
License:        MIT
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       (bash or fish or zsh or elvish)
Supplements:    (%{name} = %{version}-%{release} and (bash or fish or zsh or elvish))

%description    shell-integration
%{project_description}

%{summary}.

%package        bash-completion
Summary:        Bash completion for %{name}
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       bash-completion
Supplements:    (%{name} = %{version}-%{release} and bash-completion)

%description    bash-completion
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

%package        zsh-completion
Summary:        Zsh completion for %{name}
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       zsh
Supplements:    (%{name} = %{version}-%{release} and zsh)

%description    zsh-completion
%{project_description}

%{summary}.

%package        themes
Summary:        Themes for %{name}
License:        MIT
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Supplements:    %{name} = %{version}-%{release}

%description    themes
%{project_description}

%{summary}.

%package        extras
Summary:        Extras for %{name}
License:        MIT
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Supplements:    %{name} = %{version}-%{release}

%description    extras
%{project_description}

%{summary}.

%package        doc
Summary:        Documentation for %{name}
License:        MIT
BuildArch:      noarch
Enhances:       %{name} = %{version}-%{release}

%description    doc
%{project_description}

%{summary}.

%prep
{{{git_repo_setup_macro}}}

%build
%zig_build --fetch
%zig_fetch git+https://github.com/zigimg/zigimg#3a667bdb3d7f0955a5a51c8468eac83210c1439e
%zig_fetch git+https://github.com/mitchellh/libxev#f6a672a78436d8efee1aa847a43a900ad773618b

%zig_build %{_build_options}

%install
%zig_install %{_build_options}
%fdupes %{buildroot}%{_datadir}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{project_id}.desktop
%{buildroot}%{_bindir}/%{name} +version

%if %{with test}
%zig_test %{_build_options}
%endif

%files
%license LICENSE src/font/res/OFL.txt
%{_bindir}/%{name}
%{_datadir}/applications/%{project_id}.desktop
%{_datadir}/kio/servicemenus/%{project_id}.desktop
%{_iconsdir}/hicolor/*/apps/%{project_id}.png
%{_mandir}/man{1,5}/%{name}.*

%files terminfo
%license LICENSE
%{_datadir}/terminfo/g/%{name}
%{_datadir}/terminfo/x/xterm-%{name}
%{_datadir}/terminfo/%{name}.term{cap,info}

%files shell-integration
%license LICENSE
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/shell-integration/bash/bash-preexec.sh
%{_datadir}/%{name}/shell-integration/bash/%{name}.bash
%{_datadir}/%{name}/shell-integration/elvish/lib/%{name}-integration.elv
%{_datadir}/%{name}/shell-integration/fish/vendor_conf.d/%{name}-shell-integration.fish
%{_datadir}/%{name}/shell-integration/zsh/.zshenv
%{_datadir}/%{name}/shell-integration/zsh/%{name}-integration

%files bash-completion
%{_datadir}/bash-completion/completions/%{name}.bash

%files fish-completion
%{_datadir}/fish/vendor_completions.d/%{name}.fish

%files zsh-completion
%{_datadir}/zsh/site-functions/_%{name}

%files themes
%license LICENSE
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/themes/*

%files extras
%license LICENSE
%{_datadir}/bat/syntaxes/%{name}.sublime-syntax
%{_datadir}/nvim/site/{ftdetect,ftplugin,syntax}/%{name}.vim
%{_datadir}/vim/vimfiles/{ftdetect,ftplugin,syntax}/%{name}.vim

%files doc
%license LICENSE
%docdir %{_datadir}/%{name}/doc
%doc README.md PACKAGING.md CONTRIBUTING.md TODO.md
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/doc/%{name}.{1,5}.{md,html}

%changelog
* {{{git_custom_date}}} Arvin Verain <arvinverain@proton.me> - {{{git_custom_package_version}}}-{{{git_custom_release}}}
- Tip build from git main
