#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeframever	5.99
%define		qtver		5.15.2
%define		kfname		kdav
Summary:	Kdav
Name:		kf5-%{kfname}
Version:	5.99.0
Release:	3
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	f36ad243320bfb3c86e84e5c802c2779
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5Gui-devel
BuildRequires:	Qt5Network-devel >= 5.11.1
BuildRequires:	Qt5Test-devel
BuildRequires:	Qt5XmlPatterns-devel
BuildRequires:	cmake >= 2.8.12
BuildRequires:	gettext-devel
BuildRequires:	kf5-extra-cmake-modules >= %{kdeframever}
BuildRequires:	kf5-kcoreaddons-devel >= %{kdeframever}
BuildRequires:	kf5-ki18n-devel >= %{kdeframever}
BuildRequires:	kf5-kio-devel >= %{kdeframever}
BuildRequires:	ninja
BuildRequires:	qt5-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A DAV protocoll implemention with KJobs.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.


%prep
%setup -q -n %{kfname}-%{version}

%build
install -d build
cd build
%cmake \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DHTML_INSTALL_DIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	..
%ninja_build

%if %{with tests}
ctest
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%{_datadir}/qlogging-categories5/kdav.categories
%ghost %{_libdir}/libKF5DAV.so.5
%attr(755,root,root) %{_libdir}/libKF5DAV.so.5.*.*
%{_datadir}/qlogging-categories5/kdav.renamecategories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF5/KDAV
%{_libdir}/cmake/KF5DAV
%{_libdir}/libKF5DAV.so
%{_libdir}/qt5/mkspecs/modules/qt_KDAV.pri
