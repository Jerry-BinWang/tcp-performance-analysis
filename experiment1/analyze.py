#!/usr/bin/env python3

import os
import csv

"""
    NS trace file format:
    | 0     | 1    | 2         | 3       | 4        | 5        | 6     | 7   | 8        | 9        | 10      | 11     |
    |-------|------|-----------|---------|----------|----------|-------|-----|----------|----------|---------|--------|
    | event | time | from node | to node | pkt type | pkt size | flags | fid | src addr | dst addr | seq num | pkt id |
    For more information: https://www.tablesgenerator.com/markdown_tables
"""


def is_pkt_send_event(record):
    return record[0] == '+' and record[2] == '0' and record[3] == '1'

def is_pkt_recv_event(record):
    return record[0] == 'r' and record[2] == '2' and record[3] == '3'

def is_ack_send_event(record):
    return record[0] == '+' and record[2] == '3' and record[3] == '2'

def is_ack_recv_event(record):
    return record[0] == 'r' and record[2] == '1' and record[3] == '0'

def get_time(record):
    return float(record[1])

def get_packet_bits(record):
    return 8 * int(record[5])

def read_records_from_file(file):
    records = []

    with open(file) as fin:
        for line in fin:
            record = line.strip().split()
            if len(record) == 12:
                records.append(record)

    return records


def calculate_throughput(records):
    start_time = None

    for record in records:
        if is_pkt_send_event(record):
            start_time = get_time(record)
            break
    
    end_time = None
    received_bits = 0
    seen_seq = set()
    for record in records:
        if is_pkt_recv_event(record) and record[10] not in seen_seq:
            received_bits += get_packet_bits(record)
            seen_seq.add(record[10])
            end_time = get_time(record)
    
    return (received_bits / (end_time - start_time)) / 1e6


def calculate_drop_rate(records):
    sent_pkt_num = 0
    received_pkt_num = 0

    for record in records:
        if is_pkt_send_event(record):
            sent_pkt_num += 1
        elif is_pkt_recv_event(record):
            received_pkt_num += 1

    return ((sent_pkt_num - received_pkt_num) / sent_pkt_num) * 100


def calculate_rtt(records):
    tcp_id_send_time_map = {}
    tcp_recv_time_id_map = {}
    ack_id_send_time_map = {}

    sum = 0.0
    n = 0

    for record in records:
        pkt_id = record[11]
        seq_id = record[10]
        if is_pkt_send_event(record):
            tcp_id_send_time_map[pkt_id] = get_time(record)
        elif is_pkt_recv_event(record):
            tcp_recv_time_id_map[get_time(record)] = pkt_id
        elif is_ack_send_event(record):
            ack_id_send_time_map[pkt_id] = get_time(record)
        elif is_ack_recv_event(record):
            tcp_pkt_id = tcp_recv_time_id_map.get(ack_id_send_time_map.get(pkt_id))
            sum += get_time(record) - tcp_id_send_time_map[tcp_pkt_id]
            n += 1

    return sum / n

if __name__ == '__main__':
    results_folder = 'results/'
    with open('result.csv', 'w') as fout:
        field_names = ['latency', 'tcp', 'cbr_packet_size', 'cbr_bandwidth', 'start_time_diff', 'throughput', 'drop_rate', 'rtt']
        writer = csv.DictWriter(fout, fieldnames= field_names)
        writer.writeheader()
        for file in os.listdir(results_folder):
            parameters = file.split('_')
            print(parameters)
            record = {}
            record['latency'] = parameters[0]
            if parameters[1] == 'TCP':
                record['tcp'] = 'Tahoe'
            else:
                record['tcp'] = parameters[1]
            record['cbr_packet_size'] = parameters[2]
            record['cbr_bandwidth'] = parameters[3]
            record['start_time_diff'] = parameters[4]

            file = os.path.join(results_folder, file)
            simulation_records = read_records_from_file(file)
            record['throughput'] = calculate_throughput(simulation_records)
            record['drop_rate'] = calculate_drop_rate(simulation_records)
            record['rtt'] = calculate_rtt(simulation_records)
            writer.writerow(record)
