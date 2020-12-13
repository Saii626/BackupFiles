#!/usr/bin/env python3
import os, re
from subprocess import Popen, run, PIPE
from utils import run_rofi, notify

class Device:
    def __init__(self, model, revision, serial, device):
        self.model = model
        self.revision = revision
        self.serial = serial
        self.device = device

    def __repr__(self):
        return f'[Model: {self.model}, Revision: {self.revision}, Serial: {self.serial}, Device: {self.device}]'

class Partition:
    def __init__(self, partition, uuid, filetype, label=None, mount_point=None):
        self.partition = partition
        self.label = label
        self.uuid= uuid
        self.filetype = filetype
        self.mount_point = mount_point
        self.name = self.label if self.label else self.uuid

    def __repr__(self):
        return f'[partition: {self.partition}, UUID: {self.uuid}, Label: {self.label}, MountPoint: {self.mount_point}]'



def get_disk_status() -> [Device]:
    disk_status = run(['udisksctl', 'status'], capture_output=True, check=True)
    resp = disk_status.stdout.decode('utf-8')

    lines = resp.split('\n')
    devices = []

    for line in lines[2:]:
        if not line:
            continue

        tokens = line.split(' ')
        tokens = list(filter(lambda x: bool(x), tokens)) # Remove empty tokens
        devices.append(Device(' '.join(tokens[:-3]), tokens[-3], tokens[-2], tokens[-1]))

    return devices

def get_partition_status(device: Device) -> [Partition]:
    def get_block_device_info(name):
        disk_info = run(['udisksctl', 'info', '-b', f'/dev/{name}'], capture_output=True, check=True)
        return disk_info.stdout.decode('utf-8')

    resp = get_block_device_info(device.device)
    lines = resp.split('\n')
    partitions = []

    for line in lines:
        search = re.search('/org/freedesktop/UDisks2/block_devices/(.*\d)', line)

        if search:
            partition_name = search.group(1)

            partition_info = get_block_device_info(partition_name)
            label = re.search('IdLabel:(.*)', partition_info).group(1).strip()
            uuid = re.search('IdUUID:(.*)', partition_info).group(1).strip()
            filetype = re.search('IdType:(.*)', partition_info).group(1).strip()
            mount_point = re.search('MountPoints:(.*)', partition_info)

            if mount_point:
                mount_point = mount_point.group(1).strip()

            partitions.append(Partition(partition_name, uuid, filetype, label if label else None, mount_point if mount_point else None))

    return partitions

def mount_partition(partition: Partition):
    return run(['udisksctl', 'mount', '-b', f'/dev/{partition.partition}'], capture_output=True, check=True).stdout.decode('utf-8').strip()

def unmount_partition(partition: Partition):
    return run(['udisksctl', 'unmount', '-b', f'/dev/{partition.partition}'], capture_output=True, check=True).stdout.decode('utf-8').strip()

all_devices = get_disk_status()
selected_device = run_rofi(all_devices, 'Device', lambda d: d.model)

if selected_device is not None:
    partitions = get_partition_status(selected_device)
    partitions.sort(key=lambda p: p.label if p.label else 'zzzzzzzzzzzzzzzzzzzzz')

    def option_name_generator(part: Partition):
        return f'{part.name}    ({part.mount_point if part.mount_point else "not mounted"})'

    selected_partition = run_rofi(partitions, 'Partition', option_name_generator)

    if selected_partition is not None:
        if selected_partition.mount_point:
            ret = unmount_partition(selected_partition)
            notify('Unmount successful', ret)
        else:
            ret = mount_partition(selected_partition)
            notify('Mount successful', ret)

