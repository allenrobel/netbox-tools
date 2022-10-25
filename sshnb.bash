#!/usr/bin/env bash
# Name: sshnb.bash
# Description: ssh to a device using Netbox to resolve the device's name into the primary_ip
DEVICE=$1
SCRIPT="${HOME}/prod-netbox-tools/device_print_mgmt_ip.py"
ssh admin@`${SCRIPT} --device $1`
