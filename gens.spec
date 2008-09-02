Summary: Gens is a win32/unix Sega Genesis / Sega CD / Sega 32X emulator
Name: gens
Version: 2.15.4
Release: 1%{?dist}
License: GPLv2
Group: Applications/Emulators
URL: http://www.gens.ws/
Source0:  http://dl.sf.net/%{name}/%{name}-%{version}.tar.gz
Source1: gens.desktop
Patch0: gens-2.15.2-romsdir.patch
Patch1: gens-2.15.2-execstack.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 
# This is to build only for i386 on plague
#ExclusiveArch: %{ix86}
ExclusiveArch: i386
BuildRequires: gtk2-devel >= 2.4.0
BuildRequires: SDL-devel >= 1.1.3
BuildRequires: libglade2-devel
BuildRequires: nasm >= 0.98.37
BuildRequires: ImageMagick
BuildRequires: desktop-file-utils
Requires: hicolor-icon-theme
 
%description
Gens is a GPL emulator for the genesis, ported from win32
to BeOS and linux. It was the fastest on win32, and is pretty fast on linux.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

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
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
    %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
    %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%files
%defattr(-,root,root)
%{_bindir}/gens
%{_datadir}/gens
%{_datadir}/applications/dribble-%{name}.desktop
%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%doc AUTHORS BUGS COPYING gens.txt history.txt README

%changelog
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

