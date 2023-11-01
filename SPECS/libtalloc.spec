%if 0%{?fedora} || 0%{?rhel} > 7
%bcond_without python3
%else
%bcond_with python3
%endif

Name: libtalloc
Version: 2.3.4
Release: 1%{?dist}
Summary: The talloc library
License: LGPLv3+
URL: https://talloc.samba.org/

Source0: https://www.samba.org/ftp/talloc/talloc-%{version}.tar.gz
Source1: https://www.samba.org/ftp/talloc/talloc-%{version}.tar.asc
Source2: https://download.samba.org/pub/samba/samba-pubkey.asc#/talloc.keyring

# Patches
Patch0001: 0003-wafsamba-Fix-few-SyntaxWarnings-caused-by-regular-ex.patch

BuildRequires: make
BuildRequires: gcc
BuildRequires: libxslt
BuildRequires: docbook-style-xsl
%if %{with python3}
BuildRequires: python3-devel
%endif
BuildRequires: doxygen
BuildRequires: gnupg2

Provides: bundled(libreplace)
Obsoletes: python2-talloc < 2.2.0-1
Obsoletes: python2-talloc-devel < 2.2.0-1

%description
A library that implements a hierarchical allocator with destructors.

%package devel
Summary: Developer tools for the Talloc library
Requires: libtalloc = %{version}-%{release}

%description devel
Header files needed to develop programs that link against the Talloc library.

%if %{with python3}
%package -n python3-talloc
Summary: Python bindings for the Talloc library
Requires: libtalloc = %{version}-%{release}
%{?python_provide:%python_provide python3-talloc}

%description -n python3-talloc
Python 3 libraries for creating bindings using talloc

%package -n python3-talloc-devel
Summary: Development libraries for python3-talloc
Requires: python3-talloc = %{version}-%{release}
%{?python_provide:%python_provide python3-talloc-devel}

%description -n python3-talloc-devel
Development libraries for python3-talloc
%endif

%prep
%autosetup -n talloc-%{version} -p1

%build
zcat %{SOURCE0} | gpgv2 --quiet --keyring %{SOURCE2} %{SOURCE1} -
# workaround for https://bugzilla.redhat.com/show_bug.cgi?id=1217376
export python_LDFLAGS=""

%configure --disable-rpath \
           --disable-rpath-install \
           --bundled-libraries=NONE \
           --builtin-libraries=replace \
           --disable-silent-rules

%make_build
doxygen doxy.config

%check
%make_build check

%install
%make_install

# Install API docs
cp -a doc/man/man3 %{buildroot}%{_mandir}

%files
%{_libdir}/libtalloc.so.*

%files devel
%{_includedir}/talloc.h
%{_libdir}/libtalloc.so
%{_libdir}/pkgconfig/talloc.pc
%{_mandir}/man3/talloc*.3*
%{_mandir}/man3/libtalloc*.3*

%if %{with python3}
%files -n python3-talloc
%{_libdir}/libpytalloc-util.cpython*.so.*
%{python3_sitearch}/talloc.cpython*.so

%files -n python3-talloc-devel
%{_includedir}/pytalloc.h
%{_libdir}/pkgconfig/pytalloc-util.cpython-*.pc
%{_libdir}/libpytalloc-util.cpython*.so
%endif

%ldconfig_scriptlets

%if %{with python3}
%ldconfig_scriptlets -n python3-talloc
%endif

%changelog
* Mon Oct 24 2022 Andreas Schneider <asn@redhat.com> - 2.3.4-1
- resolves: rhbz#2132056 - Update to version 2.3.4

* Thu Aug 11 2022 Andreas Schneider <asn@redhat.com> - 2.3.3-2
- resolves: rhbz#2100088 - Rebuild to include python3-talloc-devel in CRB

* Thu Nov 25 2021 Pavel Filipenský <pfilipen@redhat.com> - 2.3.3-1
- resolves: rhbz#2013601 - Update to version 2.3.3

* Tue May 11 2021 Andreas Schneider <asn@redhat.com> - 2.3.2-1
- resolves: rhbz#1945014 - Update to version 2.3.2

* Tue Jun 2 2020 Isaac Boukris <iboukris@redhat.com> - 2.3.1-2
- resolves: rhbz#1817560 - Update to version 2.3.1

* Mon Nov 25 2019 Isaac Boukris <iboukris@redhat.com> - 2.2.0-7
- related: rhbz#1754417 - Fix PY3 symbol names

* Wed Nov 20 2019 Isaac Boukris <iboukris@redhat.com> - 2.2.0-1
- Resolves: rhbz#1754417 - Rebase talloc to version 2.2.0 for samba

* Tue Apr 30 2019 Jakub Hrozek <jhrozek@redhat.com> - 2.1.16-3
- Also obsolete python2-libtalloc-debuginfo
- Resolves: rhbz#1567136 - libtalloc: Drop Python 2 subpackage from RHEL 8

* Tue Apr 30 2019 Jakub Hrozek <jhrozek@redhat.com> - 2.1.16-2
- Remove python2 libraries on upgrade
- Resolves: rhbz#1567136 - libtalloc: Drop Python 2 subpackage from RHEL 8

* Wed Apr  3 2019 Jakub Hrozek <jhrozek@redhat.com> - 2.1.16-1
- Resolves: rhbz#1684577 - Rebase libtalloc to version 2.1.16 for Samba
- Resolves: rhbz#1597315 - libtalloc uses Python 2 to build
- Resolves: rhbz#1567136 - libtalloc: Drop Python 2 subpackage from RHEL 8

* Tue Sep 18 2018 Jakub Hrozek <jhrozek@redhat.com> - 2.1.14-3
- Resolves: rhbz#1624136 - Review annocheck distro flag failures in libtalloc

* Thu Jul 12 2018 Jakub Hrozek <jhrozek@redhat.com> - 2.1.14-2
- Use pathfix.py to select python2 instead of python

* Thu Jul 12 2018 Jakub Hrozek <jhrozek@redhat.com> - 2.1.14-1
- New upstream release - 2.1.14
- Patch the waf script to explicitly call python2 as "env python" doesn't
  yield py2 anymore

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.1.13-2
- Rebuilt for Python 3.7

* Fri Apr 06 2018 Lukas Slebodnik <lslebodn@fedoraproject.org> - 2.1.13-1
- rhbz#1564323 New upstream release - 2.1.13

* Thu Mar 22 2018 Lukas Slebodnik <lslebodn@fedoraproject.org> - 2.1.12-1
- rhbz#1559378 New upstream release - 2.1.12

* Fri Mar 02 2018 Lukas Slebodnik <lslebodn@fedoraproject.org> - 2.1.11-6
- Disable link time optimisation for python3 related libs
- Workaround for rhbz#1548823

* Mon Feb 26 2018 Lukas Slebodnik <lslebodn@fedoraproject.org> - 2.1.11-5
- Add gcc to Buildroot
- https://fedoraproject.org/wiki/Changes/Remove_GCC_from_BuildRoot

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.1.11-3
- Switch to %%ldconfig_scriptlets

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 2.1.11-2
- Rebuilt for switch to libxcrypt

* Sat Jan 13 2018 Lukas Slebodnik <lslebodn@fedoraproject.org> - 2.1.11-1
- rhbz#1534136 New upstream release - 2.1.11

* Wed Nov 29 2017 Merlin Mathesius <mmathesi@redhat.com> - 2.1.10-5
- Cleanup spec file conditionals

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 24 2017 Lukas Slebodnik  <lslebodn@redhat.com> - 2.1.10-2
- fix location of pkgconfig files for libpytalloc*

* Mon Jul 24 2017 Lukas Slebodnik  <lslebodn@redhat.com> - 2.1.10-1
- rhbz#1473997 New upstream release - 2.1.10
- enable unit tests

* Thu Jul 06 2017 Andreas Schneider <asn@redhat.com> - 2.1.9-2
- Install pytalloc-util for python3 as well

* Tue Feb 28 2017 Lukas Slebodnik  <lslebodn@redhat.com> - 2.1.9-1
- rhbz#1427352 New upstream release - 2.1.9
- rhbz#1401225 - Rename python packages to match packaging guidelines
  https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2.1.8-2
- Rebuild for Python 3.6

* Thu Jul 28 2016 Jakub Hrozek <jhrozek@redhat.com> - 2.1.8-1
- New upstream release - 2.1.8

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.7-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri May  6 2016 Jakub Hrozek <jhrozek@redhat.com> - 2.1.7-1
- New upstream release - 2.1.7
- Resolves: rhbz#1333790 - libtalloc-2.1.7 is available

* Wed Mar  9 2016 Jakub Hrozek <jhrozek@redhat.com> - 2.1.6-1
- New upstream release - 2.1.6

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov 11 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Nov 11 2015 Jakub Hrozek <jhrozek@redhat.com> - 2.1.5-1
- New upstream release - 2.1.5

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Oct 14 2015 Jakub Hrozek <jhrozek@redhat.com> - 2.1.4-1
- New upstream release - 2.1.4

* Wed Jul 22 2015 Jakub Hrozek <jhrozek@redhat.com> - 2.1.3-1
- New upstream release - 2.1.3
- Resolves: rhbz#1241928 - Switch libtalloc to use python3
- Rename pytalloc to python-talloc (Miro Hrončok <mhroncok@redhat.com>)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Mar 13 2015 Jakub Hrozek <jhrozek@redhat.com> - 2.1.2-1
- New upstream release - 2.1.2

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Jakub Hrozek <jhrozek@redhat.com> - 2.1.1-1
- New upstream release

* Sun Dec 15 2013 Jakub Hrozek <jhrozek@redhat.com> - 2.1.0-3
- Bump NVR in order to tag a build

* Tue Sep 10 2013 Jakub Hrozek <jhrozek@redhat.com> - 2.1.0-2
- New upstream release

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Dec 01 2012 Jakub Hrozek <jhrozek@redhat.com> - 2.0.8-1
- New upstream release

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 01 2011 Stephen Gallagher <sgallagh@redhat.com> - 2.0.7-3
- Add patch to ignore --disable-silent-rules
- Package API docs into libtalloc-devel

* Wed Nov 23 2011 Stephen Gallagher <sgallagh@redhat.com> - 2.0.7-2
- Add explicit mention of the bundled libreplace
- https://fedorahosted.org/fpc/ticket/120

* Fri Nov 04 2011 Stephen Gallagher <sgallagh@redhat.com> - 2.0.7-1
- New upstream release
- Required for new Samba 4 alpha builds

* Mon Aug 08 2011 Simo Sorce <ssorce@redhat.com> - 2.0.6-1
- New upstream release
- Fixes various bugs with talloc_free_children and freeing complex
  hierarchies with many siblinbgs.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 14 2011 Stephen Gallagher <sgallagh@redhat.com> - 2.0.5-7
- Let rpmbuild strip binaries, make build more verbose.
- Resolves rhbz#669477 - libtalloc 2.0.5-6 binaries not stripped,
-                        empty -debuginfo
- Original patch by Ville SkyttÃ¤ <ville.skytta@iki.fi>

* Wed Jan 12 2011 Stephen Gallagher <sgallagh@redhat.com> - 2.0.5-6
- Install python bindings in the correct location

* Tue Jan 11 2011 Stephen Gallagher <sgallagh@redhat.com> - 2.0.5-5
- Run ldconfig on pytalloc

* Tue Jan 11 2011 Stephen Gallagher <sgallagh@redhat.com> - 2.0.5-4
- Fix build failure on 32-bit platforms

* Tue Jan 11 2011 Stephen Gallagher <sgallagh@redhat.com> - 2.0.5-3
- New version from upstream
- Add support for pytalloc
- Convert to new WAF build-system

* Tue Dec 15 2009 Simo Sorce <ssorce@redhat.com> - 2.0.1-1
- New version from upstream
- Also stop building the compat lib, it is not necessary anymore

* Tue Sep  8 2009 Simo Sorce <ssorce@redhat.com> - 2.0.0-0
- New version from upstream.
- Build also sover 1 compat library to ease packages migration

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 17 2009 Simo Sorce <ssorce@redhat.com> - 1.3.1-1
- Original tarballs had a screw-up, rebuild with new fixed tarballs from
  upstream.

* Tue Jun 16 2009 Simo Sorce <ssorce@redhat.com> - 1.3.1-0
- New Upstream release.

* Wed May 6 2009 Simo Sorce <ssorce@redhat.com> - 1.3.0-0
- First public independent release from upstream
