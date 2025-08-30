Name:           sentinel
Version:        @VERSION@
Release:        1%{?dist}
Summary:        Sentinel – SSH Lifecycle Manager (Nuitka binary)

License:        MIT
URL:            https://github.com/Paul1404/Sentinel
Source0:        %{name}-%{version}-linux-x86_64.tar.gz

BuildArch:      x86_64

%description
Sentinel is a CLI tool for managing the lifecycle of SSH keys.
This package ships a precompiled binary built with Nuitka, so no Python runtime
or dependencies are required.

%prep
%setup -q

%build
# Nothing to build, binary is precompiled

%install
mkdir -p %{buildroot}/usr/bin
install -m 0755 sentinel-linux-x86_64-%{version} %{buildroot}/usr/bin/sentinel

%files
/usr/bin/sentinel

%changelog
* %{_date} Paul Dresch p.dresch@pdcd.net - %{version}-1
- Automated COPR build
