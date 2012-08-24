use strict;
use utf8;

use Amazon::SQS::Simple;
use Config::Simple;
use Net::SMTP;

my $mailer = new Net::SMTP::TLS(
	'smtp.gmail.com',  
	Hello   =>      'smtp.gmail.com',
	Port    =>      587,
	User    =>      'cys.mailer',
  Password=>      'password');
$mailer->mail('from@domain.com');
$mailer->to('to@domain.com');
$mailer->data;
$mailer->datasend("Sent from perl!");
$mailer->dataend;
$mailer->quit;

#calculate config file name
my $config = {}; #must be empty hash for Config::Simple
my $config_file = $0; $config_file =~ s/\.([^\.]+)$/\.cfg/;
die("No config file $config_file!") unless -f $config_file;

$config = Config::Simple->new( $config_file) || die("No configuration file");
my $aws_credentials = Config::Simple->new('.aws_credentails') || die("No credentials found"); #format accesskey\t_accesskey_\nsecretkey\t_secretkey_

$smtp_credentials = Config::Simple->new('smtp.credentails') || die("No credentials found"); #format accesskey\t_accesskey_\nsecretkey\t_secretkey_

#AWS Private
my $access_key = 'AKIAIC2DBRTIUKHMGASQ'; # Your AWS Access Key ID
my $secret_key = '2Ofh3ICjeKpxeWBV2KGmKJ4co4WoeGtpumiiGEPX'; # Your AWS Secret Key
my $queue_uri = 'https://queue.amazonaws.com/041722291456/sinqrtel_public'; #public queue uri

#AWS Public
my $public_access_key = 'AKIAJZDRZUXVHSK3G6LA';
my $public_secret_key = 'uBIMu6R7J7Idsdvx18495KlEZ+LEMbUDndOLjUYi';

# Create an SQS object
my $sqs = new Amazon::SQS::Simple( $aws_credentials->{accesskey}, $aws_credentials->{secretkey} );

# Get Existing queue by endpoint
my $q = $sqs->GetQueue( $queue_uri );

# Retrieve a message
my $msg = $q->ReceiveMessage( 'AttributeName.1' => 'All' , MaxNumberOfMessages=>1, VisibilityTimeout=>60 );

if ( defined $msg ) {
  print $msg->MessageBody() . "\n";
  if ( defined $msg->{Attribute} ) {
	print "\t" . join("|", map {$_->{Name} . '=' . $_->{Value}} @{$msg->{Attribute}} );
  }

  # Delete the message
 # unless ( $q->DeleteMessage($msg->ReceiptHandle()) ) {
	#print "Delete failed\n";
  #}
} else {
  print "No message visible right now\n";
}
