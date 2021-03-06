# %%global will not work here, lazy evaluation needed.
%define         target_pkg %(t=%{name}; echo ${t#lpf-})

Name:           lpf-msttcore-fonts
Version:        2.2
Release:        1%{?dist}
Summary:        Bootstrap package building msttcore-fonts using lpf

License:        MIT
URL:            https://github.com/leamas/lpf
Group:          Development/Tools
BuildArch:      noarch
Source0:        msttcore-fonts.spec.in
Source1:        License.txt
Source2:        msttcore-fonts-fontconfig.conf

BuildRequires:  desktop-file-utils
BuildRequires:  lpf
Requires:       lpf


%description
Bootstrap package allowing the lpf system to build the
msttcore-fonts non-redistributable package.


%prep
%setup -cT


%build


%install
# lpf-setup-pkg [eula] <topdir> <specfile> [sources...]
/usr/share/lpf/scripts/lpf-setup-pkg \
    %{SOURCE1} %{buildroot} %{SOURCE0} %{SOURCE2}
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%post
lpf scan %{target_pkg} &>/dev/null || :

%postun
if [ "$1" = '0' ]; then
    /usr/share/lpf/scripts/lpf-pkg-postun %{target_pkg}
fi

%lpf_triggerpostun


%files
%{_datadir}/applications/%{name}.desktop
%{_datadir}/lpf/packages/%{target_pkg}
%attr(775,pkg-build,pkg-build) /var/lib/lpf/packages/%{target_pkg}


%changelog
* Sun May 05 2013 Alec Leamas <leamas@nowhere.net> - 0.9.0.133.gd18ed58.259-2
- Initial release
