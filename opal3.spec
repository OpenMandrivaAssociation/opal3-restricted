%define _enable_debug_packages %{nil}
%define debug_package %{nil}

%define major		%{version}
%define libname		%mklibname opal %{major}
%define devname		%mklibname %{name} -d

######################
# Hardcode PLF build
%define build_plf 1
######################

%if %{build_plf}
%define distsuffix plf
# make EVR of plf build higher than regular to allow update, needed with rpm5 mkrel
%define extrarelsuffix plf
%endif

%define url_ver %(echo %version | cut -d. -f1,2)

Summary:	VoIP library
Name:		opal3
Version:	3.10.10
Release:	4%{?extrarelsuffix}
License:	MPL
Group:		System/Libraries
URL:		http://www.opalvoip.org/
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/opal/%{url_ver}/opal-%{version}.tar.xz
Patch0:		opal-3.10.7-fix-link.patch
Patch2:		opal-3.10.7-ffmpeg-0.11.patch
Patch3:		opal-3.10.10-ffmpeg-2.0.patch
BuildRequires:	gawk
BuildRequires:	openldap-devel
BuildRequires:	ptlib-devel >= 2.10.7
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(speex)
BuildRequires:	pkgconfig(theora)
BuildRequires:	ffmpeg-devel
%if %{build_plf}
BuildRequires:	pkgconfig(x264)
%endif

%description
This is an open source class library for the development of
applications that wish to use SIP / H.323 protocols for multimedia
communications over packet based networks.

%if %{build_plf}
This package is in restricted repository because the H264 codec is
covered by patents.
%endif

#----------------------------------------------------------------------------

%package -n	%{libname}-plugins
Summary:	Codec plugins for Opal
Group:		System/Libraries
Provides:	%{name}-plugins = %{EVRD}

%description -n	%{libname}-plugins
PTlib codec plugins for various formats provided by Opal.

%files -n %{libname}-plugins
%{_libdir}/opal-%{version}/codecs/audio/*
%{_libdir}/opal-%{version}/codecs/video/*

#----------------------------------------------------------------------------

%package -n	%{libname}
Summary:	Opal Library
Group:		System/Libraries
Provides:	%{name} = %{EVRD}
Requires:	%{libname}-plugins = %{EVRD}

%description -n	%{libname}
Shared library for OPAL (SIP / H323 stack).

%files -n %{libname}
%attr(0755,root,root) %{_libdir}/lib*.so.%{major}*

#----------------------------------------------------------------------------

%package -n	%{devname}
Summary:	Opal development files
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n	%{devname}
Header files and libraries for developing applications that use
Opal.

%files -n %{devname}
%doc mpl-1.0.htm
%attr(0755,root,root) %{_libdir}/*.so
%{_libdir}/*.*a
%{_includedir}/*
%{_libdir}/pkgconfig/opal.pc

#----------------------------------------------------------------------------

%prep
%setup -q -n opal-%{version}
%patch0 -p0 -b .link
%patch2 -p0 -b .ffmpeg
%patch3 -p1 -b .ffmpeg2

%build
#gw don't use the default %%optflags, see
# https://qa.mandriva.com/show_bug.cgi?id=48476
%define optflags %nil
#gw else the UINT64_C macro is not defined by stdint.h
export STDCCFLAGS=-D__STDC_CONSTANT_MACROS
%configure2_5x
%make

%install
%makeinstall_std

# remove incorrect symlinks (http://bugzilla.gnome.org/show_bug.cgi?id=553808 )
rm -f %{buildroot}%{_libdir}/libopal.so.?
rm -f %{buildroot}%{_libdir}/libopal.so.?.?

