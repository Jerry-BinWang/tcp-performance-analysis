import os
import math
import csv

results_folder = 'results/'
to_folder = 'time/'

def is_packet_recv_event(record):
    return record[0] == 'r' and record[2] == '2' and record[3] == '3'

def get_time(record):
    return float(record[1])

def get_packet_bits(record):
    return 8 * int(record[5])

def calculate_metrics_over_time(file):
    sec_received_bits_map = {}
    maxseq = {}
    cwnd = {}
    with open(file) as fin:
        for line in fin:
            tokens = line.strip().split()
            if len(tokens) == 12:
                if is_packet_recv_event(tokens):
                    sec = int(math.ceil(get_time(tokens)))
                    received_bits = get_packet_bits(tokens)
                    sec_received_bits_map[sec] = sec_received_bits_map.setdefault(sec, 0) + received_bits
            else:
                time = float(tokens[0])
                if tokens[5] == 'maxseq_':
                    value = int(tokens[6])
                    maxseq[time] = value
                elif tokens[5] == 'cwnd_':
                    value = float(tokens[6])
                    cwnd[time] = value

    metrics = []
    for sec in sec_received_bits_map:
        metrics.append({'metric': 'throughput',
                        'time': sec,
                        'value': sec_received_bits_map[sec]/1e6})
    for time in maxseq:
        metrics.append({'metric': 'maxseq',
                        'time': time,
                        'value': maxseq[time]})
    for time in cwnd:
        metrics.append({'metric': 'cwnd',
                        'time': time,
                        'value': cwnd[time]})
    return metrics

if __name__ == '__main__':
    for input_file in os .listdir(results_folder):
        print(input_file)
        output_file = input_file.split('.')[0]+'.csv'
        input_file = os.path.join(results_folder, input_file)
        output_file = os.path.join(to_folder, output_file)
        metrics = calculate_metrics_over_time(input_file)
        with open(output_file, 'w') as fout:
            fieldnames = ['metric', 'time', 'value']
            writer = csv.DictWriter(fout, fieldnames=fieldnames)
            writer.writeheader()
            for metric in metrics:
                writer.writerow(metric)