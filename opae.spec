Summary:        Open Programmable Acceleration Engine (OPAE) SDK
Name:           opae
Version:        1.4.0
Release:        1
License:        BSD
Group:          Development/Libraries
Vendor:         Intel Corporation
Requires:       uuid, json-c, python
URL:            https://github.com/OPAE/%{name}-sdk
Source0:        https://github.com/OPAE/opae-sdk/releases/download/%{version}-%{release}/%{name}-%{version}-%{release}.tar.gz
Patch0:         0001-Trix-master-sa-1428.patch
Patch1:         0001-Check-if-.git-directory-exists-before-finding-the-gi.patch
Patch2:         0001-Add-cmake-option-BUILD_TOOLS_EXTRA.patch
Patch3:         0001-Work-around-a-problem-with-python-3.7.patch
Patch4:         0001-Change-to-explictly-to-python3.patch

BuildRequires:  gcc, gcc-c++
BuildRequires:  cmake
BuildRequires:  python-devel
BuildRequires:  json-c-devel
BuildRequires:  libuuid-devel
BuildRequires:  rpm-build
BuildRequires:  hwloc-devel
BuildRequires:  python-sphinx
BuildRequires:  doxygen

%description
Open Programmable Acceleration Engine (OPAE) is a software framework
for managing and accessing programmable accelerators (FPGAs).
Its main parts are:

* OPAE Software Development Kit (OPAE SDK) (this package)
* OPAE Linux driver for Intel(R) Xeon(R) CPU with
  Integrated FPGAs and Intel(R) PAC with Arria(R) 10 GX FPGA
* Basic Building Block (BBB) library for accelerating AFU

OPAE SDK is a collection of libraries and tools to facilitate the
development of software applications and accelerators using OPAE.
It provides a library implementing the OPAE C API for presenting a
streamlined and easy-to-use interface for software applications to
discover, access, and manage FPGA devices and accelerators using
the OPAE software stack.

%package devel
Summary:    OPAE headers, sample source, and documentation
Group:      Development/Libraries
Requires:   libuuid-devel

%description devel
OPAE headers, sample source, and documentation


%package tools
Summary:    OPAE base tools binaries
Group:      Development/Libraries

%description tools
OPAE Base Tools binaries

%post tools
ldconfig

%postun tools
ldconfig

%package samples
Summary:    OPAE samples apps
Group:      Development/Libraries

%description samples
OPAE samples


%prep
%setup -q -n %{name}-%{version}-%{release}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
mkdir -p _build
cd _build
%cmake ../usr -DBUILD_ASE=OFF -DOPAE_INSTALL_RPATH=OFF -DBUILD_LIBOPAE_PY=OFF -DBUILD_TOOLS_EXTRA=OFF
make -j

%install
mkdir -p %{buildroot}%{_datadir}/opae
cp ./usr/RELEASE_NOTES.md %{buildroot}%{_datadir}/opae/RELEASE_NOTES.md

mkdir -p %{buildroot}%{_usr}/src/opae/cmake/modules
for s in FindDBus.cmake \
         FindGLIB.cmake \
         FindOPAE.cmake \
         FindQuartus.cmake \
         FindQuesta.cmake \
         FindRT.cmake \
         FindUUID.cmake \
         FindVerilator.cmake \
         Findjson-c.cmake \
         cmake_useful.cmake \
         compiler_config.cmake \
         libraries_config.cmake
do
  cp "usr/cmake/modules/${s}" %{buildroot}%{_usr}/src/opae/cmake/modules
done

mkdir -p %{buildroot}%{_usr}/src/opae/samples
cp usr/samples/hello_fpga.c %{buildroot}%{_usr}/src/opae/samples/
cp usr/samples/hello_events.c %{buildroot}%{_usr}/src/opae/samples/
cp usr/samples/object_api.c %{buildroot}%{_usr}/src/opae/samples/

cd _build
make DESTDIR=%{buildroot} install
mkdir -p %{buildroot}%{_sysconfdir}/systemd/system/
mv %{buildroot}%{_usr}/lib/systemd/system/fpgad.service %{buildroot}%{_sysconfdir}/systemd/system/fpgad.service

%clean

%post
mkdir -p %{_sysconfdir}/ld.so.conf.d
echo "" > %{_sysconfdir}/ld.so.conf.d/opae-c.conf
ldconfig

%postun
ldconfig

%pre

%preun
rm -f -- %{_sysconfdir}/ld.so.conf.d/opae-c.conf 

%files
%defattr(-,root,root,-)
%dir %{_datadir}/opae
%doc %{_datadir}/opae/RELEASE_NOTES.md
%{_libdir}/libopae-c.so*
%{_libdir}/libopae-c-ase.so*
%{_libdir}/libopae-cxx-core.so*
%{_libdir}/libxfpga.so*
%{_libdir}/libbmc.so*
%{_libdir}/libmodbmc.so*
%{_libdir}/libbitstream.so*
%{_libdir}/libboard_rc.so*
%{_libdir}/libboard_vc.so*

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/opae
%{_includedir}/opae/*
%dir %{_includedir}/safe_string
%{_includedir}/safe_string/safe_string.h
%{_libdir}/libsafestr.a
%dir %{_usr}/src/opae
%{_usr}/src/opae/samples/hello_fpga.c
%{_usr}/src/opae/samples/hello_events.c
%{_usr}/src/opae/samples/object_api.c
%{_usr}/src/opae/cmake/modules/*
%dir %{_datadir}/opae/platform
%dir %{_datadir}/opae/platform/afu_top_ifc_db
%{_datadir}/opae/platform/afu_top_ifc_db/*
%dir %{_datadir}/opae/platform/platform_db
%{_datadir}/opae/platform/platform_db/*
%dir %{_datadir}/opae/platform/platform_if
%{_datadir}/opae/platform/platform_if/*
%dir %{_datadir}/opae/platform/platform_if/par
%{_datadir}/opae/platform/platform_if/par/*

%files tools
%defattr(-,root,root,-)
%{_bindir}/fpgaconf*
%{_bindir}/fpgainfo*
%{_bindir}/fpgametrics*
%{_bindir}/fpgad*
%{_bindir}/fpgaport*
%config(noreplace) %{_sysconfdir}/opae/fpgad.cfg*
%config(noreplace) %{_sysconfdir}/sysconfig/fpgad.conf*
%config(noreplace) %{_sysconfdir}/systemd/system/fpgad.service
%{_libdir}/libfpgad-api.so*
%{_libdir}/libfpgad-xfpga.so*
%{_libdir}/libfpgad-vc.so*

%files samples
%defattr(-,root,root,-)
%{_bindir}/hello_fpga


%changelog
* Tue Dec 17 2019 Korde Nakul <nakul.korde@intel.com> 1.4.0-1
- Added support to FPGA Linux kernel Device Feature List (DFL) driver patch set2.
- Increased test cases and test coverage
- Various bug fixes
- Various compiler warning fixes
- Various memory leak fixes
- Various Static code scan bug fixes
- Added new FPGA MMIO API to write 512 bits
