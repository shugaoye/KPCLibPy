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
            for group in ctx.keepass.get_groups(path):
                print("{}/".format(group))
            for entry in ctx.keepass.get_entries(path):
                print("{}".format(entry))
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
        print(ctx.keepass.current_group.get_Name())


@command
@argument("path", description="enter a path", positional=True)
def cd(path: str):
    """
    Change directory (group), '/' - root, '..' - parent
    """
    ctx = context.get_context()
    if ctx.keepass.is_open():
        try:
            if path == '/':
                ctx.keepass.current_group = ctx.keepass.root_group
            elif path == '..':
                ctx.keepass.current_group = ctx.keepass.current_group.ParentGroup
            elif ctx.keepass.groups[path]:
                ctx.keepass.current_group = ctx.keepass.groups[path]
        except KeyError:
            cprint("Cannnot find {}".format(path), "red")


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