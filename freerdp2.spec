# TODO:
# - what is libpcsc-winpr? (-DWITH_PCSC_WINPR)
# - fix DirectFB client build (orphaned code)
# - WITH_IPP?
#
# Conditional build:
%bcond_without	alsa		# ALSA sound support
%bcond_without	cups		# CUPS printing support
%bcond_with	directfb	# DirectFB client
%bcond_without	ffmpeg		# FFmpeg audio/video codecs support (covers H264, GSM, LAME, FAAC, FAAD2, SOXR)
%bcond_with	faac		# faac for AAC audio coding (if without ffmpeg)
%bcond_with	faad		# faad2 for AAC audio decoding (if without ffmpeg)
%bcond_with	gsm		# GSM audio codec (if without ffmpeg)
%bcond_without	gstreamer	# GStreamer sound support
# for now the kerberos5 support has to be disabled due to a bad state of its code.
# See: https://github.com/FreeRDP/FreeRDP/issues/4348
# See: https://github.com/FreeRDP/FreeRDP/issues/5746
%bcond_with	kerberos5	# GSSAPI auth support
%bcond_with	lame		# LAME for MP3 audio codec (if without ffmpeg)
%bcond_without	opencl		# OpenCL support
%bcond_with	openh264	# OpenH264 for H.264 codec (overrides ffmpeg for H264)
%bcond_without	pcsc		# SmartCard support via PCSC-lite library
%bcond_without	pulseaudio	# Pulseaudio sound support
%bcond_with	soxr		# soxr for audio resampling (if without ffmpeg)
%bcond_without	systemd		# systemd journal support
%bcond_without	wayland		# Wayland client
%bcond_without	x11		# X11 client
%bcond_with	x264		# X264 for H.264 codec (only if without ffmpeg and openh264)
%bcond_without	sse2		# SSE2 and higher instructions (runtime detection with sse patch)

%define	freerdp_api	2

%ifnarch %{ix86} %{x8664} x32
%undefine	with_sse2
%endif
Summary:	Remote Desktop Protocol client
Summary(pl.UTF-8):	Klient protokołu RDP
Name:		freerdp2
Version:	2.3.0
Release:	1
License:	Apache v2.0
Group:		Applications/Communications
Source0:	https://pub.freerdp.com/releases/freerdp-%{version}.tar.gz
# Source0-md5:	e07c94cc753dcd8e8ebbeadd71ed9c74
Patch0:		freerdp-opt.patch
Patch1:		freerdp-gsm.patch
Patch2:		docbook-xsl.patch
URL:		http://www.freerdp.com/
%{?with_directfb:BuildRequires:	DirectFB-devel}
%{?with_opencl:BuildRequires:	OpenCL-devel}
%{?with_alsa:BuildRequires:	alsa-lib-devel}
%{!?with_ffmpeg:BuildRequires:	cairo-devel}
BuildRequires:	cmake >= 2.8
%{?with_cups:BuildRequires:	cups-devel}
BuildRequires:	desktop-file-utils
BuildRequires:	docbook-style-xsl-nons
%{?with_faac:BuildRequires:	faac-devel}
%{?with_faad:BuildRequires:	faad2-devel >= 2}
# libavcodec >= 57.48.101, libavresample, libavutil
%{?with_ffmpeg:BuildRequires:	ffmpeg-devel >= 3.1}
%{?with_gstreamer:BuildRequires:	gstreamer-devel >= 1.0.5}
%{?with_gstreamer:BuildRequires:	gstreamer-plugins-base-devel >= 1.0.5}
# MIT krb5 >= 1.13 also possible
%{?with_kerberos5:BuildRequires:	heimdal-devel}
%{?with_lame:BuildRequires:	lame-libs-devel}
%{?with_gsm:BuildRequires:	libgsm-devel}
BuildRequires:	libjpeg-devel
%{?with_x264:BuildRequires:	libx264-devel}
%{?with_openh264:BuildRequires:	openh264-devel}
# also mbedtls possible
BuildRequires:	openssl-devel
%{?with_pcsc:BuildRequires:	pcsc-lite-devel}
BuildRequires:	pkgconfig
%{?with_pulseaudio:BuildRequires:	pulseaudio-devel}
BuildRequires:	rpmbuild(macros) >= 1.742
%{?with_soxr:BuildRequires:	soxr-devel}
%{?with_systemd:BuildRequires:	systemd-devel >= 1:209}
%{?with_wayland:BuildRequires:	wayland-devel}
BuildRequires:	xmlto
%{?with_wayland:BuildRequires:	xorg-lib-libxkbcommon-devel}
%if %{with x11}
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXcursor-devel
BuildRequires:	xorg-lib-libXdamage-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXfixes-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXrandr-devel
BuildRequires:	xorg-lib-libXtst-devel
BuildRequires:	xorg-lib-libXv-devel
BuildRequires:	xorg-lib-libxkbfile-devel
%endif
BuildRequires:	zlib-devel
Requires:	%{name}-libs = %{version}-%{release}
Requires:	hicolor-icon-theme
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
%setup -q -n freerdp-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

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
	%{cmake_on_off alsa WITH_ALSA} \
	%{!?with_ffmpeg:-DWITH_CAIRO=ON} \
	-DWITH_CUNIT=OFF \
	%{cmake_on_off cups WITH_CUPS} \
	-DWITH_DEBUG_LICENSE=ON \
	%{cmake_on_off directfb WITH_DIRECTFB} \
	%{cmake_on_off ffmpeg WITH_DSP_FFMPEG} \
	%{cmake_on_off faac WITH_FAAC} \
	%{cmake_on_off faad WITH_FAAD2} \
	%{cmake_on_off ffmpeg WITH_FFMPEG} \
	%{cmake_on_off gsm WITH_GSM} \
	%{cmake_on_off gstreamer WITH_GSTREAMER_1_0} \
	%{cmake_on_off kerberos5 WITH_GSSAPI} \
	-DWITH_JPEG=ON \
	%{cmake_on_off systemd WITH_LIBSYSTEMD} \
	%{cmake_on_off opencl WITH_OPENCL} \
	%{cmake_on_off openh264 WITH_OPENH264} \
	-DWITH_OSS=ON \
	%{cmake_on_off pcsc WITH_PCSC} \
	%{cmake_on_off pulseaudio WITH_PULSE} \
	-DWITH_SERVER=ON \
	%{cmake_on_off soxr WITH_SOXR} \
	%{cmake_on_off sse2 WITH_SSE2} \
	%{cmake_on_off ffmpeg WITH_SWSCALE} \
	%{cmake_on_off wayland WITH_WAYLAND} \
	%{cmake_on_off x11 WITH_X11} \
	%{cmake_on_off x264 WITH_X264} \
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
%attr(755,root,root) %{_bindir}/freerdp-proxy
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
%doc ChangeLog README.md
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
