#!/bin/sh
set -e
echo "Test 1: single coder should burn out"
./codexion 1 200 50 50 50 1 10 fifo | sed -n '1,5p'
echo
echo "Test 2: two coders each compile once and exit"
./codexion 2 800 200 200 200 1 50 fifo | sed -n '1,20p'
