%define contentdir /var/www
%define their_version 1.4.1

Summary: Squid report generator per user/ip/name
Name: sarg
Version: 1.4.1
Release: 4mdk
URL: http://sarg.sourceforge.net/
Source: http://web.onda.com.br/orso/sarg-%{their_version}.tar.bz2
Source1: 0sarg.daily
Source2: 0sarg.weekly
Source3: 0sarg.monthly
Source4: sarg.conf.rpm
Patch0: sarg-1.4.1-2.6.fix.patch
Patch1: sarg-1.4.1-index.sort.patch
License: GPL
Group: Monitoring
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Requires: squid, bash

%description
Sarg (was Sqmgrlog) generate reports per user/ip/name from SQUID log file.
The reports will be generated in HTML or email.

%prep
%setup -n %{name}-%{their_version}

%patch0 -p1 
%patch1 -p1 -b .sort

%build
chmod a+x cfgaux languages include
%configure --enable-bindir=%{_sbindir} --enable-sysconfdir=%{_sysconfdir}/%{name} --enable--mandir=%{buildroot}%{_mandir}


mkdir -p %{buildroot}/%{_mandir}/man1
perl -p -i -e 's|/usr/share/man/man1|%{buildroot}/usr/share/man/man1|' $RPM_BUILD_DIR/%name-%their_version/Makefile
make

%install
mkdir -p $RPM_BUILD_ROOT/{usr/sbin,etc/sarg,var}
mkdir -p $RPM_BUILD_ROOT%{contentdir}/html/squid
mkdir -p $RPM_BUILD_ROOT%{contentdir}/html/squid/{daily,weekly,monthly}
make BINDIR=$RPM_BUILD_ROOT%{_sbindir} SYSCONFDIR=$RPM_BUILD_ROOT%{_sysconfdir}/sarg MANDIR=$RPM_BUILD_ROOT%{_mandir}/man1 install
mkdir -p $RPM_BUILD_ROOT/etc/cron.daily
install -m 0755 %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.daily/0%{name}
mkdir -p $RPM_BUILD_ROOT/etc/cron.weekly
install -m 0755 %{SOURCE2} $RPM_BUILD_ROOT/etc/cron.weekly/0%{name}
mkdir -p $RPM_BUILD_ROOT/etc/cron.monthly
install -m 0755 %{SOURCE3} $RPM_BUILD_ROOT/etc/cron.monthly/0%{name}
cp sarg.conf $RPM_BUILD_ROOT%{_sysconfdir}/sarg/sarg.conf.default
cp $RPM_BUILD_ROOT%{_sysconfdir}/sarg/sarg.conf.default $RPM_BUILD_ROOT/%{_sysconfdir}/sarg/sarg.conf

# real access.log file location
perl -p -i -e "s|#access_log /usr/local/squid/logs/access.log|access_log /var/log/squid/access.log|" $RPM_BUILD_ROOT/%{_sysconfdir}/sarg/sarg.conf
perl -p -i -e "s|#output_dir /home/httpd/html/squid-reports # RedHat version|output_dir /var/www/html/squid-reports # Mandrake version|" $RPM_BUILD_ROOT/%{_sysconfdir}/sarg/sarg.conf

strip -s $RPM_BUILD_ROOT/%{_sbindir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,squid)
%doc CONTRIBUTORS DONATIONS ChangeLog
%{_mandir}/man1/*
%attr(0755,root,squid) %{_sbindir}/%{name}*
%attr(0664,root,squid) %config(noreplace) %{_sysconfdir}/sarg/sarg.conf
%attr(0755,root,squid) %dir %{contentdir}/html/squid
%attr(0755,root,squid) %dir %{contentdir}/html/squid/daily
%attr(0755,root,squid) %dir %{contentdir}/html/squid/weekly
%attr(0755,root,squid) %dir %{contentdir}/html/squid/monthly
%config(noreplace) %attr(0755,root,squid) %dir %{_sysconfdir}/sarg
%config(noreplace) %attr(0755,root,squid) %dir %{_sysconfdir}/sarg/languages
%config(noreplace) %attr(0754,root,squid) %{_sysconfdir}/cron.*/*
%config(noreplace) %attr(0644,root,squid) %{_sysconfdir}/sarg/sarg.conf.default
%config(noreplace) %attr(0644,root,squid) %{_sysconfdir}/sarg/exclude_codes
%config(noreplace) %attr(0644,root,squid) %{_sysconfdir}/sarg/languages/.new
%config(noreplace) %attr(0644,root,squid) %{_sysconfdir}/sarg/languages/*

