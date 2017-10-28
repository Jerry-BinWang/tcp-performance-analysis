# Create a simulator object
set ns [new Simulator]

# Open the trace file
set tf [open [lindex $argv 12] w]
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
$ns trace-queue $N4 $N3 $tf
$ns trace-queue $N5 $N2 $tf
$ns trace-queue $N2 $N5 $tf
$ns trace-queue $N3 $N6 $tf
$ns trace-queue $N6 $N3 $tf

# Setup a TCP connection
set tcp_1 [new [lindex $argv 1]]
$ns attach-agent $N1 $tcp_1
set sink_1 [new Agent/TCPSink]
$ns attach-agent $N4 $sink_1
$ns connect $tcp_1 $sink_1

$tcp_1 trace cwnd_
$tcp_1 trace maxseq_
$tcp_1 attach $tf

# Setup a FTP connection over TCP
set ftp_1 [new Application/FTP]
$ftp_1 attach-agent $tcp_1

# Setup another TCP connection
set tcp_2 [new [lindex $argv 2]]
$ns attach-agent $N5 $tcp_2
set sink_2 [new Agent/TCPSink]
$ns attach-agent $N6 $sink_2
$ns connect $tcp_2 $sink_2

$tcp_2 trace cwnd_
$tcp_2 trace maxseq_
$tcp_2 attach $tf

# Setup another FTP connection over TCP 2
set ftp_2 [new Application/FTP]
$ftp_2 attach-agent $tcp_2

# Setup a UDP connection
set udp [new Agent/UDP]
$ns attach-agent $N2 $udp
set null [new Agent/Null]
$ns attach-agent $N3 $null
$ns connect $udp $null

# Setup a CBR flow
set cbr [new Application/Traffic/CBR]
$cbr set packet_size_ [lindex $argv 3]
$cbr set rate_ [lindex $argv 4]
$cbr attach-agent $udp

# Schedule events
$ns at [lindex $argv 5] "$cbr start"
$ns at [lindex $argv 6] "$cbr stop"
$ns at [lindex $argv 7] "$ftp_1 start"
$ns at [lindex $argv 8] "$ftp_1 stop"
$ns at [lindex $argv 9] "$ftp_2 start"
$ns at [lindex $argv 10] "$ftp_2 stop"

# Call the finish procedure
$ns at [lindex $argv 11] "finish"

# Print CBR packet size and interval
puts "CBR packet size = [$cbr set packet_size_]"
puts "CBR interval = [$cbr set interval_]"

# Run the simulation
$ns run
