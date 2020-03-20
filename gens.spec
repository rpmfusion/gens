%define _legacy_common_support 1

Summary: A Sega Genesis / Sega CD / Sega 32X emulator
Name: gens
Version: 2.15.5
Release: 16%{?dist}
License: GPLv2
Group: Applications/Emulators
URL: http://www.gens.me/
Source0: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1: gens.desktop
# Gentoo
# https://bugs.gentoo.org/show_bug.cgi?id=153593
Patch0: gens-2.15.2-romsdir.patch
# https://bugs.gentoo.org/show_bug.cgi?id=340665
# https://sourceforge.net/tracker/?func=detail&aid=3097146&group_id=73619&atid=538344
Patch1: gens-2.15.5-ovflfix.patch
# https://bugs.gentoo.org/show_bug.cgi?id=247350
Patch2: gens-2.15.5-as-needed.patch
# Andrea Musuruane
Patch3: gens-2.15.2-execstack.patch
# GetDeb
# https://bugs.launchpad.net/getdeb.net/+bug/561819
Patch4: gens-2.15.5-spelling.patch
# Mandriva
Patch5: gens-2.15.5-strings.patch
# OpenSUSE
Patch6: gens-2.15.5-rpmlint.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 
# This is to build only for ix86 on plague
ExclusiveArch: i686

BuildRequires: gcc-c++
BuildRequires: gtk2-devel >= 2.4.0
BuildRequires: SDL-devel >= 1.1.3
BuildRequires: libglade2-devel
BuildRequires: nasm >= 0.98.37
BuildRequires: ImageMagick
BuildRequires: desktop-file-utils
Requires: hicolor-icon-theme
 
%description
Gens is a GPL emulator for the genesis, ported from win32 to BeOS and Linux. 
It was the fastest on win32, and is pretty fast on Linux.

%prep
%setup -q
%patch0 -p1
%patch1 -p0
%patch2 -p0
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p0

# Fix line encoding
sed -i 's/\r//' gens.txt
sed -i 's/\r//' history.txt

# Fix char encoding
iconv --from=ISO-8859-1 --to=UTF-8 BUGS > BUGS.utf8
mv BUGS.utf8 BUGS
iconv --from=ISO-8859-1 --to=UTF-8 gens.txt > gens.txt.utf8
mv gens.txt.utf8 gens.txt

%build
%configure
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# install desktop file and icons
mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install --vendor dribble        \
  --dir %{buildroot}%{_datadir}/applications \
  %{SOURCE1}

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/{16x16,32x32}/apps
convert -delete 1 pixmaps/Gens2.ico \
  %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
convert -delete 0 pixmaps/Gens2.ico \
  %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png

%clean
rm -rf %{buildroot}

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%defattr(-,root,root)
%{_bindir}/gens
%{_datadir}/gens
%{_datadir}/applications/dribble-%{name}.desktop
%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%doc AUTHORS BUGS COPYING gens.txt history.txt README

%changelog
* Fri Mar 20 2020 Andrea Musuruane <musuruan@gmail.com> - 2.15.5-16
- Fix FTBFS

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.15.5-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Aug 10 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.15.5-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 05 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.15.5-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Aug 19 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.15.5-12
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Fri Jul 27 2018 RPM Fusion Release Engineering <sergio@serjux.com> - 2.15.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Mar 02 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 2.15.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 2.15.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Mar 25 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 2.15.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 2.15.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Mar 12 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.15.5-6
- https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Mar 18 2012 Andrea Musuruane <musuruan@gmail.com> 2.15.5-5
- added patches from various distributions
- updated icon cache scriptlet according to packaging guidelines
- fixed summary not to repeat package name
- fixed spelling in summary

* Thu Feb 09 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.15.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 11 2010 Andrea Musuruane <musuruan@gmail.com> 2.15.5-3
- updated upstream URL
- fixed Source0 according to packaging guidelines

* Sat Mar 28 2009 Andrea Musuruane <musuruan@gmail.com> 2.15.5-2
- fixed ExclusiveArch for F11

* Sun Oct 05 2008 Andrea Musuruane <musuruan@gmail.com> 2.15.5-1
- updated to upstream 2.15.5

* Tue Sep 02 2008 Andrea Musuruane <musuruan@gmail.com> 2.15.4-1
- updated to upstream 2.15.4

* Sun Aug 23 2008 Andrea Musuruane <musuruan@gmail.com> 2.15.3-1
- updated to upstream 2.15.3

* Sat Aug 09 2008 Andrea Musuruane <musuruan@gmail.com> 2.15.2-1
- updated to upstream 2.15.2
- added a patch not to require an executable stack
- removed no longer needed patches
- added openGL support in BR
- used a workaround to build only for i386 on plague

* Fri Mar 21 2008 Andrea Musuruane <musuruan@gmail.com> 2.12-0.4.rc3
- changed license due to new guidelines
- updated URL tag
- added a patch from Daniel Schneidereit to fix "Open Rom" always starting in 
  ~/.gens (Gentoo #153593)
- removed %%{?dist} tag from changelog
- updated icon cache scriptlets to be compliant to new guidelines
- fixed char encodings in docs
- desktop file is no longer built in the spec file
- removed icon extension from desktop file to match Icon Theme Specification

* Sat Mar 17 2007 Andrea Musuruane <musuruan@gmail.com> 2.12-0.3.rc3
- dropped --add-category X-Fedora from desktop-file-install
- changed .desktop category to Game;Emulator;

* Sat Jan 06 2007 Andrea Musuruane <musuruan@gmail.com> 2.12-0.2.rc3
- fixed upstream source link and package
- changed .desktop category to "Application;Emulator;"

* Sun Nov 26 2006 Andrea Musuruane <musuruan@gmail.com> 2.12-0.1.rc3%
- first release 
- used a patch from Avuton Olrich to fix gcc4 compile patch (Gentoo #119024)
- used a patch from Dieter Baron to fix analog joysticks (SF #981963)

