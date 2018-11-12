#!/bin/bash

# Author: Andrew Habib
# Created on: 31 August 2018

[[ ! "${#BASH_SOURCE[@]}" -gt "1" ]] && { source ./scripts/config.sh; }

if [ $MACHINE = "Linux" ]; then
	get_abs_path() {
		readlink -f $1
	}
	INF_BIN="$(get_abs_path `find ${CHECKERS_ROOT} -maxdepth 1 -type d -name infer-linux*`)/bin/infer"
elif [ $MACHINE = "Mac" ]; then
	get_abs_path() {
		greadlink -f $1
	}
	INF_BIN="$(get_abs_path `find ${CHECKERS_ROOT} -maxdepth 1 -type d -name infer-osx*`)/bin/infer"
else
	echo "Reporting from script: $(basename $BASH_SOURCE) at line: $LINENO"
	echo "Not sure how to get abs path of static analyzers given your OS: $MACHINE."
	echo "Add your OS equivalent of 'readlink -f' here"
	echo "Will exit..."
	exit 1
fi
EP_BIN=$(get_abs_path `find ${CHECKERS_ROOT} -name error_prone*.jar`)
SB_BIN="$(get_abs_path `find ${CHECKERS_ROOT} -maxdepth 1 -type d -name spotbugs*`)/lib/spotbugs.jar"

if [ -d ${STUDY_ROOT} ]; then rm -rf ${STUDY_ROOT}; fi
mkdir -p $OUT_BUGGY && mkdir -p $OUT_FIXED

echo
echo ">>> Running the static checkers on the buggy versions from the Defects4j <<<"
(cd $OUT_BUGGY \
	&& echo ">>> Running Error Prone" && python3 ${PY_SCRIPTS_ROOT}/RunErrorprone.py ${EP_BIN} ${D4J_BUGGY} $JOBS \
	&& echo ">>> Running Infer" && python3 ${PY_SCRIPTS_ROOT}/RunInfer.py ${INF_BIN} ${D4J_BUGGY} $JOBS \
	&& echo ">>> Running SpotBugs" && python3 ${PY_SCRIPTS_ROOT}/RunSpotbugs.py ${SB_BIN} ${D4J_BUGGY} $JOBS \
)

echo
echo ">>> Running the static checkers on the fixed versions from the Defects4j <<<"
(cd $OUT_FIXED \
	&& echo ">>> Running Error Prone" && python3 ${PY_SCRIPTS_ROOT}/RunErrorprone.py ${EP_BIN} ${D4J_FIXED} $JOBS \
	&& echo ">>> Running Infer" && python3 ${PY_SCRIPTS_ROOT}/RunInfer.py ${INF_BIN} ${D4J_FIXED} $JOBS \
	&& echo ">>> Running SpotBugs"	&& python3 ${PY_SCRIPTS_ROOT}/RunSpotbugs.py ${SB_BIN} ${D4J_FIXED} $JOBS \
)
