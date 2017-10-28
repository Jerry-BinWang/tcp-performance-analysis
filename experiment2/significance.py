import os

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

if __name__ == '__main__':
    results_folder = 'Newreno_vegas'
    with open('Newreno_vegas    .out', 'w') as fout:
        for file in os.listdir(results_folder):
            parameters = file.split('_')
            print(parameters)
            tcp_1 = parameters[1]
            tcp_2 = parameters[2]

            file = os.path.join(results_folder, file)
            simulation_records = read_records_from_file(file)
            throughput_1 = calculate_throughput(simulation_records, '0', '3')
            throughput_2 = calculate_throughput(simulation_records, '4', '5')
            print('{},{}'.format(tcp_1+'/'+tcp_2, throughput_1/throughput_2), file=fout)


