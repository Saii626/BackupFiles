#!/usr/bin/env python3

import os, re, json, pyperclip, traceback
from subprocess import run, Popen, PIPE
from utils import run_rofi, notify

class LPassItem:

    def __init__(self, group, name):
        self.group = group
        self.name = name
        self.ids = set()

        if self.group == '(none)':
            self.group = None

    def __hash__(self):
        return self.name.__hash__() * 31 + self.group.__hash__()

    def __eq__(self, o):
        return type(o) == LPassItem and o.name == self.name and o.group == self.group

    @classmethod
    def create_item_from_regex(cls, regex):
        if not hasattr(LPassItem, 'all_items'):
            LPassItem.all_items = set()

        (group, name, id) = (regex.group(1), regex.group(2), regex.group(3))
        temp_item = LPassItem(group, name)

        existing_item = list(filter(lambda x: x == temp_item, LPassItem.all_items))
        if len(existing_item) == 0:
            temp_item.ids.add(id)
            LPassItem.all_items.add(temp_item)
            return temp_item
        else:
            existing_item[0].ids.add(id)
            return existing_item[0]
    
    @staticmethod
    def get_all_lpass_items():
        return LPassItem.all_items

class LPassItemDetails:

    def __init__(self, id, fullname, username, password):
        self.id = id
        self.fullname = fullname
        self.username = username
        self.password = password

    def __repr__(self):
        return f'FName: {self.fullname}, UName: {self.username}'

def run_lpass_cli(args, check=True):
    cmd = run(['lpass', *args], capture_output=True, check=check)
    return cmd.stdout.decode('utf-8')

try:
    lpass_status = run_lpass_cli(['status'], check=False).strip()

    if lpass_status == 'Not logged in.':
        login = run_lpass_cli(['login', 'saikat626@gmail.com'])
        lpass_status = run_lpass_cli(['status']).strip()

    search = re.search('Logged in as (.*)\.', lpass_status)
    if search:
        username = search.group(1)

        pass_list = run_lpass_cli(['ls']).strip()

        for line in pass_list.split('\n'):
            line_parse = re.search('(.*)/(.*) \[id: (.*)\]', line)

            if line_parse:
                LPassItem.create_item_from_regex(line_parse)

        selected_item = run_rofi(LPassItem.get_all_lpass_items(), username, lambda x: x.name)

        def get_details_of_id(id):
            resp = run_lpass_cli(['show', '-j', id])
            resp = json.loads(resp)[0]
            return LPassItemDetails(resp["id"], resp["fullname"], resp["username"], resp["password"])

        selected_item_details = None

        if len(selected_item.ids) == 1:
            selected_item_details = get_details_of_id(selected_item.ids.pop())

        elif len(selected_item.ids) > 1:
            item_details = [get_details_of_id(id) for id in selected_item.ids]
            selected_item_details = run_rofi(item_details, f'{username}/{selected_item.name}', lambda x: x.username)

            if not selected_item_details:
                exit(0)

        options = ['Copy username to clipboard', 'Copy password to clipboard']
        selected_option = run_rofi(options, f'{username}/{selected_item_details.id}')

        if selected_option:
            if selected_option == options[0]:
                ret = selected_item_details.username
            else:
                ret = selected_item_details.password

            pyperclip.copy(ret)
except Exception as e:
    notify("LPass error", str(e))
    traceback.print_exc()
