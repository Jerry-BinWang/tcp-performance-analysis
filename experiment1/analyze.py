#!/usr/bin/env python3

import sys

"""
    NS trace file format:
    | 0     | 1    | 2         | 3       | 4        | 5        | 6     | 7   | 8        | 9        | 10      | 11     |
    |-------|------|-----------|---------|----------|----------|-------|-----|----------|----------|---------|--------|
    | event | time | from node | to node | pkt type | pkt size | flags | fid | src addr | dst addr | seq num | pkt id |
    For more information: https://www.tablesgenerator.com/markdown_tables
"""


def is_pkt_send_event(record):
    return record[0] == '+' and record[2] == '0' and record[3] == '1' and record[4] == 'tcp'

def is_pkt_recv_event(record):
    return record[0] == 'r' and record[2] == '2' and record[3] == '3' and record[4] == 'tcp'

def is_ack_recv_event(record):
    return record[0] == 'r' and record[2] == '1' and record[3] == '0' and record[4] == 'ack'

def get_time(record):
    return float(record[1])

def get_packet_bits(record):
        return 8 * int(record[5])

def read_records_from_file(file):
    records = []

    with open(file) as fin:
        for line in fin:
            record = line.strip().split()
            if record[4] != 'cbr':
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

    return (sent_pkt_num - received_pkt_num) / sent_pkt_num


def calculate_latency(records):
    send_times = {}
    sum = 0.0
    n = 0

    for record in records:
        if is_pkt_send_event(record):
            send_times[record[10]] = get_time(record)
        elif is_ack_recv_event(record) and record[10] in send_times:
            sum += get_time(record) - send_times.pop(record[10])
            n += 1

    return sum / n

if __name__ == '__main__':
    input_file = sys.argv[1]
    records = read_records_from_file(input_file)
    for record in records:
        assert len(record) == 12, print(record)
    print(calculate_throughput(records))
    print(calculate_drop_rate(records))
    print(calculate_latency(records))
