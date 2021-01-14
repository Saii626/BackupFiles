#!/usr/bin/env sh

# i3bar appears in tree iff it is in dock mode.
if i3-msg -t get_tree | rg "\"class\":\"i3bar\"" ; then
    i3-msg bar mode hide
else
    i3-msg bar mode dock
fi
