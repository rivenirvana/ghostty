%bcond test 1

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
URL:            https://github.com/ghostty-org/ghostty
Source0:        {{{git_repo_archive}}}

BuildRequires:  git zig ncurses freetype-devel oniguruma-devel gtk4-devel libadwaita-devel pandoc

Requires:       %{name}-terminfo = %{version}-%{release}
Requires:       %{name}-shell-integration = %{version}-%{release}
Recommends:     %{name}-extras = %{version}-%{release}
Recommends:     %{name}-doc = %{version}-%{release}

%description
%{project_description}

%package        terminfo
Summary:        Terminfo files for %{name}
BuildArch:      noarch

%description    terminfo
%{project_description}

Terminfo files for %{name}.

%package        shell-integration
Summary:        Shell integration scripts for %{name}
BuildArch:      noarch

%description    shell-integration
%{project_description}

Shell integration scripts for %{name}.

%package        extras
Summary:        Extras for %{name}
BuildArch:      noarch

%description    extras
%{project_description}

Extras for %{name}.

%package        doc
Summary:        Documentation for %{name}
BuildArch:      noarch

%description    doc
%{project_description}

Documentation for %{name}.

%prep
{{{git_repo_setup_macro}}}
ZIG_GLOBAL_CACHE_DIR=/tmp/offline-cache ./nix/build-support/fetch-zig-cache.sh

%build
%set_build_flags
zig build \
    --system /tmp/offline-cache/p \
    -Doptimize=ReleaseFast \
    -Demit-docs \
    -Dcpu=baseline \
    -Dversion-string={{{git_custom_internal_version}}}

%install
cp -r zig-out %{buildroot}%{_prefix}

%check
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{project_id}.desktop

%if %{with test}
zig build test
%endif

%files
%dir %{_datadir}/%{name}
%license LICENSE
%{_bindir}/%{name}
%{_mandir}/man{1,5}/%{name}.*
%{_datadir}/applications/%{project_id}.desktop
%{_datadir}/kio/servicemenus/%{project_id}.desktop
%{_datadir}/icons/hicolor/*/apps/%{project_id}.png
%{_datadir}/%{name}/themes/*

%files terminfo
%license LICENSE
%{_datadir}/terminfo/g/%{name}
%{_datadir}/terminfo/x/xterm-%{name}
%{_datadir}/terminfo/%{name}.term{cap,info}

%files shell-integration
%dir %{_datadir}/%{name}
%license LICENSE
%{_datadir}/bash-completion/completions/%{name}.bash
%{_datadir}/fish/vendor_completions.d/%{name}.fish
%{_datadir}/zsh/site-functions/_%{name}
%{_datadir}/%{name}/shell-integration/bash/bash-preexec.sh
%{_datadir}/%{name}/shell-integration/bash/%{name}.bash
%{_datadir}/%{name}/shell-integration/elvish/lib/%{name}-integration.elv
%{_datadir}/%{name}/shell-integration/fish/vendor_conf.d/%{name}-shell-integration.fish
%{_datadir}/%{name}/shell-integration/zsh/.zshenv
%{_datadir}/%{name}/shell-integration/zsh/%{name}-integration

%files extras
%license LICENSE
%{_datadir}/bat/syntaxes/%{name}.sublime-syntax
%{_datadir}/nvim/site/{ftdetect,ftplugin,syntax}/%{name}.vim
%{_datadir}/vim/vimfiles/{ftdetect,ftplugin,syntax}/%{name}.vim

%files doc
%dir %{_datadir}/%{name}
%license LICENSE
%doc README.md PACKAGING.md CONTRIBUTING.md TODO.md
%{_datadir}/%{name}/doc/%{name}.{1,5}.{md,html}

%changelog
* {{{git_custom_date}}} Arvin Verain <arvinverain@proton.me> - {{{git_custom_package_version}}}-{{{git_custom_release}}}
- Nightly build from git main
