#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
Summary:	C library for executing name service queries asynchronously
Summary(pl.UTF-8):	Biblioteka C do asynchronicznego wykonywania zapytań o nazwy
Name:		libasyncns
Version:	0.5
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://0pointer.de/lennart/projects/libasyncns/%{name}-%{version}.tar.gz
# Source0-md5:	0347f9916dfb6cd0da5c38c4406d76e5
Patch0:		%{name}-link.patch
URL:		http://0pointer.de/lennart/projects/libasyncns/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.9
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libasyncns is a C library for Linux/Unix for executing name service
queries asynchronously. It is an asynchronous wrapper around
getaddrinfo(3) and getnameinfo(3) from the libc.

In contrast to GNU's asynchronous name resolving API getaddrinfo_a(),
libasyncns does not make use of UNIX signals for reporting completion
of name queries. Instead, the API exports a standard UNIX file
descriptor which may be integerated cleanly into custom main loops.

%description -l pl.UTF-8
libasyncns to biblioteka C dla Linuksa/Uniksa do asynchronicznego
wykonywania zapytań o nazwy. Jest to asynchroniczne obudowanie dla
funkcji getaddrinfo(3) i getnameinfo(3) z libc.

W przeciwieństwie do asynchronicznego API rozwiązywania nazw GNU,
getaddrinfo_a(), libasyncns nie wykorzystuje uniksowych sygnałów do
informowania o zakończeniu zapytań. Zamiast tego API eksportuje
standardowy uniksowy deskryptor pliku, który można łatwo zintegrować
we własnych głównych pętlach.

%package devel
Summary:	Header files for libasyncns library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libasyncns
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libasyncns library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libasyncns.

%package static
Summary:	Static libasyncns library
Summary(pl.UTF-8):	Statyczna biblioteka libasyncns
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libasyncns library.

%description static -l pl.UTF-8
Statyczna biblioteka libasyncns.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
# no need to generate doc/README from doc/README.html, there is README anyway
%configure \
	--disable-lynx \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_libdir}/libasyncns.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libasyncns.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libasyncns.so
%{_libdir}/libasyncns.la
%{_includedir}/asyncns.h
%{_pkgconfigdir}/libasyncns.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libasyncns.a
%endif
