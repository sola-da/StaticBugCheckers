#!/bin/bash

# Author: Andrew Habib
# Created on: 31 August 2018

[[ ! "${#BASH_SOURCE[@]}" -gt "1" ]] && { source ./scripts/config.sh; }

echo
echo ">>> Computing diffs between buggy and fixed versions in the Defects4j <<<"
(cd ${STUDY_ROOT} \
	&& python3 ${PY_SCRIPTS_ROOT}/ExtractAndSerializeDiffs.py $D4J_BUGGY $D4J_FIXED > /dev/null 2>&1 \
)

echo
echo ">>> Executing the Diff-based methodology: intersect diffs with flagged lines <<<"
(cd ${STUDY_ROOT} \
	&& python3 ${PY_SCRIPTS_ROOT}/CompareDiffsToErrorprone.py $DIFFS_FILE ${OUT_BUGGY}/ep_parsed.json \
	&& python3 ${PY_SCRIPTS_ROOT}/CompareDiffsToInfer.py $DIFFS_FILE ${OUT_BUGGY}/inf_parsed.json \
	&& python3 ${PY_SCRIPTS_ROOT}/CompareDiffsToSpotbugs.py $DIFFS_FILE ${OUT_BUGGY}/sb_parsed.json \
)
