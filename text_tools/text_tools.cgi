#!/usr/bin/perl
 use CGI qw(:standard);
print "Content-type: text/plain\n\n";

my $interfaces  = param('interfaces');
my $configs  = param('configs');
my $type  = param('type');




$interfaces =~ s/\r/\n/g;
$interfaces =~ s/\n\n/\n/g;
my @interfaces = split(/\n|\r/,$interfaces);
my (%temp_hash,%final_hash,%reverse_hash) =();
#my $type = 'multiple';

if ($type eq 'onetime') {
	my (@firstpass,@secondpass)= ();
	foreach my $line (@interfaces) {
		my @splitinput = split(/,/,$line);
		my $tempname = randomPassword(12);
		my $originalname = $splitinput[0];
		my $newname = $splitinput[1];
		chomp($newname);
		$temp_hash{$originalname} = $tempname;
		$final_hash{$tempname} = $newname;
		$reverse_hash{$tempname} = $originalname;
		push @firstpass, $originalname if $originalname;
		push @secondpass, $tempname if $originalname;
	}
	my $configs1 = $configs;
	foreach my $line (@firstpass){
		$configs1 =~ s/$line/$temp_hash{$line}/g;
	}
	my $configs2 = $configs1;
	foreach my $line (@secondpass){
		$configs2 =~ s/$line/$final_hash{$line}/g;
	}
	print $configs2;
}
elsif ($type eq 'multiple'){
	my $variables = shift(@interfaces);
	my @variableinput = split(/,/,$variables);
        foreach my $line (@interfaces) {
                my @splitinput = split(/,/,$line);
                my $number = @splitinput;
#		$number++;

		my $configs1 = $configs;
                for (my $i = 0; $i <= $number; $i++) {
#			my $ii = $i + 1;
			$configs1 =~ s/$variableinput[$i]/$splitinput[$i]/g;
		}
		print "$configs1\n";			

#               my $configs1 = $configs;
#               my $configs2 = $configs1;
#               $configs2 =~ s/$line/$final_hash{$line}/g;
#               print $configs2 . "\n\n";
        }
}


sub randomPassword {
	my $password;
	my $_rand;

	my $password_length = $_[0];
	    if (!$password_length) {
	        $password_length = 10;
	    }

	my @chars = split(" ",
	    "a b c d e f g h i j k l m n o
	    p q r s t u v w x y z A B C D
	    E F G H I J K L M N O P Q R S
	    T U V W X Y Z - _
	    0 1 2 3 4 5 6 7 8 9");
	
	srand;

	for (my $i=0; $i <= $password_length ;$i++) {
	    $_rand = int(rand 41);
	    $password .= $chars[$_rand];
	}
	return $password;
}

