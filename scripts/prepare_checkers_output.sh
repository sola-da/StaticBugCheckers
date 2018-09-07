#!/bin/bash

# Author: Andrew Habib
# Created on: 31 August 2018

[[ ! "${#BASH_SOURCE[@]}" -gt "1" ]] && { source ./scripts/config.sh; }

echo
echo ">>> Parsing and serializing output from the static checkers <<<"

(cd $OUT_BUGGY \
	&& python3 ${PY_SCRIPTS_ROOT}/ParseAndSerializeErrorprone.py ep_output/ \
	&& python3 ${PY_SCRIPTS_ROOT}/ParseAndSerializeInfer.py inf_output_json/ \
	&& python3 ${PY_SCRIPTS_ROOT}/ParseAndSerializeSpotbugs.py sb_output/ \
)

(cd $OUT_FIXED \
	&& python3 ${PY_SCRIPTS_ROOT}/ParseAndSerializeErrorprone.py ep_output/ \
	&& python3 ${PY_SCRIPTS_ROOT}/ParseAndSerializeInfer.py inf_output_json/ \
	&& python3 ${PY_SCRIPTS_ROOT}/ParseAndSerializeSpotbugs.py sb_output/ \
)
