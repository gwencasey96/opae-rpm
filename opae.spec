Summary:        Open Programmable Acceleration Engine (OPAE) SDK
Name:           opae
Version:        1.4.0
Release:        5%{?dist}
License:        BSD and MIT
ExclusiveArch:  x86_64
URL:            https://github.com/OPAE/%{name}-sdk
Source0:        https://github.com/OPAE/opae-sdk/releases/download/%{version}-1/%{name}-%{version}-1.tar.gz
Patch0:         0001-upstreaming-trim-down-to-the-files-for-1.4.1.patch 
Patch1:         0001-upstreaming-fix-rpmlint-errors.patch
Patch2:         0001-Trix-master-sa-1428.patch
Patch3:         0001-Check-if-.git-directory-exists-before-finding-the-gi.patch
Patch5:         0001-Work-around-a-problem-with-python-3.7.patch
Patch6:         0001-Change-to-explictly-to-python3.patch
Patch7:         fix-hwloc-20.patch
Patch8:         disable-fpgadiag.patch
Patch9:         python3-fpgabist.patch
Patch10:        0001-Add-INTEL_FPGA_API_VERSION-version-to-shared-objects.patch
Patch11:        0001-Fix-exec-stack-in-fpga_dma_vc_test.patch
Patch12:        move-modules-out-of-lib.patch
Patch13:        change-safestr-to-shared.patch
Patch14:        improve-library-link.patch

BuildRequires:  gcc, gcc-c++
BuildRequires:  cmake
BuildRequires:  python3-devel
BuildRequires:  json-c-devel
BuildRequires:  libuuid-devel
BuildRequires:  rpm-build
BuildRequires:  hwloc-devel
BuildRequires:  doxygen
BuildRequires:  systemd-rpm-macros
BuildRequires:  systemd

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
Requires:   libuuid-devel, %{name}%{?_isa} = %{version}-%{release}

%description devel
OPAE headers, tools, sample source, and documentation

%prep
%setup -q -n %{name}-%{version}-1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
# Remove hidden .clang-format
rm usr/libopaecxx/.clang-format
rm usr/libopae/.clang-format
rm usr/testing/.clang-format
rm usr/testing/xfpga/.clang-format
rm usr/common/include/opae/cxx/.clang-format
rm usr/tools/base/argsfilter/.clang-format
rm usr/pyopae/.clang-format

%build
mkdir -p _build
cd _build
%cmake ../usr -DBUILD_ASE=OFF -DOPAE_INSTALL_RPATH=OFF -DBUILD_LIBOPAE_PY=OFF
%make_build

%install
mkdir -p %{buildroot}%{_datadir}/opae
cp ./usr/RELEASE_NOTES.md %{buildroot}%{_datadir}/opae/RELEASE_NOTES.md
cp ./usr/LICENSE %{buildroot}%{_datadir}/opae/LICENSE
cp ./usr/COPYING %{buildroot}%{_datadir}/opae/COPYING

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

%make_install -C _build
mkdir -p %{buildroot}%{_sysconfdir}/systemd/system/

%post
mkdir -p %{_sysconfdir}/ld.so.conf.d
echo "" > %{_sysconfdir}/ld.so.conf.d/opae-c.conf

%files
%dir %{_datadir}/opae
%doc %{_datadir}/opae/RELEASE_NOTES.md
%license %{_datadir}/opae/LICENSE
%license %{_datadir}/opae/COPYING
%{_libdir}/libbitstream.so.%{version}
%{_libdir}/libbitstream.so.1
%{_libdir}/libbmc.so.%{version}
%{_libdir}/libbmc.so.1
%{_libdir}/libfpgad-api.so.%{version}
%{_libdir}/libfpgad-api.so.1
%{_libdir}/libhssi-io.so.%{version}
%{_libdir}/libhssi-io.so.1
%{_libdir}/libopae-c.so.%{version}
%{_libdir}/libopae-c.so.1
%{_libdir}/libopae-cxx-core.so.%{version}
%{_libdir}/libopae-cxx-core.so.1
%{_libdir}/libopae-c++-utils.so.%{version}
%{_libdir}/libopae-c++-utils.so.1
%{_libdir}/libsafestr.so.%{version}
%{_libdir}/libsafestr.so.1

%post devel
%systemd_post fpgad.service

%preun devel
%systemd_preun fpgad.service

%files devel
%dir %{_includedir}/opae
%dir %{_includedir}/safe_string
%dir %{_sysconfdir}/opae
%dir %{_libdir}/opae
%dir %{_usr}/src/opae
%dir %{_usr}/src/opae/cmake
%dir %{_usr}/src/opae/cmake/modules
%dir %{_usr}/src/opae/samples
%config(noreplace) %{_sysconfdir}/opae/fpgad.cfg*
%config(noreplace) %{_sysconfdir}/sysconfig/fpgad.conf*
%{_bindir}/bist
%{_bindir}/bist_app
%{_bindir}/bist_app.py
%{_bindir}/bist_common.py
%{_bindir}/bist_dma.py
%{_bindir}/bist_def.py
%{_bindir}/bist_nlb3.py
%{_bindir}/bist_nlb0.py
%{_bindir}/coreidle
%{_bindir}/fpgaconf*
%{_bindir}/fpgainfo*
%{_bindir}/fpgametrics*
%{_bindir}/fpgad*
%{_bindir}/fpga_dma_vc_test
%{_bindir}/fpgabist
%{_bindir}/hello_fpga
%{_bindir}/hssi_config
%{_bindir}/hssi_loopback
%{_bindir}/mmlink
%{_bindir}/ras
%{_bindir}/userclk
%{_includedir}/opae/*
%{_includedir}/safe_string/safe_string.h
%{_libdir}/libbitstream.so
%{_libdir}/libbmc.so
%{_libdir}/libfpgad-api.so
%{_libdir}/libhssi-io.so
%{_libdir}/libopae-c.so
%{_libdir}/libopae-cxx-core.so
%{_libdir}/libopae-c++-utils.so
%{_libdir}/libsafestr.so
%{_libdir}/opae/libboard_rc.so*
%{_libdir}/opae/libboard_vc.so*
%{_libdir}/opae/libfpgad-vc.so*
%{_libdir}/opae/libfpgad-xfpga.so*
%{_libdir}/opae/libmodbmc.so*
%{_libdir}/opae/libxfpga.so*
%{_usr}/src/opae/samples/hello_fpga.c
%{_usr}/src/opae/samples/hello_events.c
%{_usr}/src/opae/samples/object_api.c
%{_usr}/src/opae/cmake/modules/*
%{_unitdir}/fpgad.service

%changelog
* Fri Mar 6 2020 Tom Rix <trix@redhat.com> 1.4.0-5
- Use make_install macro
- Use license tag correctly

* Tue Mar 3 2020 Tom Rix <trix@redhat.com> 1.4.0-4
- Add libraries to link of libopae-cxx-core libopae-c++-utils
- Remove unneeded build flag _smp_mflags

* Thu Feb 27 2020 Tom Rix <trix@redhat.com> 1.4.0-3
- Remove ldconfig from post and postun
- Append dist tag to release tag
- Change libsafestr to shared library
- Set license tag to location of license files
- Remove phython3-sphnix build dependency.
- Consolidate samples,tools,tools-extra pkgs into devel
- Improve pkg created dir specification
- Set x86_64 as ExclusiveArch
- Change to runtime to implicit dependency on build *-devel
- Remove preun rm of opae-c.conf
- Use systemd rpm macros
- Add _smp_mflags to build
- Use unitdir for fpgad.service path
- Distribute the license and copying files

* Mon Feb 24 2020 Tom Rix <trix@redhat.com> 1.4.0-2
- Change to python3
- Remove release tag from upstream Source0 definition.
- Improve requires tag for subpackages
- Remove explicit root owner
- Remove vendor tag
- Remove group tag
- Remove clean section

* Tue Dec 17 2019 Korde Nakul <nakul.korde@intel.com> 1.4.0-1
- Added support to FPGA Linux kernel Device Feature List (DFL) driver patch set2.
- Increased test cases and test coverage
- Various bug fixes
- Various compiler warning fixes
- Various memory leak fixes
- Various Static code scan bug fixes
- Added new FPGA MMIO API to write 512 bits
