#!/usr/bin/env python3

# Copyright (c) Roger Ye.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#

import typing
#from pathlib import *
from termcolor import cprint
from nubia import command, argument, context
#from commands.keepass import KeePass, IStatusLogger, get_homepath, lsdb


@command
@argument("path", description="a specified path", positional=False)
def ls(path=""):
    "Lists entries or groups in pwd or in a specified path"
    ctx = context.get_context()
    if ctx.keepass.is_open():
        if path:
            current_group = ctx.keepass.find_group_by_path(path)
            if current_group:
                for group in current_group.Groups:
                    print("{}/".format(group.get_Name()))
                for entry in current_group.Entries:
                    print("{}".format(entry.Strings.ReadSafe("Title")))
            else:
                entry = ctx.keepass.find_entry_by_path(path)
                if entry:
                    print("{}".format(entry.Strings.ReadSafe("Title")))
                else:
                    print("cannot access {}: No such file or directory".format(path))
        else:
            for group in ctx.keepass.groups:
                print("{}/".format(group))
            for entry in ctx.keepass.entries:
                print("{}".format(entry))


@command
def pwd():
    "Print the current working directory"
    ctx = context.get_context()
    if ctx.keepass.is_open():
        print(ctx.keepass.db.CurrentPath)


@command
@argument("path", description="enter a path", positional=True)
def cd(path: str):
    """
    Change directory (group), '/' - root, '..' - parent
    """
    ctx = context.get_context()
    if ctx.keepass.is_open():
        if path == '/':
            ctx.keepass.current_group = ctx.keepass.root_group
        else:
            group = ctx.keepass.find_group_by_path(path)
            if group:
                ctx.keepass.current_group = group
            else:
                cprint("Cannnot find {}".format(path), "yellow")


@command
@argument("group_name", description="enter a group name", positional=True)
def mkdir(group_name: str):
    "Create a new directory (group)"
    ctx = context.get_context()
    if ctx.keepass.is_open():
        new_group = ctx.keepass.current_group.FindCreateGroup(group_name, False)
        if new_group:
            cprint("{} already exist.".format(new_group))
        else:
            new_group = ctx.keepass.current_group.FindCreateGroup(group_name, True)
            cprint("Created group {}".format(new_group))

@command
@argument("group_name", description="enter a group name", positional=True)
def rmdir(group_name: str):
    "Delete a directory (group)"
    ctx = context.get_context()
    if ctx.keepass.is_open():
        group = ctx.keepass.current_group.FindCreateGroup(group_name, False)
        if group:
            ctx.keepass.db.DeleteGroup(group)
            cprint("Removed {}.".format(group))
        else:
            cprint("rmdir: failed to remove {}: No such group.".format(group))
