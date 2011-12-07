%define plugin_ver     0.3.0
%define linuxtools_rel R0_5_0
%define eclipse_base   %{_libdir}/eclipse
%define install_loc    %{_libdir}/eclipse/dropins/oprofile
%define qualifier      201003171651
%define ver_qual       %{plugin_ver}.%{qualifier}

# All arches line up between Eclipse and Linux kernel names except i386 -> x86
%ifarch %{ix86}
%define eclipse_arch    x86
%else
%define eclipse_arch   %{_arch}
%endif


Name:           eclipse-oprofile
Version:        0.5.0
Release:        1%{?dist}
Summary:        Eclipse plugin for OProfile integration

Group:          Development/Tools
License:        EPL
URL:            http://www.eclipse.org/linuxtools/projectPages/oprofile/
## sh %{name}-fetch-src.sh
Source0:        %{name}-fetched-src-%{linuxtools_rel}.tar.bz2
Source1:        %{name}-fetch-src.sh
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if 0%{?rhel} >= 6
ExclusiveArch: i686 x86_64
%endif

BuildRequires: eclipse-pde >= 1:3.5.0
BuildRequires: eclipse-cdt >= 6.0.0
BuildRequires: eclipse-linuxprofilingframework >= 0.1.0
BuildRequires: oprofile >= 0.9.3
BuildRequires: oprofile-devel >= 0.9.3
BuildRequires: binutils-devel >= 2.18.50.0.6
Requires: eclipse-platform >= 3.5.0
Requires: eclipse-cdt >= 6.0.0
Requires: eclipse-linuxprofilingframework >= 0.2.0
Requires: oprofile >= 0.9.3
Requires: usermode >= 1.98

%description
Eclipse plugins to integrate OProfile's profiling capabilities with the CDT.

%prep
%setup -q -c
#remove binaries
rm -f org.eclipse.linuxtools.oprofile.core.linux.*/os/linux/*/opxml

%build
#build binaries
cd org.eclipse.linuxtools.oprofile.core/natives/linux/opxml
make "CFLAGS=$RPM_OPT_FLAGS"

mv opxml \
  %{_builddir}/%{name}-%{version}/org.eclipse.linuxtools.oprofile.core.linux.%{eclipse_arch}/os/linux/%{eclipse_arch}

cd %{_builddir}/%{name}-%{version}

%{eclipse_base}/buildscripts/pdebuild -f org.eclipse.linuxtools.oprofile \
				      -d "cdt linuxprofilingframework" \
                                      -a "-DjavacSource=1.5 -DjavacTarget=1.5 -DforceContextQualifier=%{qualifier} -Dosgi.arch=%{eclipse_arch} -Dconfigs=linux,gtk,%{eclipse_arch}"

%install
%{__rm} -rf %{buildroot}
install -d -m 755 %{buildroot}%{install_loc}

%{__unzip} -q -d %{buildroot}%{install_loc} \
     build/rpmBuild/org.eclipse.linuxtools.oprofile.zip 

### install.sh stuff ###
%define corepath %{buildroot}%{install_loc}/eclipse/plugins/org.eclipse.linuxtools.oprofile.core_%{ver_qual}

#create opcontrol wrapper
ln -s ../../../../../../../../../../../usr/bin/consolehelper \
  %{corepath}/natives/linux/scripts/opcontrol

#install opcontrol wrapper permission files
install -d -m 755 %{buildroot}%{_sysconfdir}/security/console.apps
install -D -m 644 \
  org.eclipse.linuxtools.oprofile.core/natives/linux/scripts/opcontrol-wrapper.security \
  %{buildroot}%{_sysconfdir}/security/console.apps/opcontrol
install -d -m 755 %{buildroot}%{_sysconfdir}/pam.d
install -D -m 644 \
  org.eclipse.linuxtools.oprofile.core/natives/linux/scripts/opcontrol-wrapper.pamd \
  %{buildroot}%{_sysconfdir}/pam.d/opcontrol

#remove install/uninstall script (used in update site only)
rm -f %{corepath}/natives/linux/scripts/install.sh
rm -f %{corepath}/natives/linux/scripts/uninstall.sh

#remove opxml source (rpmlint warnings)
rm -rf %{corepath}/natives/linux/opxml
rm -f %{corepath}/natives/linux/scripts/.svnignore

#+x opxml
chmod +x \
  %{buildroot}%{install_loc}/eclipse/plugins/org.eclipse.linuxtools.oprofile.core.linux.%{eclipse_arch}_%{ver_qual}/os/linux/%{eclipse_arch}/opxml


%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{install_loc}
%doc org.eclipse.linuxtools.oprofile-feature/epl-v10.html
%{_sysconfdir}/security/console.apps/opcontrol
%{_sysconfdir}/pam.d/opcontrol

%changelog
* Tue Mar 23 2010 Jeff Johnston <jjohnstn@redhat.com> 0.5.0-1
- Resolves: #575107
- Rebase to Linux tools 0.5.0.

* Mon Dec 14 2009 Andrew Overholt <overholt@redhat.com> 0.4.0-2
- Only build on x86 and x86_64.

* Sat Dec 5 2009 Kent Sebastian <kksebasti@gmail.com> - 0.4.0-1
- 0.4.0 (long overdue)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 18 2009 Alexander Kurtakov <akurtako@redhat.com> 0.2.0-2
- Add -Dconfigs to fix compile.

* Wed May 13 2009 Kent Sebastian <ksebasti@redhat.com> 0.2.0-1
- 0.2.0

* Mon Mar 23 2009 Kent Sebastian <ksebasti@redhat.com> 0.1.0-4
- Rebuild for new pdebuild.

* Wed Mar 4 2009 Kent Sebastian <ksebasti@redhat.com> 0.1.0-3
- Refined patch for gcc build failures.

* Wed Mar 4 2009 Kent Sebastian <ksebasti@redhat.com> 0.1.0-2
- Add patch for gcc build failure.

* Thu Feb 12 2009 Kent Sebastian <ksebasti@redhat.com> 0.1.0-1
- Initial packaging.
