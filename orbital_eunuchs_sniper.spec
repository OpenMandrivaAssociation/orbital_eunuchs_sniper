%define	name	orbital_eunuchs_sniper
%define	version	1.28
%define rel	12
%define	Summary	Orbital Eunuchs Sniper

Name:		%{name}
Version:	%{version}
Release:	%mkrel %rel
URL:		https://www.icculus.org/oes/
Source0:	%{name}-%{version}.tar.bz2
Source11:	%{name}-16x16.png
Source12:	%{name}-32x32.png
Source13:	%{name}-48x48.png
Patch0:		orbital_eunuchs_sniper-pointer_size.patch
License:	BSD
Group:		Games/Arcade
Summary:	%{Summary}
BuildRequires:	SDL-devel
BuildRequires:	SDL_image-devel
BuildRequires:	SDL_mixer-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Orbital Eunuchs Sniper is a simple game in which the player
must control an orbital laser to prevent harm from coming to
the VIPs (in blue squares) in the form of human threats
(in red squares). Avoid killing the neutral humans, however,
or else you may be 'retired'. 

%prep
%setup -q
%patch0 -p0

%build
%configure2_5x	--bindir=%{_gamesbindir} \
		--datadir=%{_gamesdatadir} \
		--with-games-dir=%{_gamesdatadir} \
		--with-pic \
		--with-gnu-ld \
		--disable-debug
%make

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{makeinstall_std}

#(peroyvind) move ark-config to %{_bindir} as this belongs to the devel package
%{__install} -d $RPM_BUILD_ROOT{%{_bindir},%{_gamesdatadir}}

install -m 755 -d $RPM_BUILD_ROOT%{_datadir}/applications/
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%Summary
Comment=%Summary
Exec=%{_gamesbindir}/snipe2d
Icon=%name
Terminal=false
Type=Application
StartupNotify=true
Categories=Game;ArcadeGame;
EOF


%{__install} -m644 %{SOURCE11} -D ${RPM_BUILD_ROOT}%{_miconsdir}/%{name}.png
%{__install} -m644 %{SOURCE12} -D ${RPM_BUILD_ROOT}%{_iconsdir}/%{name}.png
%{__install} -m644 %{SOURCE13} -D ${RPM_BUILD_ROOT}%{_liconsdir}/%{name}.png

#(peroyvind) clean out crap
rm -f $RPM_BUILD_ROOT%{_gamesdatadir}/%{name}/snipe2d.x86.static
mv $RPM_BUILD_ROOT%{_gamesdatadir}/%{name}/snipe2d.x86.dynamic $RPM_BUILD_ROOT%{_gamesbindir}/snipe2d.bin

cat <<EOF > $RPM_BUILD_ROOT%{_gamesbindir}/snipe2d
#! /bin/bash
pushd %{_gamesdatadir}/orbital_eunuchs_sniper
snipe2d.bin \$*
popd
EOF

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO COPYING
%{_gamesdatadir}/%{name}
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_datadir}/applications/mandriva-%{name}.desktop
%defattr(755,root,root,755)
%{_gamesbindir}/*




%changelog
* Mon Feb 07 2011 Funda Wang <fwang@mandriva.org> 1.28-12mdv2011.0
+ Revision: 636505
- tighten BR

* Tue Dec 07 2010 Oden Eriksson <oeriksson@mandriva.com> 1.28-11mdv2011.0
+ Revision: 613544
- rebuild

* Thu Feb 25 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 1.28-10mdv2010.1
+ Revision: 510843
- fix release tag

* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 1.28-9mdv2010.0mdv2010.0
+ Revision: 430220
- rebuild

* Wed Jul 30 2008 Thierry Vignaud <tv@mandriva.org> 1.28-8mdv2009.0mdv2009.0
+ Revision: 254913
- rebuild
- drop old menu

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Thu Jan 03 2008 Olivier Blin <oblin@mandriva.com> 1.28-6mdv2008.1mdv2008.1
+ Revision: 141036
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - buildrequires X11-devel instead of XFree86-devel
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'


* Sat Jan 06 2007 Pascal Terjan <pterjan@mandriva.org> 1.28-6mdv2007.0mdv2007.0
+ Revision: 104684
- add patch to handle non 32 bits pointers and re-enable x86_64

  + Götz Waschk <waschk@mandriva.org>
    - don't build on x86_64
    - Import orbital_eunuchs_sniper

* Fri Jan 05 2007 Götz Waschk <waschk@mandriva.org> 1.28-5mdv2007.1mdv2007.1
- xdg menu

* Fri Dec 23 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 1.28-5mdk
- %%rebuild
- %%mkrel

* Fri Aug 27 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.28-4mdk
- rebuild for new menu

* Wed Jun 09 2004 Götz Waschk <waschk@linux-mandrake.com> 1.28-3mdk
- rebuild for new g++

