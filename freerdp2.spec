# TODO:
# - what is libpcsc-winpr? (-DWITH_PCSC_WINPR)
# - fix DirectFB client build (orphaned code)
#
# Conditional build:
%bcond_without	alsa		# ALSA sound support
%bcond_without	cups		# CUPS printing support
%bcond_with	directfb	# DirectFB client
%bcond_without	ffmpeg		# FFmpeg audio/video decoding support
%bcond_without	gsm		# GSM audio codec
%bcond_without	gstreamer	# GStreamer sound support
%bcond_with	openh264	# OpenH264 for H.264 codec [only if ffmpeg disabled]
%bcond_without	pcsc		# SmartCard support via PCSC-lite library
%bcond_without	pulseaudio	# Pulseaudio sound support
%bcond_without	systemd		# systemd journal support
%bcond_without	wayland		# Wayland client
%bcond_without	x11		# X11 client
%bcond_with	x264		# X264 for H.264 codec [only if ffmpeg and openh264 disabled]
%bcond_without	sse2		# SSE2 and higher instructions (runtime detection with sse patch)

%define	freerdp_api	2

%ifnarch %{ix86} %{x8664} x32
%undefine	with_sse2
%endif
Summary:	Remote Desktop Protocol client
Summary(pl.UTF-8):	Klient protokołu RDP
Name:		freerdp2
Version:	2.0.0
%define	snap	20170201
%define	gitref	6001cb710dc67eb8811362b7bf383754257a902b
%define	rel	1
Release:	0.%{snap}.%{rel}
License:	Apache v2.0
Group:		Applications/Communications
Source0:	https://github.com/FreeRDP/FreeRDP/archive/%{gitref}/freerdp-%{version}-%{snap}.tar.gz
# Source0-md5:	66f2fa62e39a9ba02ef6ca600c5281f8
Patch0:		freerdp-DirectFB-include.patch
Patch1:		freerdp-opt.patch
Patch2:		freerdp-gsm.patch
Patch3:		freerdp-sse.patch
URL:		http://www.freerdp.com/
%{?with_directfb:BuildRequires:	DirectFB-devel}
%{?with_alsa:BuildRequires:	alsa-lib-devel}
BuildRequires:	cmake >= 2.8
%{?with_cups:BuildRequires:	cups-devel}
BuildRequires:	desktop-file-utils
# libavcodec >= 53.25.0, libavutil
%{?with_ffmpeg:BuildRequires:	ffmpeg-devel >= 0.8}
%{?with_gstreamer:BuildRequires:	gstreamer-devel >= 1.0.5}
%{?with_gstreamer:BuildRequires:	gstreamer-plugins-base-devel >= 1.0.5}
%{?with_gsm:BuildRequires:	libgsm-devel}
BuildRequires:	libjpeg-devel
%{?with_x264:BuildRequires:	libx264-devel}
%{?with_openh264:BuildRequires:	openh264-devel}
BuildRequires:	openssl-devel
%{?with_pcsc:BuildRequires:	pcsc-lite-devel}
BuildRequires:	pkgconfig
%{?with_pulseaudio:BuildRequires:	pulseaudio-devel}
%{?with_systemd:BuildRequires:	systemd-devel >= 1:209}
%{?with_wayland:BuildRequires:	wayland-devel}
BuildRequires:	xmlto
%if %{with x11}
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXcursor-devel
BuildRequires:	xorg-lib-libXdamage-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXfixes-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXtst-devel
BuildRequires:	xorg-lib-libXv-devel
BuildRequires:	xorg-lib-libxkbfile
%endif
BuildRequires:	zlib-devel
Requires:	%{name}-libs = %{version}-%{release}
Requires:	hicolor-icon-theme
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# Usage: -DWITH_<option>=%{cmake_on_off <bcond_name>}
%define		cmake_on_off() %{expand:%%{?with_%{1}:ON}%%{!?with_%{1}:OFF}}

%description
FreeRDP is Remote Desktop Protocol (RDP) client.

xfreerdp can connect to RDP servers such as Microsoft Windows
machines, xrdp and VirtualBox.

%description -l pl.UTF-8
xfreerdp to klient protokołu RDP (Remote Desktop Protocol) z projektu
FreeRDP.

xfreerdp może łączyć się z serwerami RDP, takimi jak maszyny z
Microsoft Windows, xrdp oraz VirtualBox.

%package dfb
Summary:	DirectFB based Remote Desktop Protocol klient
Summary(pl.UTF-8):	Klient protokołu RDP oparty na DirectFB
Group:		Applications/Communications
Requires:	%{name} = %{version}-%{release}
Obsoletes:	freerdp-dfb < 2

%description dfb
DirectFB based Remote Desktop Protocol klient.

dfreerdp can connect to RDP servers such as Microsoft Windows
machines, xrdp and VirtualBox.

%description dfb -l pl.UTF-8
Klient protokołu RDP oparty na DirectFB.

dfreerdp może łączyć się z serwerami RDP, takimi jak maszyny z
Microsoft Windows, xrdp oraz VirtualBox.

%package wayland
Summary:	Wayland based Remote Desktop Protocol klient
Summary(pl.UTF-8):	Klient protokołu RDP oparty na Wayland
Group:		Applications/Communications
Requires:	%{name} = %{version}-%{release}

%description wayland
Wayland based Remote Desktop Protocol klient.

wlfreerdp can connect to RDP servers such as Microsoft Windows
machines, xrdp and VirtualBox.

%description wayland -l pl.UTF-8
Klient protokołu RDP oparty na Wayland.

wlfreerdp może łączyć się z serwerami RDP, takimi jak maszyny z
Microsoft Windows, xrdp oraz VirtualBox.

%package x11
Summary:	X11 based Remote Desktop Protocol klient
Summary(pl.UTF-8):	Klient protokołu RDP oparty na X11
Group:		Applications/Communications
Requires:	%{name} = %{version}-%{release}
Provides:	xfreerdp = %{version}-%{release}
Obsoletes:	freerdp < 2

%description x11
X11 based Remote Desktop Protocol klient.

xfreerdp can connect to RDP servers such as Microsoft Windows
machines, xrdp and VirtualBox.

%description x11 -l pl.UTF-8
Klient protokołu RDP oparty na X11.

xfreerdp może łączyć się z serwerami RDP, takimi jak maszyny z
Microsoft Windows, xrdp oraz VirtualBox.

%package libs
Summary:	Core libraries implementing the RDP protocol
Summary(pl.UTF-8):	Główne biblioteki implementujące protokół RDP
Group:		Libraries

%description libs
Core libraries implementing the RDP protocol.

%description libs -l pl.UTF-8
Główne biblioteki implementujące protokół RDP.

%package devel
Summary:	Development files for FreeRDP 2 libraries
Summary(pl.UTF-8):	Pliki programistyczne bibliotek FreeRDP 2
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
This package contains the header files for developing applications
that use FreeRDP 2 libraries.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia aplikacji
wykorzystujących biblioteki FreeRDP 2.

%prep
%setup -q -n FreeRDP-%{gitref}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

cat << EOF > xfreerdp.desktop
[Desktop Entry]
Type=Application
Name=X FreeRDP
NoDisplay=true
Comment=Connect to RDP server and display remote desktop
Comment[pl]=Połączenie z serwerem RDP i wyświetlanie zdalnego pulpitu
Icon=%{name}
Exec=%{_bindir}/xfreerdp
Terminal=false
Categories=Network;RemoteAccess;
EOF

%build
install -d build
cd build
%cmake .. \
	-DCMAKE_INSTALL_LIBDIR:PATH=%{_lib} \
	-DWITH_ALSA=%{cmake_on_off alsa} \
	-DWITH_CUNIT=OFF \
	-DWITH_CUPS=%{cmake_on_off cups} \
	-DWITH_DEBUG_LICENSE=ON \
	-DWITH_DIRECTFB=%{cmake_on_off directfb} \
	-DWITH_FFMPEG=%{cmake_on_off ffmpeg} \
	-DWITH_GSM=%{cmake_on_off gsm} \
	-DWITH_GSTREAMER_1_0=%{cmake_on_off gstreamer} \
	-DWITH_JPEG=ON \
	-DWITH_LIBSYSTEMD=%{cmake_on_off systemd} \
	-DWITH_OPENH264=%{cmake_on_off openh264} \
	-DWITH_OSS=ON \
	-DWITH_PCSC=%{cmake_on_off pcsc} \
	-DWITH_PULSE=%{cmake_on_off pulseaudio} \
	-DWITH_SERVER=ON \
	-DWITH_SSE2=%{cmake_on_off sse2} \
	-DWITH_WAYLAND=%{cmake_on_off wayland} \
	-DWITH_X11=%{cmake_on_off x11} \
	-DWITH_X264=%{cmake_on_off x264} \
	-DWITH_XCURSOR=ON \
	-DWITH_XEXT=ON \
	-DWITH_XINERAMA=ON \
	-DWITH_XKBFILE=ON \
	-DWITH_XV=ON

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	INSTALL="install -p" \
	DESTDIR=$RPM_BUILD_ROOT

desktop-file-install --dir=$RPM_BUILD_ROOT%{_desktopdir} xfreerdp.desktop
install -p -D resources/FreeRDP_Icon_256px.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/256x256/apps/%{name}.png

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/freerdp-shadow-cli
%attr(755,root,root) %{_bindir}/winpr-hash
%attr(755,root,root) %{_bindir}/winpr-makecert
%{_iconsdir}/hicolor/256x256/apps/freerdp2.png
%{_mandir}/man1/freerdp-shadow-cli.1*
%{_mandir}/man1/winpr-hash.1*
%{_mandir}/man1/winpr-makecert.1*
%{_mandir}/man7/wlog.7*

%if %{with directfb}
%files dfb
%defattr(644,root,root,755)
%doc doc/README.directfb
%attr(755,root,root) %{_bindir}/dfreerdp
%endif

%if %{with wayland}
%files wayland
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/wlfreerdp
%{_mandir}/man1/wlfreerdp.1*
%endif

%if %{with x11}
%files x11
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/xfreerdp
%{_desktopdir}/xfreerdp.desktop
%{_mandir}/man1/xfreerdp.1*
%endif

%files libs
%defattr(644,root,root,755)
%doc ChangeLog README
%attr(755,root,root) %{_libdir}/libfreerdp-client%{freerdp_api}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfreerdp-client%{freerdp_api}.so.2
%attr(755,root,root) %{_libdir}/libfreerdp-server%{freerdp_api}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfreerdp-server%{freerdp_api}.so.2
%attr(755,root,root) %{_libdir}/libfreerdp-shadow%{freerdp_api}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfreerdp-shadow%{freerdp_api}.so.2
%attr(755,root,root) %{_libdir}/libfreerdp-shadow-subsystem%{freerdp_api}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfreerdp-shadow-subsystem%{freerdp_api}.so.2
%attr(755,root,root) %{_libdir}/libfreerdp%{freerdp_api}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfreerdp%{freerdp_api}.so.2
%attr(755,root,root) %{_libdir}/libuwac0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libuwac0.so.0
%attr(755,root,root) %{_libdir}/libwinpr%{freerdp_api}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libwinpr%{freerdp_api}.so.2
%attr(755,root,root) %{_libdir}/libwinpr-tools%{freerdp_api}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libwinpr-tools%{freerdp_api}.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfreerdp-client%{freerdp_api}.so
%attr(755,root,root) %{_libdir}/libfreerdp-server%{freerdp_api}.so
%attr(755,root,root) %{_libdir}/libfreerdp-shadow%{freerdp_api}.so
%attr(755,root,root) %{_libdir}/libfreerdp-shadow-subsystem%{freerdp_api}.so
%attr(755,root,root) %{_libdir}/libfreerdp%{freerdp_api}.so
%attr(755,root,root) %{_libdir}/libuwac0.so
%attr(755,root,root) %{_libdir}/libwinpr%{freerdp_api}.so
%attr(755,root,root) %{_libdir}/libwinpr-tools%{freerdp_api}.so
%{_includedir}/freerdp2
%{_includedir}/uwac0
%{_includedir}/winpr2
%{_pkgconfigdir}/freerdp-client2.pc
%{_pkgconfigdir}/freerdp-server2.pc
%{_pkgconfigdir}/freerdp-shadow2.pc
%{_pkgconfigdir}/freerdp2.pc
%{_pkgconfigdir}/uwac0.pc
%{_pkgconfigdir}/winpr-tools2.pc
%{_pkgconfigdir}/winpr2.pc
%{_libdir}/cmake/FreeRDP-Client2
%{_libdir}/cmake/FreeRDP-Server2
%{_libdir}/cmake/FreeRDP-Shadow2
%{_libdir}/cmake/FreeRDP2
%{_libdir}/cmake/WinPR2
%{_libdir}/cmake/uwac0
