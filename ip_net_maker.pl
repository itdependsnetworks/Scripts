#!/usr/bin/perl

 use NetAddr::IP;

#fill in your directory here
my $rtr_directory = '/tmp/configs';

opendir(DIR, $rtr_directory);
foreach my $file (readdir(DIR)){
    push @filecheck, "$rtr_directory/$file";
}
closedir(DIR);

my (%nethash,%maskhash)=();
foreach my $filename (@filecheck){
        open(FILE, "$filename") or die("Unable to open file");
        @conf = <FILE>;
        close FILE;

        if ($filename =~ /.+\/(.+)/){
                $device = $1;
        }
        if ($device =~ /(.+?)-/){
                $site = $1;
        }

        my $start = 0;
        foreach my $line (@conf){
                if ($line =~ /^hostname (.+)$/){
                        $hostname = $1;
                        if (lc($hostname) ne lc($device)){
                                push @hostname, "Hostname Mismatch: Device $hostname - DNS $device\n"
                        }
                }
                if ($line =~ /^interface (.+?)\s/){
                        $start = 1;
                        $interface_hold = ();
                }
                if ($start == 1){
                        if ($line =~ /^interface (.+?)\s/){
                                $interface_hold = $1;
                        }
                        elsif ($line =~ /^\s+ip address (\d+\.\d+\.\d+\.\d+) (\d+\.\d+\.\d+\.\d+)/){
                                $ip_address = $1;
                                $subnet_mask = $2;
                                $masklen =  &subnetConversion($subnet_mask,1);
                                $network = getSubnet($ip_address,$subnet_mask );
                                $sort = &makeint("$network/$masklen");
				$nethash{$sort} = $network;
				$maskhash{$sort} = $masklen;
				push @sort, $sort;
                        }
                                elsif ($line =~ /^ shutdown/){
                                        ($subnet_mask,$masklen,$network,$sort,$ip_address) = ();
                                        $interface_hold = ();
                                }

                }
 
        }
#       GOTOEND:
}
@sort = sort(@sort);
@sort = unique(@sort);
foreach my $line (@sort) {
	print "$nethash{$line} $maskhash{$line}\n";
}
print @hostname;

#takes ip address and subenet mack, returns network address
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

sub makeint {
        my $ip = shift;
        my ($ipout,$mask,$intout) = ();
       if ($ip =~ /.+\/(.+)/){
              $mask = $1;
              $mask = sprintf("%03d",$mask);
       }
        if ($ip =~ /(\d+)\.(\d+)\.(\d+)\.(\d+)/){
                my $one = sprintf("%03d",$1);
                my $two = sprintf("%03d",$2);
               my $three = sprintf("%03d",$3);
                my $four = sprintf("%03d",$4);
                $intout = "$one$two$three$four$mask";

        }
        return $intout;
}

#Takes array, returns unique elements
sub unique{
        my (%seen, $array);
        ($array)=@_;
        if(@$array){return grep{$seen{$_} ++} @$array;}
        else{return grep{ ! $seen{$_} ++} @_;}
}

