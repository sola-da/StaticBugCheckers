#!/bin/bash

# Author: Andrew Habib
# Created on: 31 August 2018

[[ ! "${#BASH_SOURCE[@]}" -gt "1" ]] && { source ./scripts/config.sh; }

echo
echo ">>> Executing the Removed warnings-based methodology: find removed (a.k.a disappeared) warnings <<<"
(cd ${STUDY_ROOT} \
	&& python3 ${PY_SCRIPTS_ROOT}/CompareBugToFixErrorprone.py ${OUT_BUGGY}/ep_parsed.json ${OUT_FIXED}/ep_parsed.json \
	&& python3 ${PY_SCRIPTS_ROOT}/CompareBugToFixInfer.py ${OUT_BUGGY}/inf_parsed.json ${OUT_FIXED}/inf_parsed.json \
	&& python3 ${PY_SCRIPTS_ROOT}/CompareBugToFixSpotbugs.py ${OUT_BUGGY}/sb_parsed.json ${OUT_FIXED}/sb_parsed.json \
)