#!/usr/bin/perl


use REST::Client;


#update community
my $community = 'public';

#update Vendor lookups:
my @checkoui = ();
push @checkoui, 'Netgear';
push @checkoui, 'Flextronics'; 

my $device = @ARGV[0];

my $vlanoid = '1.3.6.1.2.1.47.1.2.1.1.2';
my $cmd = "snmpwalk -c $community -v2c $device $vlanoid";
my @vlans = `$cmd`;

my $macoid = '1.3.6.1.2.1.17.4.3.1.1';
foreach my $line (@vlans){
	if ($line =~ /STRING: "vlan(\d+)"/){ 
		my $vlan = $1;
		my $newcomm = $community . '@' . $vlan;
		my $maccmd = "snmpwalk -c $newcomm -v2c $device $macoid";

		my @current_mac = `$maccmd`;
		push @macs, @current_mac;
	}
}
my %machash =();
foreach my $mac (@macs){
	if ($mac =~ /Hex-STRING: (\w{2} \w{2} \w{2}) \w{2} \w{2} \w{2}/){
		my $mac = $1;
		$mac =~ s/\s+//g;
		$machash{$mac} = 1;
	}

}
my $client = REST::Client->new();

foreach my $key (sort keys %machash){
#	my $oui_name_cmd = "dig +short AS" . "$mac" . ".oui.old.nu/ TXT";
#	my $oui_name_lookup = `$oui_name_cmd`;

	my $rest = "http://www.macvendorlookup.com/api/v2/$key/xml";
	my $rest_lookup = $client->GET("$rest");
	my $oui_name_lookup = $client->responseContent();

	if ($oui_name_lookup =~ /<company>(.+)<\/company>/){
		my $VENDOR = $1;
#		print $VENDOR . "\n";
		foreach my $lookup (@checkoui){
			if ($VENDOR =~ /$lookup/i){
				&sendalert($key,$VENDOR,$lookup,$device);
			}
		}
	}

}

sub sendalert{
	my $oui = shift;
	my $vendor = shift;
	my $lookup = shift;
	my $device = shift;
	print "$device has an OUI of $oui $VENDOR, appears to match $lookup\n";

	
}
