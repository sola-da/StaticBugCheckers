#!/bin/bash

# Author: Andrew Habib
# Created on: 31 August 2018

export CHECKERS_ROOT="$PWD/static-checkers"

export D4J_ROOT="$PWD/defects4j"
export D4J_BUGGY="${D4J_ROOT}/projects/b"
export D4J_FIXED="${D4J_ROOT}/projects/f"

export PY_SCRIPTS_ROOT="$PWD/python"

export STUDY_ROOT="$PWD/study"
export OUT_BUGGY="${STUDY_ROOT}/output-buggy"
export OUT_FIXED="${STUDY_ROOT}/output-fixed"
export DIFFS_FILE="${STUDY_ROOT}/diffs_parsed.json"

export JOBS=$((`grep -c ^processor /proc/cpuinfo` * 2/3))
