%define		crates_ver	12.1.1

Summary:	Line oriented search tool using Rust's regex library
Name:		ripgrep
Version:	12.1.1
Release:	1
License:	MIT or Unlicense
Group:		Applications
Source0:	https://github.com/BurntSushi/ripgrep/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	d3190853d47d51ad077a65aadbf55448
# ./create-crates.sh
Source1:	%{name}-crates-%{crates_ver}.tar.xz
# Source1-md5:	9edecedd92d2a028eff4d41fb3d8a800
URL:		https://github.com/BurntSushi/ripgrep
BuildRequires:	cargo
BuildRequires:	rpmbuild(macros) >= 2.004
BuildRequires:	rust
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
ExclusiveArch:	%{rust_arches}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ripgrep is a line-oriented search tool that recursively searches your
current directory for a regex pattern. By default, ripgrep will
respect your .gitignore and automatically skip hidden
files/directories and binary files.

%package -n bash-completion-ripgrep
Summary:	Bash completion for ripgrep
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 2.0
BuildArch:	noarch

%description -n bash-completion-ripgrep
Bash completion for ripgrep.

%package -n fish-completion-ripgrep
Summary:	fish-completion for ripgrep
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	fish
BuildArch:	noarch

%description -n fish-completion-ripgrep
fish-completion for ripgrep.

%prep
%setup -q -a1

%{__mv} %{name}-%{crates_ver}/* .
sed -i -e 's/@@VERSION@@/%{version}/' Cargo.lock

# use our offline registry
export CARGO_HOME="$(pwd)/.cargo"

mkdir -p "$CARGO_HOME"
cat >.cargo/config <<EOF
[source.crates-io]
registry = 'https://github.com/rust-lang/crates.io-index'
replace-with = 'vendored-sources'

[source.vendored-sources]
directory = '$PWD/vendor'
EOF

%build
export CARGO_HOME="$(pwd)/.cargo"

%cargo_build --frozen

%install
rm -rf $RPM_BUILD_ROOT
export CARGO_HOME="$(pwd)/.cargo"

%cargo_install --frozen --root $RPM_BUILD_ROOT%{_prefix} --path $PWD
install -D target/release/build/%{name}-*/out/rg.1 $RPM_BUILD_ROOT%{_mandir}/man1/rg.1
install -D target/release/build/%{name}-*/out/rg.bash $RPM_BUILD_ROOT%{bash_compdir}/rg
install -D target/release/build/%{name}-*/out/rg.fish $RPM_BUILD_ROOT%{fish_compdir}/rg.fish

%{__rm} $RPM_BUILD_ROOT%{_prefix}/.crates*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md COPYING FAQ.md GUIDE.md LICENSE-MIT README.md UNLICENSE
%attr(755,root,root) %{_bindir}/rg
%{_mandir}/man1/rg.1*

%files -n bash-completion-ripgrep
%defattr(644,root,root,755)
%{bash_compdir}/rg

%files -n fish-completion-ripgrep
%defattr(644,root,root,755)
%{fish_compdir}/rg.fish
