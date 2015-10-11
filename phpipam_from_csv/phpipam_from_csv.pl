#!/usr/bin/perl

 use NetAddr::IP;
 use Net::IP;



# Fill out as appropriate
my $section = 3; # section number
my $folderroot = 7; #folder should be 7 if it is the first thing you enter, but please check
my $file = 'test.csv'; #CSV file filed out as '<network>,<subnet_mask_slash_format>,<description>
my $index = 8; # if the index is higher then starting off
my $logdate = '2015-04-01 01:00:00'; #time stamp all logs will show

my ($locationdesc,@location) = ();

open(FILE, "$file") or die("Unable to open file");
@csv = <FILE>;
close FILE;
chomp @csv;

foreach my $line (@csv){
	@splitline = split (/,/,$line);
	$network = $splitline[0];
	$mask = $splitline[1];
	$description = $splitline[2];

	$deschash{$network}{$mask} = $description;
	push (@{$HOA{$mask}}, $network);

}
my %hash = ();
$index++;
my %parentid =();
for ($i = 8; $i <= 32; $i++){
	my $subnet_mask = &subnetConversion($i);
	foreach my $ip_address (@{$HOA{$i}}){
		$location = $deschash{$ip_address}{$i};
		$found = ();

		$name = $location;
		my $dec =  ip2dec($ip_address);
		$network = $ip_address;
		$masklen = $i ;
		$startcount = $masklen - 1 ;

		if ($hash{$dec}{$i}){
	#		print "MATCH $ip_address $i\n";
		}
		elsif (!$hash{$dec}{$i} && $ip_address =~ /^\d+\.\d+\.\d+\.\d+/){
			$current_dec = ip2dec($current_network);
	                for ($count = $startcount; $count >= 8; $count--){
	                        my $current_longmask = subnetConversion($count);
	                        my $current_network = getSubnet($ip_address,$current_longmask);

				my $subnet_mask_current = &subnetConversion($count);
				$current_dec = ip2dec($current_network);
	                        if ($hash{$current_dec}{$count}){
                                        $last = 1;
                                        $found = 1;
					$current_parent = $hash{$current_dec}{$count};
					print "INSERT INTO `subnets` (`id`, `subnet`, `mask`, `sectionId`, `description`, `vrfId`, `masterSubnetId`, `allowRequests`, `vlanId`, `showName`, `permissions`, `isFolder`, `editDate`)";
					print " values (\'$index\', \'$dec\', \'$masklen\', \'$section\', \'$name\', \'0\', \'$current_parent\', \'1\', \'0\', \'0\', \'{\"2\":\"3\"}\', \'0\', \'$logdate\');\n";
	                                last;
	                        }
	                }
			if (!$found){
				print "INSERT INTO `subnets` (`id`, `subnet`, `mask`, `sectionId`, `description`, `vrfId`, `masterSubnetId`, `allowRequests`, `vlanId`, `showName`, `permissions`, `isFolder`, `editDate`)";
				print " values (\'$index\', \'$dec\', \'$masklen\', \'$section\', \'$name\', \'0\', \'$folderroot\', \'1\', \'0\', \'0\', \'{\"2\":\"3\"}\', \'0\', \'$logdate\');\n";
			}
				$hash{$dec}{$i} = $index;
		
		}
#		else {
#				print "insert into subnets values (\'$index\', \'$dec\', \'$masklen\', \'$section\', \'$name\', \'0\', \'$parentid}\', \'1\', \'0\', \'0\', \'{\"2\":\"3\"}\', \'0\', \'0x30\', \'0\', \'$logdate\');\n";
#		}
		$index++;

        }
}
#Takes slash netmask, converts to subnet form
sub subnetConversion {
        my %sub_conversion = (
        "8"=>"255.0.0.0",
        "9"=>"255.128.0.0",
        "10"=>"255.192.0.0",
        "11"=>"255.224.0.0",
        "12"=>"255.240.0.0",
        "13"=>"255.248.0.0",
        "14"=>"255.252.0.0",
        "15"=>"255.254.0.0",
        "16"=>"255.255.0.0",
        "17"=>"255.255.128.0",
        "18"=>"255.255.192.0",
        "19"=>"255.255.224.0",
        "20"=>"255.255.240.0",
        "21"=>"255.255.248.0",
        "22"=>"255.255.252.0",
        "23"=>"255.255.254.0",
        "24"=>"255.255.255.0",
        "25"=>"255.255.255.128",
        "26"=>"255.255.255.192",
        "27"=>"255.255.255.224",
        "28"=>"255.255.255.240",
        "29"=>"255.255.255.248",
        "30"=>"255.255.255.252",
        "31"=>"255.255.255.254",
        "32"=>"255.255.255.255");
        if ($_[1]){
                %rev_conv = reverse %sub_conversion;
                return  $rev_conv{$_[0]};
        }
        return $sub_conversion{$_[0]};
}

sub getSubnet {
        my $ipaddr=$_[0];
        my $nmask=$_[1];

        my @addrarr=split(/\./,$ipaddr);
        my ( $ipaddress ) = unpack( "N", pack( "C4",@addrarr ) );

        my @maskarr=split(/\./,$nmask);
        my ( $netmask ) = unpack( "N", pack( "C4",@maskarr ) );

        # Calculate network address by logical AND operation of addr & netmask
        # and convert network address to IP address format
        my $netadd = ( $ipaddress & $netmask );
        my @netarr=unpack( "C4", pack( "N",$netadd ) );
        my $netaddress=join(".",@netarr);

        #print "Network address : $netaddress \n";
        return $netaddress;

        # Calculate broadcase address by inverting the netmask
        # and do a logical or with network address
        my $bcast = ( $ipaddress & $netmask ) + ( ~ $netmask );
        my @bcastarr=unpack( "C4", pack( "N",$bcast ) ) ;
        my $broadcast=join(".",@bcastarr);

        #print "Broadcast address: $broadcast\n";
}

  sub ip2dec ($) {
    return unpack N => pack CCCC => split /\./ => shift;
  }
