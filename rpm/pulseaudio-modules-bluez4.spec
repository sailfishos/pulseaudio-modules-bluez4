%define pulseversion %{expand:%(rpm -q --qf '[%%{version}]' pulseaudio)}
%define pulsemajorminor %{expand:%(echo '%{pulseversion}' | cut -d+ -f1)}
%define moduleversion %{pulsemajorminor}.%{expand:%(echo '%{version}' | cut -d. -f3)}

Name:       pulseaudio-modules-bluez4

Summary:    Legacy BlueZ4 modules for PulseAudio
Version:    1.1
Release:    1
License:    LGPLv2+
URL:        https://git.sailfishos.org/mer-core/pulseaudio-modules-bluez4
Source0:    %{name}-%{version}.tar.gz
BuildRequires:  pkgconfig(pulsecore) >= %{pulsemajorminor}
BuildRequires:  pkgconfig(dbus-1) >= 1.4.12
BuildRequires:  pkgconfig(bluez) >= 4.101
BuildRequires:  pkgconfig(sbc) >= 1.0
BuildRequires:  libtool-ltdl-devel
Conflicts:      pulseaudio <= 12.2

%description
Legacy BlueZ4 modules for PulseAudio. These are meant for legacy devices
which don't have support for BlueZ5.

%prep
%autosetup -n %{name}-%{version}

%build
echo "%{moduleversion}" > .tarball-version
%reconfigure --disable-static
%make_build

%install
rm -rf %{buildroot}
%make_install

%files
%defattr(-,root,root,-)
%{_libdir}/pulse-%{pulsemajorminor}/modules/*.so
%license LICENSE
