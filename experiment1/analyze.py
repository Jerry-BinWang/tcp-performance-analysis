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
    return (record[0] == 'r' or record[0] == '+') and record[2] == '0' and record[3] == '1'


def is_pkt_recv_event(record):
    return (record[0] == 'r' or record[1] == '-') and record[2] == '2' and record[3] == '3'


def get_time(record):
    return float(record[1])


def read_records_from_file(file):
    records = []

    with open(file) as fin:
        for line in fin:
            record = line.strip().split()
            records.append(record)

    return records


def calculate_throughput(records):
    start_time = None
    end_time = None
    received_pkt_num = 0

    for record in records:
        if is_pkt_send_event(record):
            if start_time is None:
                start_time = get_time(record)
        elif is_pkt_recv_event(record):
            end_time = get_time(record)
            received_pkt_num += 1

    return received_pkt_num / (end_time - start_time)


def calculate_drop_rate(input_file):
    sent_pkt_num = 0
    received_pkt_num = 0

    for record in records:
        if is_pkt_send_event(record):
            sent_pkt_num += 1
        elif is_pkt_recv_event(record):
            received_pkt_num += 1

    return (sent_pkt_num - received_pkt_num) / sent_pkt_num


def calculate_latency(input_file):
    # TODO
    return 0


if __name__ == '__main__':
    input_file = sys.argv[1]
    records = read_records_from_file(input_file)
    print(calculate_throughput(records))
    print(calculate_drop_rate(records))
