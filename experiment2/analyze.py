import os
import csv

def read_records_from_file(file):
    records = []

    with open(file) as fin:
        for line in fin:
            tokens = line.strip().split()
            if len(tokens) == 12:
                records.append(tokens)

    return records

def is_tcp_send_event(record, node):
    return record[0] == '+' and record[2] == node and record[4] == 'tcp'

def is_tcp_recv_event(record, node):
    return record[0] == 'r' and record[3] == node and record[4] == 'tcp'

def is_ack_send_event(record, node):
    return record[0] == '+' and record[2] == node and record[4] =='ack'

def is_ack_recv_event(record, node):
    return record[0] == 'r' and record[3] == node and record[4] == 'ack'

def get_time(record):
    return float(record[1])

def get_packet_bits(record):
    return 8 * int(record[5])

def calculate_throughput(records, from_node, to_node):
    start_time = None
    for record in records:
        if is_tcp_send_event(record, from_node):
            start_time = get_time(record)
            break

    end_time = None
    received_bits = 0
    seen_seq = set()
    for record in records:
        seq_id = record[10]
        if is_tcp_recv_event(record, to_node) and seq_id not in seen_seq:
            received_bits += get_packet_bits(record)
            seen_seq.add(seq_id)
            end_time = get_time(record)

    return (received_bits / (end_time - start_time)) / 1e6

def calculate_drop_rate(records, from_node, to_node):
    send_pkt_num = 0
    recv_pkt_num = 0

    for record in records:
        if is_tcp_send_event(record, from_node):
            send_pkt_num += 1
        elif is_tcp_recv_event(record, to_node):
            recv_pkt_num += 1

    return ((send_pkt_num - recv_pkt_num) / send_pkt_num) * 100

def calculate_rtt(records, from_node, to_node):
    tcp_id_send_time_map = {}
    tcp_recv_time_id_map = {}
    ack_id_send_time_map = {}

    sum = 0.0
    n = 0

    for record in records:
        pkt_id = record[11]
        if is_tcp_send_event(record, from_node):
            tcp_id_send_time_map[pkt_id] = get_time(record)
        elif is_tcp_recv_event(record, to_node):
            tcp_recv_time_id_map[get_time(record)] = pkt_id
        elif is_ack_send_event(record, to_node):
            ack_id_send_time_map[pkt_id] = get_time(record)
        elif is_ack_recv_event(record, from_node):
            tcp_pkt_id = tcp_recv_time_id_map.get(ack_id_send_time_map.get(pkt_id))
            sum += get_time(record) - tcp_id_send_time_map[tcp_pkt_id]
            n += 1

    return sum / n


if __name__ == '__main__':
    results_folder = 'results/'
    with open('result.csv', 'w') as fout:
        field_names = ['latency', 'tcp_1', 'tcp_2', 'cbr_packet_size', 'cbr_bandwidth', 'start_time_diff',
                       'throughput_1', 'throughput_2','drop_rate_1', 'drop_rate_2', 'rtt_1', 'rtt_2']

        writer = csv.DictWriter(fout, fieldnames= field_names)
        writer.writeheader()
        for file in os.listdir(results_folder):
            parameters = file.split('_')
            print(parameters)
            record = {}
            record['latency'] = parameters[0]
            record['tcp_1'] = parameters[1]
            record['tcp_2'] = parameters[2]
            record['cbr_packet_size'] = parameters[3]
            record['cbr_bandwidth'] = parameters[4]
            record['start_time_diff'] = parameters[5]

            file = os.path.join(results_folder, file)
            simulation_records = read_records_from_file(file)
            record['throughput_1'] = calculate_throughput(simulation_records, '0', '3')
            record['throughput_2'] = calculate_throughput(simulation_records, '4', '5')
            record['drop_rate_1'] = calculate_drop_rate(simulation_records, '0', '3')
            record['drop_rate_2'] = calculate_drop_rate(simulation_records, '4', '5')
            record['rtt_1'] = calculate_rtt(simulation_records, '0', '3')
            record['rtt_2'] = calculate_rtt(simulation_records, '4', '5')
            writer.writerow(record)
