%define contentdir /var/www

Summary:	Squid report generator per user/ip/name
Name:		sarg
Version:	2.2.5
Release:	%mkrel 7
License:	GPLv2+
Group:		Monitoring
URL:		http://sarg.sourceforge.net/
Source:		http://prdownloads.sourceforge.net/sarg/%{name}-%{version}.tar.gz
Source1:	0sarg.daily
Source2:	0sarg.weekly
Source3:	0sarg.monthly
Source4:	sarg.conf.mandriva
Patch1:		sarg-2.2.3.1-lots-of-compiler-warnings.patch
Patch2:		sarg-2.2.3.1-rewind.patch
Patch3:		sarg-2.2.5-avx-fix_segfault.patch
Patch4:		sarg-2.2.5-avx-make-getword-better.patch
Patch5:		sarg-2.2.5-avx-make_useragent_prettier.patch
Patch6:		sarg-2.2.5-avx-too_small_font_buffer.patch
Patch7:		sarg-2.2.5-enlarge_report_buffers.patch
Patch8:		sarg-2.2.5-limit_sprintf.patch
Requires:	squid, bash
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Sarg (was Sqmgrlog) generate reports per user/ip/name from SQUID log file.
The reports will be generated in HTML or email.

%prep

%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p0

%build
chmod a+x cfgaux languages include
%configure2_5x \
    --enable-bindir=%{_sbindir} \
    --enable-sysconfdir=%{_datadir}/%{name} \
    --enable--mandir=%{buildroot}%{_mandir}


mkdir -p %{buildroot}/%{_mandir}/man1
perl -p -i -e 's|/usr/share/man/man1|%{buildroot}/usr/share/man/man1|' $RPM_BUILD_DIR/%name-%version/Makefile
make

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/{%_sbindir,%_datadir/%name,%_sysconfdir/%name}
mkdir -p $RPM_BUILD_ROOT%{contentdir}/html/squid
mkdir -p $RPM_BUILD_ROOT%{contentdir}/html/squid/{daily,weekly,monthly}
make BINDIR=$RPM_BUILD_ROOT%{_sbindir} SYSCONFDIR=$RPM_BUILD_ROOT%{_datadir}/%{name} MANDIR=$RPM_BUILD_ROOT%{_mandir}/man1 install
mkdir -p $RPM_BUILD_ROOT/etc/cron.daily
install -m 0755 %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.daily/0%{name}
mkdir -p $RPM_BUILD_ROOT/etc/cron.weekly
install -m 0755 %{SOURCE2} $RPM_BUILD_ROOT/etc/cron.weekly/0%{name}
mkdir -p $RPM_BUILD_ROOT/etc/cron.monthly
install -m 0755 %{SOURCE3} $RPM_BUILD_ROOT/etc/cron.monthly/0%{name}
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/%{name}.conf
ln -sf %_sysconfdir/%{name}/%{name}.conf $RPM_BUILD_ROOT/%{_datadir}/%{name}/%{name}.conf
mv $RPM_BUILD_ROOT/%{_datadir}/%{name}/exclude_codes $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/exclude_codes

%find_lang %name

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %name.lang
%defattr(-,root,squid)
%doc CONTRIBUTORS DONATIONS ChangeLog
%{_mandir}/man1/*
%attr(0755,root,squid) %{_sbindir}/%{name}*
%attr(0755,root,squid) %dir %{_sysconfdir}/%{name}
%attr(0664,root,squid) %config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%attr(0755,root,squid) %dir %{contentdir}/html/squid
%attr(0755,root,squid) %dir %{contentdir}/html/squid/daily
%attr(0755,root,squid) %dir %{contentdir}/html/squid/weekly
%attr(0755,root,squid) %dir %{contentdir}/html/squid/monthly
%{_datadir}/%{name}
%config(noreplace) %attr(0754,root,squid) %{_sysconfdir}/cron.*/*
%config(noreplace) %attr(0644,root,squid) %{_sysconfdir}/%{name}/exclude_codes
