%define		mod_name	access_identd
%define 	apxs		/usr/sbin/apxs1
Summary:	Apache module: access based on ident (RFC1413)
Summary(pl):	Modu³ do apache: dostêp na podstawie protoko³u ident (RFC1413)
Name:		apache1-mod_%{mod_name}
Version:	1.2.0
Release:	0.4
License:	MeepZor Consulting Public Licence (MCPL)
Group:		Networking/Daemons
Source0:	http://meepzor.com/packages/mod_%{mod_name}/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	67a5a1b9d5862eeaf2ba812f6dca98d9
Source1:	http://meepzor.com/packages/mod_access_identd/LICENCE.txt
URL:		http://meepzor.com/packages/mod_access_identd/
BuildRequires:	apache1-devel >= 1.3.33-2
Requires:	apache1 >= 1.3.33-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
A security module for the Apache Web server, supplying mandatory
access control based upon the client username and host. The
credentials are obtained using the identd (RFC1413) mechanism, so this
is of limited usefulness if document access is through a proxy or by
clients not running an RFC1413 server daemon. As a result, this module
is best suited for intranets.

%description -l pl
Modu³ zabezpieczaj±cy dla serwera apache dostarczaj±cy obowi±zkow±
kontrolê dostêpu bazuj±c± na nazwie u¿ytkownika i ho¶cie klienta.
Listy dostêpu uzyskiwane s± przy pomocy protoko³u ident (RFC1413),
zatem u¿yteczno¶æ jest ograniczona je¶li dostêp nastêpuje przez proxy
lub klienci nie posiadaj± serwera identd. Modu³ przeznaczony jest do
u¿ytku g³ównie w intranetach.

%prep
%setup -q -n mod_%{mod_name}

%build
%{apxs} -c mod_%{mod_name}.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/conf.d}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
cp %{SOURCE1} .

echo 'LoadModule %{mod_name}_module	modules/mod_%{mod_name}.so' > \
	$RPM_BUILD_ROOT%{_sysconfdir}/conf.d/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/apache ]; then
	/etc/rc.d/init.d/apache restart 1>&2
fi

%postun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/apache ]; then
		/etc/rc.d/init.d/apache restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc README CHANGELOG mod_access_identd.html LICENCE.txt
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*
