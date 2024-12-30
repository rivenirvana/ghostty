%bcond test 1

%if 0%{?fedora} == 40
%bcond simdutf 0
%else
%bcond simdutf 1
%endif

%global debug_package %{nil}
%global project_id          com.mitchellh.ghostty
%global project_description Ghostty is a terminal emulator that differentiates itself by being fast, \
feature-rich, and native. While there are many excellent terminal emulators \
available, they all force you to choose between speed, features, or native UIs. \
Ghostty provides all three.

Name:           ghostty
Version:        {{{git_custom_package_version}}}
Release:        {{{git_custom_release}}}%{?dist}
Summary:        Fast, native, feature-rich terminal emulator pushing modern features

License:        MIT AND OFL-1.1
URL:            https://ghostty.org/
Source0:        {{{git_repo_archive}}}

BuildRequires:  zig >= 0.13.0, zig < 0.14.0
BuildRequires:  git, pandoc, fdupes, desktop-file-utils
BuildRequires:  pkgconfig(fontconfig), pkgconfig(freetype2), pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(glib-2.0), pkgconfig(gtk4), pkgconfig(libadwaita-1)
BuildRequires:  pkgconfig(oniguruma), pkgconfig(libpng), pkgconfig(zlib-ng)

%if %{with simdutf}
BuildRequires: pkgconfig(simdutf) >= 4.0.9
%endif

%if %{with test}
BuildRequires:  hostname
%endif

Recommends:     %{name}-terminfo = %{version}-%{release}
Recommends:     %{name}-shell-integration = %{version}-%{release}
Suggests:       %{name}-bash-completion = %{version}-%{release}
Suggests:       %{name}-fish-completion = %{version}-%{release}
Suggests:       %{name}-zsh-completion = %{version}-%{release}
Suggests:       %{name}-extras = %{version}-%{release}
Suggests:       %{name}-doc = %{version}-%{release}

%description
%{project_description}

%package        terminfo
Summary:        Terminfo files for %{name}
BuildArch:      noarch

%description    terminfo
%{project_description}

%{summary}.

%package        shell-integration
Summary:        Shell integration scripts for %{name}
BuildArch:      noarch

%description    shell-integration
%{project_description}

%{summary}.

%package        bash-completion
Summary:        Bash completion for %{name}
BuildArch:      noarch

%description    bash-completion
%{project_description}

%{summary}.

%package        fish-completion
Summary:        Fish completion for %{name}
BuildArch:      noarch

%description    fish-completion
%{project_description}

%{summary}.

%package        zsh-completion
Summary:        Zsh completion for %{name}
BuildArch:      noarch

%description    zsh-completion
%{project_description}

%{summary}.

%package        extras
Summary:        Extras for %{name}
BuildArch:      noarch

%description    extras
%{project_description}

%{summary}.

%package        doc
Summary:        Documentation for %{name}
BuildArch:      noarch

%description    doc
%{project_description}

%{summary}.

%prep
{{{git_repo_setup_macro}}}
ZIG_GLOBAL_CACHE_DIR=/tmp/offline-cache ./nix/build-support/fetch-zig-cache.sh

%build
%set_build_flags
%global _build_options %{?with_simdutf:-fsys=simdutf} --system /tmp/offline-cache/p -Dpie=true -Doptimize=ReleaseFast -Dcpu=baseline -Dtarget=native -Demit-docs=true -Dgtk-x11=true -Dversion-string={{{git_custom_internal_version}}} --summary all
zig build %{_build_options}

%install
zig build install --prefix %{buildroot}%{_prefix} %{_build_options}
%fdupes %{buildroot}%{_datadir}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{project_id}.desktop

%if %{with test}
zig build test %{_build_options}
%endif

%files
%dir %{_datadir}/%{name}
%license LICENSE
%{_bindir}/%{name}
%{_mandir}/man{1,5}/%{name}.*
%{_datadir}/applications/%{project_id}.desktop
%{_datadir}/kio/servicemenus/%{project_id}.desktop
%{_iconsdir}/hicolor/*/apps/%{project_id}.png
%{_datadir}/%{name}/themes/*

%files terminfo
%license LICENSE
%{_datadir}/terminfo/g/%{name}
%{_datadir}/terminfo/x/xterm-%{name}
%{_datadir}/terminfo/%{name}.term{cap,info}

%files shell-integration
%dir %{_datadir}/%{name}
%license LICENSE
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

%files extras
%license LICENSE
%{_datadir}/bat/syntaxes/%{name}.sublime-syntax
%{_datadir}/nvim/site/{ftdetect,ftplugin,syntax}/%{name}.vim
%{_datadir}/vim/vimfiles/{ftdetect,ftplugin,syntax}/%{name}.vim

%files doc
%dir %{_datadir}/%{name}
%docdir %{_datadir}/%{name}/doc
%license LICENSE
%doc README.md PACKAGING.md CONTRIBUTING.md TODO.md
%{_datadir}/%{name}/doc/%{name}.{1,5}.{md,html}

%changelog
* {{{git_custom_date}}} Arvin Verain <arvinverain@proton.me> - {{{git_custom_package_version}}}-{{{git_custom_release}}}
- Nightly build from git main
