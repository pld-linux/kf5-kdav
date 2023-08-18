#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeframever	5.109
%define		qtver		5.15.2
%define		kfname		kdav
Summary:	Kdav
Name:		kf5-%{kfname}
Version:	5.109.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	d4e4e96920394601cf599ed8e36bd635
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5Gui-devel
BuildRequires:	Qt5Network-devel >= 5.11.1
BuildRequires:	Qt5Test-devel
BuildRequires:	Qt5XmlPatterns-devel
BuildRequires:	cmake >= 3.16
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
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DHTML_INSTALL_DIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
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
