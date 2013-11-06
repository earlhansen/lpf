%global commit  84c3544573a328d43c4e971bb8c122a10073252a
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           lpf
Version:        0
Release:        5.%{shortcommit}%{?dist}
Summary:        Local package factory - build non-redistributable rpms

                # Icon from iconarchive.com
License:        MIT
URL:            https://github.com/leamas/lpf
Group:          Development/Tools
Source0:        %{url}/archive/%{commit}/lpf-%{shortcommit}.tar.gz
BuildArch:      noarch

BuildRequires:  desktop-file-utils
Buildrequires:  python2-devel
Requires:       hicolor-icon-theme
Requires:       rpmdevtools
Requires:       rpm-build
Requires:       sudo
Requires:       sudo
Requires:       yum-utils
Requires(pre):  shadow-utils


%description
lpf (Local Package Factory) is designed to handle two separate
problems:
 - Packages built from sources which does not allow redistribution.
 - Packages requiring user to accept EULA-like terms.

It works by downloading sources, possibly requiring a user to accept
license terms and then building and installing rpm package(s) locally.
Besides being interactive the operation is similar to akmod and dkms


%prep
%setup -qn lpf-%{commit}
rm -rf examples


%build


%install
make DESTDIR=%{buildroot} install
desktop-file-validate %{buildroot}%{_datadir}/applications/lpf.desktop


%pre
getent group pkg-build >/dev/null || groupadd -r pkg-build
getent passwd pkg-build >/dev/null || \
    useradd -r -g pkg-build -d /var/lib/lpf -s /sbin/nologin \
        -c "lpf local package build user" pkg-build
exit 0

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/lpf scan || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%doc README.md LICENSE
%{_bindir}/lpf
%{_datadir}/lpf
%{_datadir}/applications/lpf.desktop
%{_datadir}/icons/hicolor/*/apps/lpf.png
%{_datadir}/man/man1/lpf.*
%{_libexecdir}/lpf-kill-pgroup
# fedpkg import does not accept /etc ATM.
%config(noreplace) %{_sysconfdir}/sudoers.d/pkg-build
%attr(2775, pkg-build, pkg-build)/var/lib/lpf


%changelog
* Sat Oct 26 2013 Alec Leamas <leamas.alec@gmail.com> - 0-5.84c3544
- Allow spec file to be named .spec.in

* Fri Oct 25 2013 Alec Leamas <leamas.alec@gmail.com> - 0-4.3051236
- Updating examples

* Sun Jun 23 2013 Alec Leamas <leamas@nowhere.net> - 0-3.fe3defcf9
- Removed examples, added lpf spec tamplate.
- Add manpage

* Thu Jun 13 2013 Alec Leamas <leamas@nowhere.net> - 0-3.fe3defcf9
- Added BR: python2-devel
- Simplified Source0 (https://fedorahosted.org/fpc/ticket/284)
- Using 2775 instead of 775 perms (https://fedorahosted.org/fpc/ticket/286)

* Tue Jun 11 2013 Alec Leamas <leamas@nowhere.net> - 0-1.c4bc5a2
- Upstream Makefile added, clean up installation

* Mon Jun 10 2013 Alec Leamas <leamas@nowhere.net> - 0-1.d961366
- Initial release
