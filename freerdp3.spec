# TODO:
# - consider -DUWAC_HAVE_PIXMAN_REGION, so that libuwac would depend on pixman instead of freerdp3-libs
# - what is libpcsc-winpr? (-DWITH_PCSC_WINPR)
# - WITH_IPP?
#
# Conditional build:
%bcond_without	alsa		# ALSA sound support
%bcond_without	cups		# CUPS printing support
%bcond_without	ffmpeg		# FFmpeg audio/video codecs support (covers H264, GSM, LAME, FAAC, FAAD2, SOXR)
%bcond_with	faac		# faac for AAC audio coding (if without ffmpeg)
%bcond_with	faad		# faad2 for AAC audio decoding (if without ffmpeg)
%bcond_without	fdk_aac		# fdk-aac for AAC audio encoding and decoding 
%bcond_with	gsm		# GSM audio codec (if without ffmpeg)
%bcond_without	gstreamer	# GStreamer sound support
%bcond_without	kerberos5	# Kerberos authentication support
%bcond_with	lame		# LAME for MP3 audio codec (if without ffmpeg)
%bcond_without	opencl		# OpenCL support
%bcond_with	openh264	# OpenH264 for H.264 codec (overrides ffmpeg for H264)
%bcond_with	opus		# OPUS audio codec (if without ffmpeg)
%bcond_without	pcsc		# SmartCard support via PCSC-lite library
%bcond_without	pulseaudio	# Pulseaudio sound support
%bcond_without	rdpecam_client	# MS-RDPECAM client channel support (requires ffmpeg)
%bcond_without	sdl		# SDL client
%bcond_with	soxr		# soxr for audio resampling (if without ffmpeg)
%bcond_without	systemd		# systemd journal support
%bcond_without	wayland		# Wayland client
%bcond_without	x11		# X11 client
%bcond_without	sse2		# SSE2 and higher instructions (runtime detection with sse patch)

%define	freerdp_api	3

%ifnarch %{ix86} %{x8664} x32
%undefine	with_sse2
%endif

%if %{without ffmpeg}
%undefine	with_rdpecam_client
%endif

Summary:	Remote Desktop Protocol client
Summary(pl.UTF-8):	Klient protokołu RDP
Name:		freerdp3
Version:	3.9.0
Release:	2
License:	Apache v2.0
Group:		Applications/Communications
Source0:	https://pub.freerdp.com/releases/freerdp-%{version}.tar.xz
# Source0-md5:	bc2a02e5eeae0ae17027f64d16de1cc5
Patch0:		freerdp-opt.patch
Patch1:		freerdp-gsm.patch
Patch2:		freerdp-heimdal.patch
URL:		https://www.freerdp.com/
%{?with_opencl:BuildRequires:	OpenCL-devel}
%{?with_sdl:BuildRequires:	SDL2-devel >= 2.0}
%{?with_sdl:BuildRequires:	SDL2_image-devel >= 2.0}
%{?with_sdl:BuildRequires:	SDL2_ttf-devel >= 2.0}
%{?with_alsa:BuildRequires:	alsa-lib-devel}
%{!?with_ffmpeg:BuildRequires:	cairo-devel}
BuildRequires:	cjson-devel
BuildRequires:	cmake >= 3.13
%{?with_cups:BuildRequires:	cups-devel >= 2.0}
BuildRequires:	desktop-file-utils
BuildRequires:	docbook-style-xsl-nons
%{?with_faac:BuildRequires:	faac-devel}
%{?with_faad:BuildRequires:	faad2-devel >= 2}
%{?with_fdk_aac:BuildRequires:	fdk-aac-devel}
# libavcodec >= 57.48.101, libavresample, libavutil
%{?with_ffmpeg:BuildRequires:	ffmpeg-devel >= 3.1}
BuildRequires:	gcc >= 6:4.7
BuildRequires:	glib2-devel >= 2.0
%{?with_gstreamer:BuildRequires:	gstreamer-devel >= 1.0.5}
%{?with_gstreamer:BuildRequires:	gstreamer-plugins-base-devel >= 1.0.5}
# or gtk-webkit4
BuildRequires:	gtk-webkit4.1-devel
BuildRequires:	gtk+3-devel >= 3.0
# or MIT krb5 >= 1.14 (without heimdal patch)
%{?with_kerberos5:BuildRequires:	heimdal-devel}
%{?with_lame:BuildRequires:	lame-libs-devel}
BuildRequires:	libfuse3-devel >= 3
%{?with_gsm:BuildRequires:	libgsm-devel}
BuildRequires:	libicu-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libusb-devel >= 1.0
BuildRequires:	libwebp-devel
%{?with_rdpecam_client:BuildRequires:	libv4l-devel}
%{?with_openh264:BuildRequires:	openh264-devel}
# also mbedtls possible
BuildRequires:	openssl-devel
%{?with_opus:BuildRequires:	opus-devel}
%{?with_pcsc:BuildRequires:	pcsc-lite-devel}
BuildRequires:	pkgconfig
BuildRequires:	pkcs11-helper-devel
%{?with_pulseaudio:BuildRequires:	pulseaudio-devel}
BuildRequires:	rpmbuild(macros) >= 1.742
%{?with_soxr:BuildRequires:	soxr-devel}
%{?with_systemd:BuildRequires:	systemd-devel >= 1:209}
BuildRequires:	tar >= 1:1.22
BuildRequires:	uriparser-devel
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
BuildRequires:	xz
BuildRequires:	zlib-devel
Requires:	%{name}-libs = %{version}-%{release}
Requires:	hicolor-icon-theme
Obsoletes:	freerdp2 < 3
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

%package sdl
Summary:	SDL based Remote Desktop Protocol klient
Summary(pl.UTF-8):	Klient protokołu RDP oparty na SDL
Group:		Applications/Communications
Requires:	%{name} = %{version}-%{release}
Obsoletes:	freerdp-dfb < 2
Obsoletes:	freerdp2-dfb < 3

%description sdl
SDL based Remote Desktop Protocol client.

sdl-freerdp can connect to RDP servers such as Microsoft Windows
machines, xrdp and VirtualBox.

%description sdl -l pl.UTF-8
Klient protokołu RDP oparty na SDL.

sdl-freerdp może łączyć się z serwerami RDP, takimi jak maszyny z
Microsoft Windows, xrdp oraz VirtualBox.

%package wayland
Summary:	Wayland based Remote Desktop Protocol klient
Summary(pl.UTF-8):	Klient protokołu RDP oparty na Wayland
Group:		Applications/Communications
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-libuwac = %{version}-%{release}
Obsoletes:	freerdp2-wayland < 3

%description wayland
Wayland based Remote Desktop Protocol client.

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
Obsoletes:	freerdp2-x11 < 3

%description x11
X11 based Remote Desktop Protocol client.

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
Requires:	libfuse3-devel >= 3

%description devel
This package contains the header files for developing applications
that use FreeRDP 2 libraries.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia aplikacji
wykorzystujących biblioteki FreeRDP 2.

%package libuwac
Summary:	uwac: using wayland as a client
Summary(pl.UTF-8):	Biblioteka uwac pozwalająca na korzystanie z waylanda jako klienta
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}
Obsoletes:	freerdp2-libuwac < 3
Conflicts:	freerdp2-libs < 2.11.7-2

%description libuwac
uwac library for using wayland as a client.

%description libuwac -l pl.UTF-8
Biblioteka uwac pozwalająca na korzystanie z waylanda jako klienta.

%package libuwac-devel
Summary:	Header files for uwac library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki uwac
Group:		Development/Libraries
Requires:	%{name}-libuwac = %{version}-%{release}
Requires:	wayland-devel
Obsoletes:	freerdp2-libuwac-devel < 3
Conflicts:	freerdp2-devel < 2.11.7-2

%description libuwac-devel
Header files for uwac library.

%description libuwac-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki uwac.

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
%cmake -B build \
	-DCMAKE_INSTALL_LIBDIR:PATH=%{_lib} \
	-DWINPR_UTILS_IMAGE_JPEG=ON \
	-DWINPR_UTILS_IMAGE_PNG=ON \
	-DWINPR_UTILS_IMAGE_WEBP=ON \
	%{cmake_on_off alsa WITH_ALSA} \
	%{!?with_ffmpeg:-DWITH_CAIRO=ON} \
	%{cmake_on_off sdl WITH_CLIENT_SDL} \
	%{cmake_on_off sdl WITH_SDL_IMAGE_DIALOGS} \
	-DWITH_CUNIT=OFF \
	%{cmake_on_off cups WITH_CUPS} \
	-DWITH_DEBUG_LICENSE=ON \
	%{cmake_on_off ffmpeg WITH_DSP_FFMPEG} \
	%{cmake_on_off faac WITH_FAAC} \
	%{cmake_on_off faad WITH_FAAD2} \
	%{cmake_on_off fdk_aac WITH_FDK_AAC} \
	%{cmake_on_off ffmpeg WITH_FFMPEG} \
	%{cmake_on_off gsm WITH_GSM} \
	%{cmake_on_off gstreamer WITH_GSTREAMER_1_0} \
	-DWITH_JPEG=ON \
	%{cmake_on_off kerberos5 WITH_KRB5} \
	%{cmake_on_off systemd WITH_LIBSYSTEMD} \
	%{cmake_on_off opencl WITH_OPENCL} \
	%{cmake_on_off openh264 WITH_OPENH264} \
	%{cmake_on_off opus WITH_OPUS} \
	-DWITH_OSS=ON \
	%{cmake_on_off pcsc WITH_PCSC} \
	%{cmake_on_off pulseaudio WITH_PULSE} \
	%{cmake_on_off rdpecam_client CHANNEL_RDPECAM_CLIENT} \
	-DWITH_SERVER=ON \
	%{cmake_on_off soxr WITH_SOXR} \
	%{cmake_on_off sse2 WITH_SSE2} \
	%{cmake_on_off ffmpeg WITH_SWSCALE} \
	-DWITH_TIMEZONE_ICU=ON \
	%{cmake_on_off ffmpeg WITH_VAAPI} \
	%{cmake_on_off ffmpeg WITH_VIDEO_FFMPEG} \
	%{cmake_on_off wayland WITH_WAYLAND} \
	-DWITH_WEBVIEW=ON \
	%{cmake_on_off x11 WITH_X11} \
	-DWITH_XCURSOR=ON \
	-DWITH_XEXT=ON \
	-DWITH_XI=ON \
	-DWITH_XINERAMA=ON \
	-DWITH_XRENDER=ON \
	-DWITH_XV=ON

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	INSTALL="install -p" \
	DESTDIR=$RPM_BUILD_ROOT

desktop-file-install --dir=$RPM_BUILD_ROOT%{_desktopdir} xfreerdp.desktop
install -p -D resources/FreeRDP_Icon_256px.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/256x256/apps/%{name}.png

# empty dirs
rmdir $RPM_BUILD_ROOT%{_includedir}/{rdtk0/CMakeFiles,uwac0/CMakeFiles,winpr3/CMakeFiles,winpr3/config}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post	libuwac -p /sbin/ldconfig
%postun	libuwac -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/freerdp-proxy
%attr(755,root,root) %{_bindir}/freerdp-shadow-cli
%attr(755,root,root) %{_bindir}/sfreerdp
%attr(755,root,root) %{_bindir}/sfreerdp-server
%attr(755,root,root) %{_bindir}/winpr-hash
%attr(755,root,root) %{_bindir}/winpr-makecert
%{_datadir}/FreeRDP
%{_iconsdir}/hicolor/256x256/apps/freerdp3.png
%{_mandir}/man1/freerdp-proxy.1*
%{_mandir}/man1/freerdp-shadow-cli.1*
%{_mandir}/man1/winpr-hash.1*
%{_mandir}/man1/winpr-makecert.1*
%{_mandir}/man7/wlog.7*

%if %{with sdl}
%files sdl
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/sdl-freerdp
%{_mandir}/man1/sdl-freerdp.1*
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
%doc ChangeLog README.md SECURITY.md
%attr(755,root,root) %{_libdir}/libfreerdp-client%{freerdp_api}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfreerdp-client%{freerdp_api}.so.3
%attr(755,root,root) %{_libdir}/libfreerdp-server%{freerdp_api}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfreerdp-server%{freerdp_api}.so.3
%attr(755,root,root) %{_libdir}/libfreerdp-server-proxy%{freerdp_api}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfreerdp-server-proxy%{freerdp_api}.so.3
%attr(755,root,root) %{_libdir}/libfreerdp-shadow%{freerdp_api}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfreerdp-shadow%{freerdp_api}.so.3
%attr(755,root,root) %{_libdir}/libfreerdp-shadow-subsystem%{freerdp_api}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfreerdp-shadow-subsystem%{freerdp_api}.so.3
%attr(755,root,root) %{_libdir}/libfreerdp%{freerdp_api}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfreerdp%{freerdp_api}.so.3
%attr(755,root,root) %{_libdir}/librdtk0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/librdtk0.so.0
%attr(755,root,root) %{_libdir}/libwinpr%{freerdp_api}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libwinpr%{freerdp_api}.so.3
%attr(755,root,root) %{_libdir}/libwinpr-tools%{freerdp_api}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libwinpr-tools%{freerdp_api}.so.3
%dir %{_libdir}/freerdp3
%dir %{_libdir}/freerdp3/proxy
%attr(755,root,root) %{_libdir}/freerdp3/proxy/proxy-bitmap-filter-plugin.so
%attr(755,root,root) %{_libdir}/freerdp3/proxy/proxy-demo-plugin.so
%attr(755,root,root) %{_libdir}/freerdp3/proxy/proxy-dyn-channel-dump-plugin.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfreerdp-client%{freerdp_api}.so
%attr(755,root,root) %{_libdir}/libfreerdp-server%{freerdp_api}.so
%attr(755,root,root) %{_libdir}/libfreerdp-server-proxy%{freerdp_api}.so
%attr(755,root,root) %{_libdir}/libfreerdp-shadow%{freerdp_api}.so
%attr(755,root,root) %{_libdir}/libfreerdp-shadow-subsystem%{freerdp_api}.so
%attr(755,root,root) %{_libdir}/libfreerdp%{freerdp_api}.so
%attr(755,root,root) %{_libdir}/librdtk0.so
%attr(755,root,root) %{_libdir}/libwinpr%{freerdp_api}.so
%attr(755,root,root) %{_libdir}/libwinpr-tools%{freerdp_api}.so
%{_includedir}/freerdp3
%{_includedir}/rdtk0
%{_includedir}/winpr3
%{_pkgconfigdir}/freerdp-client3.pc
%{_pkgconfigdir}/freerdp-server3.pc
%{_pkgconfigdir}/freerdp-server-proxy3.pc
%{_pkgconfigdir}/freerdp-shadow3.pc
%{_pkgconfigdir}/freerdp3.pc
%{_pkgconfigdir}/rdtk0.pc
%{_pkgconfigdir}/winpr-tools3.pc
%{_pkgconfigdir}/winpr3.pc
%{_libdir}/cmake/FreeRDP-Client3
%{_libdir}/cmake/FreeRDP-Proxy3
%{_libdir}/cmake/FreeRDP-Server3
%{_libdir}/cmake/FreeRDP-Shadow3
%{_libdir}/cmake/FreeRDP3
%{_libdir}/cmake/WinPR-tools3
%{_libdir}/cmake/WinPR3
%{_libdir}/cmake/rdtk0

%files libuwac
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libuwac0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libuwac0.so.0

%files libuwac-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libuwac0.so
%{_includedir}/uwac0
%{_pkgconfigdir}/uwac0.pc
%{_libdir}/cmake/uwac0
