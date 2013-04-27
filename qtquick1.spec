%define _qtmodule_snapshot_version 5.0.2
Name:       qt5-qtquick1
Summary:    Qt Quick 1
Version:    5.0.2
Release:    1%{?dist}
Group:      Qt/Qt
License:    LGPLv2.1 with exception or GPLv3
URL:        http://qt.nokia.com
#Source0:    %{name}-%{version}.tar.xz
Source0:    qtquick1-opensource-src-%{_qtmodule_snapshot_version}.tar.xz
Patch1:     0001-Fix-build-in-dedicated-buildroot.patch
BuildRequires:  qt5-qtcore-devel
BuildRequires:  qt5-qtgui-devel
BuildRequires:  qt5-qtwidgets-devel
BuildRequires:  qt5-qtopengl-devel
BuildRequires:  qt5-qtdeclarative-devel
BuildRequires:  qt5-qtdeclarative-qtquick-devel
BuildRequires:  qt5-qtnetwork-devel
BuildRequires:  qt5-qtscript-devel
BuildRequires:  qt5-qtxmlpatterns-devel
BuildRequires:  fdupes

%description
Qt is a cross-platform application and UI framework. Using Qt, you can
write web-enabled applications once and deploy them across desktop,
mobile and embedded systems without rewriting the source code.
.
This package contains the Qt Quick 1 library


%package devel
Summary:        Qt Quick - development files
Group:          Qt/Qt
Requires:       %{name} = %{version}-%{release}

%description devel
Qt is a cross-platform application and UI framework. Using Qt, you can
write web-enabled applications once and deploy them across desktop,
mobile and embedded systems without rewriting the source code.
.
This package contains the Qt Quick 1 development files



#### Build section

%prep
%setup -q -n qtquick1-opensource-src-%{_qtmodule_snapshot_version}
%patch1 -p1

%build
export QTDIR=/usr/share/qt5
qmake -qt=5 
make %{?_smp_flags}

%install
rm -rf %{buildroot}
%qmake_install
# Fix wrong path in pkgconfig files
find %{buildroot}%{_libdir}/pkgconfig -type f -name '*.pc' \
-exec perl -pi -e "s, -L%{_builddir}/?\S+,,g" {} \;
# Fix wrong path in prl files
find %{buildroot}%{_libdir} -type f -name '*.prl' \
-exec sed -i -e "/^QMAKE_PRL_BUILD_DIR/d;s/\(QMAKE_PRL_LIBS =\).*/\1/" {} \;
# Remove unneeded .la files
rm -f %{buildroot}/%{_libdir}/*.la

# We don't need qt5/Qt/
rm -rf %{buildroot}/%{_includedir}/qt5/Qt


%fdupes %{buildroot}/%{_includedir}


#### Pre/Post section

%post
/sbin/ldconfig
%postun
/sbin/ldconfig

#### File section

%files
%defattr(-,root,root,-)
%{_qt5_bindir}/qmlviewer
%{_qt5_bindir}/qml1plugindump
%{_libdir}/libQt5Declarative.so.5
%{_libdir}/libQt5Declarative.so.5.*
%{_libdir}/qt5/plugins/qmltooling/libqmldbg*.so
%{_libdir}/qt5/imports/*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libQt5Declarative.so
%{_libdir}/libQt5Declarative.prl
%{_includedir}/qt5/QtDeclarative/
%{_libdir}/cmake/
%{_libdir}/pkgconfig/Qt5Declarative.pc
%{_datadir}/qt5/mkspecs/modules/qt_lib_declarative.pri



#### No changelog section, separate $pkg.changes contains the history

