#!/usr/bin/env bash

# Some distro requires that the absolute path is given when invoking lspci
# e.g. /sbin/lspci if the user is not root.
gpu=$(lspci | grep -i '.* vga .* nvidia .*')

shopt -s nocasematch

if [[ $gpu == *' nvidia '* ]]; then
  printf 'Nvidia GPU is present:  %s\n' "$gpu"
  sudo docker-compose -f docker-compose-gpu.yml up -d
else
  printf 'Nvidia GPU is not present: %s\n' "$gpu"
  sudo docker-compose -f docker-compose-cpu.yml up -d
fi