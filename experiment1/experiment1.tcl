# Create a simulator object
set ns [new Simulator]

# Open the trace file
set tf [open [lindex $argv 9] w]
# $ns trace-all $tf

# Define a finish procedure
proc finish {} {
    global ns tf
    $ns flush-trace

    # Close the trace file
    close $tf

    exit 0
}

# Create nodes
set N1 [$ns node]
set N2 [$ns node]
set N3 [$ns node]
set N4 [$ns node]
set N5 [$ns node]
set N6 [$ns node]

# Create links
$ns duplex-link $N1 $N2 10Mb [lindex $argv 0] DropTail
$ns duplex-link $N2 $N3 10Mb [lindex $argv 0] DropTail
$ns duplex-link $N3 $N4 10Mb [lindex $argv 0] DropTail
$ns duplex-link $N5 $N2 10Mb [lindex $argv 0] DropTail
$ns duplex-link $N3 $N6 10Mb [lindex $argv 0] DropTail

$ns trace-queue $N1 $N2 $tf
$ns trace-queue $N2 $N1 $tf
$ns trace-queue $N3 $N4 $tf 

# Setup a TCP connection
set tcp [new [lindex $argv 1]]
$ns attach-agent $N1 $tcp
set sink [new Agent/TCPSink]
$ns attach-agent $N4 $sink
$ns connect $tcp $sink

$tcp trace cwnd_
$tcp trace maxseq_
$tcp attach $tf

# Setup a FTP connection over TCP
set ftp [new Application/FTP]
$ftp attach-agent $tcp

# Setup a UDP connection
set udp [new Agent/UDP]
$ns attach-agent $N2 $udp
set null [new Agent/Null]
$ns attach-agent $N3 $null
$ns connect $udp $null

# Setup a CBR flow
set cbr [new Application/Traffic/CBR]
$cbr set packet_size_ [lindex $argv 2]
$cbr set rate_ [lindex $argv 3]
$cbr attach-agent $udp

# Schedule events
$ns at [lindex $argv 4] "$cbr start"
$ns at [lindex $argv 5] "$cbr stop"
$ns at [lindex $argv 6] "$ftp start"
$ns at [lindex $argv 7] "$ftp stop"


# Call the finish procedure
$ns at [lindex $argv 8] "finish"

# Print CBR packet size and interval
puts "CBR packet size = [$cbr set packet_size_]"
puts "CBR interval = [$cbr set interval_]"

# Run the simulation
$ns run
