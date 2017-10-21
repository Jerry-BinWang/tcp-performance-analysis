import subprocess

latency_list = ['1ms', '10ms', '100ms']
TCP_list = ['Agent/TCP', 'Agent/TCP/Reno', 'Agent/TCP/Newreno', 'Agent/TCP/Vegas']
CBR_packet_size_list = [100, 200, 500, 1000]
CBR_bandwidth_list = [str(i)+'mb' for i in range(1, 11)]
start_time_diff_list = [-1, 0.1, 1, 5, 10]
tcp_run_time = 20

def run_ns2_simulation(latency, tcp, cbr_packet_size, cbr_bandwidth, start_time_diff):
    if start_time_diff < 0:
        cbr_start_time = 0
        tcp_start_time = -start_time_diff
    else:
        tcp_start_time = 0
        cbr_start_time = start_time_diff
    tcp_end_time = tcp_start_time + tcp_run_time
    cbr_end_time = tcp_end_time + 5
    end_time = cbr_end_time + 5
    
    file_name = latency + '_'
    file_name += tcp.split('/')[-1]
    file_name += '_'
    file_name += str(cbr_packet_size)
    file_name += '_'
    file_name += cbr_bandwidth
    file_name += '_'
    file_name += str(start_time_diff)
    file_name += '_'
    file_name += str(tcp_run_time)
    file_name += '.tr'
    print(file_name)
    subprocess.run(['ns', 'experiment1.tcl', latency, tcp, str(cbr_packet_size), cbr_bandwidth
        , str(cbr_start_time), str(cbr_end_time), str(tcp_start_time), str(tcp_end_time), str(end_time), file_name])


if __name__ == '__main__':
    sum = 0
    for latency in latency_list:
        for tcp in TCP_list:
            for start_time_diff in start_time_diff_list:
                for cbr_packet_size in CBR_packet_size_list:
                    for cbr_bandwidth in CBR_bandwidth_list:
                        run_ns2_simulation(latency, tcp, cbr_packet_size, cbr_bandwidth, start_time_diff)