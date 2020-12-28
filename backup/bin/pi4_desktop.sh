#!/bin/bash

Xephyr -br -ac -noreset -screen 1900x1020 :1 &
pid=$!

ssh -X pi4 "DISPLAY=:1 startx"

kill -9 $pid
