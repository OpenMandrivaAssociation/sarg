%define contentdir /var/www

Summary:	Squid report generator per user/ip/name
Name:		sarg
Version:	2.3.2
Release:	1
License:	GPLv2+
Group:		Monitoring
URL:		http://sarg.sourceforge.net/
Source:		http://prdownloads.sourceforge.net/sarg/%{name}-%{version}.tar.gz
Source1:	0sarg.daily
Source2:	0sarg.weekly
Source3:	0sarg.monthly
Source4:	sarg.conf.mandriva
Requires:	squid
Requires:	bash

%description
Sarg (was Sqmgrlog) generate reports per user/ip/name from SQUID log file.
The reports will be generated in HTML or email.

%prep
%setup -q

%build
chmod a+x cfgaux configure include
chmod 744 images
%configure2_5x

mkdir -p %{buildroot}/%{_mandir}/man1
perl -p -i -e 's|/usr/share/man/man1|%{buildroot}/usr/share/man/man1|' %{buildroot}/%name-%version/Makefile
make

%install
mkdir -p %{buildroot}/{%_bindir,%_datadir/%name,%_sysconfdir/%name}
mkdir -p %{buildroot}%{contentdir}/html/squid
mkdir -p %{buildroot}%{contentdir}/html/squid/{daily,weekly,monthly}
%makeinstall_std
mkdir -p %{buildroot}/etc/cron.daily
install -m 0755 %{SOURCE1} %{buildroot}/etc/cron.daily/0%{name}
mkdir -p %{buildroot}/etc/cron.weekly
install -m 0755 %{SOURCE2} %{buildroot}/etc/cron.weekly/0%{name}
mkdir -p %{buildroot}/etc/cron.monthly
install -m 0755 %{SOURCE3} %{buildroot}/etc/cron.monthly/0%{name}
install -m 644 %{SOURCE4} %{buildroot}/%{_sysconfdir}/%{name}/%{name}.conf
mv %{buildroot}/%{_sysconfdir}/exclude_codes %{buildroot}/%{_sysconfdir}/%{name}/exclude_codes
mv %{buildroot}/%{_sysconfdir}/%{name}.conf %{buildroot}/%{_sysconfdir}/%{name}/%{name}.conf
mv %{buildroot}/%{_sysconfdir}/user_limit_block %{buildroot}/%{_sysconfdir}/%{name}/user_limit_block
mv %{buildroot}/%{_sysconfdir}/css.tpl %{buildroot}/%{_sysconfdir}/%{name}/css.tpl

%find_lang %{name}

%files -f %{name}.lang
%defattr(-,root,squid)
%doc CONTRIBUTORS DONATIONS ChangeLog
%{_mandir}/man1/*
%{_sysconfdir}/%{name}/*.tpl
%{_sysconfdir}/%{name}/user*
%attr(0755,root,squid) %{_bindir}/%{name}*
%attr(0755,root,squid) %dir %{_sysconfdir}/%{name}
%attr(0664,root,squid) %config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%attr(0755,root,squid) %dir %{contentdir}/html/squid
%attr(0755,root,squid) %dir %{contentdir}/html/squid/daily
%attr(0755,root,squid) %dir %{contentdir}/html/squid/weekly
%attr(0755,root,squid) %dir %{contentdir}/html/squid/monthly
%attr(0755,root,squid) %dir %{contentdir}/html/%{name}-php
%{_datadir}/%{name}
%config(noreplace) %attr(0754,root,squid) %{_sysconfdir}/cron.*/*
%config(noreplace) %attr(0644,root,squid) %{_sysconfdir}/%{name}/exclude_codes

