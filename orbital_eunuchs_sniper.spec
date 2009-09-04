%define	name	orbital_eunuchs_sniper
%define	version	1.28
%define release	%mkrel 9
%define	Summary	Orbital Eunuchs Sniper

Name:		%{name}
Version:	%{version}
Release:	%mkrel %{release}
URL:		http://www.icculus.org/oes/
Source0:	%{name}-%{version}.tar.bz2
Source11:	%{name}-16x16.png
Source12:	%{name}-32x32.png
Source13:	%{name}-48x48.png
Patch0:		orbital_eunuchs_sniper-pointer_size.patch
License:	BSD
Group:		Games/Arcade
Summary:	%{Summary}
BuildRequires:	SDL_image-devel X11-devel jpeg-devel oggvorbis-devel png-devel
BuildRequires:	nas-devel SDL_mixer-devel
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
		--with-pic \
		--with-gnu-ld \
		--disable-debug
%make CXXFLAGS="$RPM_OPT_FLAGS"

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{makeinstall} bindir=$RPM_BUILD_ROOT%{_gamesbindir} datadir=$RPM_BUILD_ROOT%{_gamesdatadir}

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
Categories=X-MandrivaLinux-MoreApplications-Games-Arcade;Game;ArcadeGame;
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


