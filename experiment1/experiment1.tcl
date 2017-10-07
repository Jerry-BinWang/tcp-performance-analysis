# Create a simulator object
set ns [new Simulator]

# Open the trace file
set tf [open experiment1.tr w]
set nf [open experiment1.nam w]
$ns trace-all $tf
$ns namtrace-all $nf

# Define a finish procedure
proc finish {} {
    global ns tf nf
    $ns flush-trace

    # Close the trace file
    close $tf
    close $nf

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
$ns duplex-link $N1 $N2 100Mb 10ms DropTail
$ns duplex-link $N2 $N3 100Mb 10ms DropTail
$ns duplex-link $N3 $N4 100Mb 10ms DropTail
$ns duplex-link $N5 $N2 100Mb 10ms DropTail
$ns duplex-link $N3 $N6 100Mb 10ms DropTail

# Setup a TCP connection
set tcp [new Agent/TCP/Reno]
$ns attach-agent $N1 $tcp
set sink [new Agent/TCPSink]
$ns attach-agent $N4 $sink
$ns connect $tcp $sink

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
$cbr set packet_size_ 100
$cbr set rate_ 5mb
$cbr attach-agent $udp

# Schedule events
$ns at 0.5 "$cbr start"
$ns at 1.0 "$ftp start"
$ns at 9.0 "$ftp stop"
$ns at 9.5 "$cbr stop"

# Call the finish procedure
$ns at 10.0 "finish"

# Run the simulation
$ns run
