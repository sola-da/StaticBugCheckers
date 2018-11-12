#!/bin/bash

# Author: Andrew Habib
# Created on: 31 August 2018

# Defining various paths used by our scripts

export CHECKERS_ROOT="$PWD/static-checkers"

export D4J_ROOT="$PWD/defects4j"
export D4J_BUGGY="${D4J_ROOT}/projects/b"
export D4J_FIXED="${D4J_ROOT}/projects/f"

export PY_SCRIPTS_ROOT="$PWD/python"

export STUDY_ROOT="$PWD/study"
export OUT_BUGGY="${STUDY_ROOT}/output-buggy"
export OUT_FIXED="${STUDY_ROOT}/output-fixed"
export DIFFS_FILE="${STUDY_ROOT}/diffs_parsed.json"

# Find out which os am I running on
unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*)     MACHINE=Linux;;
    Darwin*)    MACHINE=Mac;;
    CYGWIN*)    MACHINE=Cygwin;;
    MINGW*)     MACHINE=MinGw;;
    *)          MACHINE="UNKNOWN:${unameOut}"
esac
export $MACHINE

# Use 2/3 of the number of available cores
# Ubuntu-like OS:
if [ $MACHINE = "Linux" ]; then
  JOBS=$((`grep -c ^processor /proc/cpuinfo` * 2/3))
elif [ $MACHINE = "Mac" ]; then
  JOBS=$((`sysctl -n hw.ncpu` * 2/3))
else
  JOBS=`python -c 'import multiprocessing as mp; print(mp.cpu_count()*2/3)'`
fi
export $"JOBS"
