#!/usr/local/bin/python3.8
# -*- coding: utf-8 -*-
# @FileName: inventory.py
# @author: Cold Cat
# @date: 2020/12/28


import argparse
from ruamel.yaml import YAML

parser = argparse.ArgumentParser(description="Generate ansible inventory hosts.yaml configuration file.")
parser.add_argument('-m', '--masters', nargs='+', help='kubernetes master node hosts', required=True)
parser.add_argument('-n', '--nodes', nargs='+', help='kubernetes worker node hosts')
args = parser.parse_args()

master_hosts = args.masters
node_hosts = args.nodes
master_hostname = []
node_hostname = []

yaml = YAML()


def generate_master_names():
    if len(master_hosts) == 1:
        master_hostname.append("master")
        return
    for i in range(len(master_hosts)):
        master_hostname.append("master" + str(i + 1))


def generate_node_names():
    if node_hosts is not None:
        if len(node_hosts) == 1:
            node_hostname.append("node")
            return
        for i in range(len(node_hosts)):
            node_hostname.append("node" + str(i + 1))


def convert_list_to_none_dict(hosts):
    return dict(zip(hosts, [None] * len(hosts)))


def generate_inventory_json_to_yaml():
    all_hosts = {}

    for i, host in enumerate(master_hosts):
        all_hosts[master_hostname[i]] = {"ansible_host": host}

    inventory = {"all": {"hosts": all_hosts,
                         "children": {"k8s_master": {"hosts": convert_list_to_none_dict(master_hostname)}}}}

    if node_hosts is not None:
        for i, host in enumerate(node_hosts):
            all_hosts[node_hostname[i]] = {"ansible_host": host}
        inventory['all']['children']['k8s_node'] = {"hosts": convert_list_to_none_dict(node_hostname)}

    with open('./inventory/hosts.yaml', mode='w', encoding='utf-8') as f:
        yaml.dump(inventory, f)


if __name__ == '__main__':
    generate_master_names()
    generate_node_names()
    generate_inventory_json_to_yaml()
