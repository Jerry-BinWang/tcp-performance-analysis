import subprocess

latency_list = ['1ms', '10ms', '100ms']
tcp_pair_list = [('Agent/TCP/Reno', 'Agent/TCP/Reno'),
                 ('Agent/TCP/Newreno', 'Agent/TCP/Reno'),
                 ('Agent/TCP/Vegas', 'Agent/TCP/Vegas'),
                 ('Agent/TCP/Newreno', 'Agent/TCP/Vegas')]
cbr_packet_size_list = [1000]
cbr_bandwidth_list = [str(i)+'mb' for i in range(1, 11)]
start_time_diff_list = [-1, 0.1, 1, 5, 10]
tcp_run_time = 20

def run_ns2_simulation(latency, tcp_1, tcp_2, cbr_packet_size, cbr_bandwidth, start_time_diff):
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
    file_name += tcp_1.split('/')[-1]
    file_name += '_'
    file_name += tcp_2.split('/')[-1]
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
    subprocess.run(['ns', 'experiment2.tcl', latency, tcp_1, tcp_2 , str(cbr_packet_size), cbr_bandwidth
                       , str(cbr_start_time), str(cbr_end_time), str(tcp_start_time), str(tcp_end_time)
                       , str(tcp_start_time), str(tcp_end_time), str(end_time), file_name])

if __name__ == '__main__':
    for latency in latency_list:
        for tcp_pair in tcp_pair_list:
            tcp_1 = tcp_pair[0]
            tcp_2 = tcp_pair[1]
            for cbr_packet_size in cbr_packet_size_list:
                for cbr_bandwidth in cbr_bandwidth_list:
                    for start_time_diff in start_time_diff_list:
                        run_ns2_simulation(latency, tcp_1, tcp_2, cbr_packet_size, cbr_bandwidth, start_time_diff)