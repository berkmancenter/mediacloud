#!/usr/bin/env perl

#
# Add MediaWords::Job::TM::SnapshotTopic job
#

use strict;
use warnings;

BEGIN
{
    use FindBin;
    use lib "$FindBin::Bin/../lib";
}

use Modern::Perl "2015";
use MediaWords::CommonLibs;

use Getopt::Long;

use MediaWords::DB;
use MediaWords::TM;
use MediaWords::Job::TM::SnapshotTopic;

sub main
{
    my ( $topic_opt, $direct_job );

    binmode( STDOUT, 'utf8' );
    binmode( STDERR, 'utf8' );
    $| = 1;

    Getopt::Long::GetOptions(
        "topic=s"     => \$topic_opt,
        "direct_job!" => \$direct_job
    ) || return;

    die( "Usage: $0 --topic < id >" ) unless ( $topic_opt );

    my $db = MediaWords::DB::connect_to_db();
    my $topics = MediaWords::TM::require_topics_by_opt( $db, $topic_opt );
    unless ( $topics )
    {
        die "Unable to find topics for option '$topic_opt'";
    }

    for my $topic ( @{ $topics } )
    {
        my $topics_id = $topic->{ topics_id };

        if ( $direct_job )
        {
            MediaWords::Job::TM::SnapshotTopic->run_locally( $db, { topics_id => $topics_id } );
            next;
        }

        my $args = { topics_id => $topics_id };
        my $job_id = MediaWords::Job::TM::SnapshotTopic->add_to_queue( $args );
        INFO "Added topic ID $topics_id ('$topic->{ name }') with job ID: $job_id";
    }

}

main();

__END__
