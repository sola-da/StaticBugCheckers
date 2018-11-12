#!/bin/bash

# Author: Andrew Habib
# Created on: 31 August 2018

[[ ! "${#BASH_SOURCE[@]}" -gt "1" ]] && { source ./scripts/config.sh; }

if [ -d ${D4J_ROOT} ]; then rm -rf ${D4J_ROOT}; fi
echo
echo ">>> Downloading the Defects4J framework <<<"

git clone -q https://github.com/rjust/defects4j.git

# This is the original pull request (pr) #112 used in the study.
# However, many of the additional projects (not in the official d4j), have wrong d4j properties
# and they don't compile right away. For the study, we have manually fixed all these errors.
# But adding our ad-hoc fixes to the pr is not easy and is not our goal as it is unofficial anyways.
# One alternative is to either restrict the reproduction to the original d4j.
# Or use a different and more recent (hopefully cleaner) pull requests such as pr #174

# NOTE: depending on which version is used, python/CheckoutD4j.py should be updated accordingly.
# as it now has the list of Defects projects identifiers and number of bugs encoded manually.

D4J_PR="112"	# Comment out this line to use the most recent official release of the Defects4J.
							# Look at the note above. Don't forget to update python/CheckoutD4j.py.

if [ $D4J_PR ]
then
	echo ">>> Switching from master to pr #${D4J_PR}"
	(cd $D4J_ROOT \
		&& git fetch -q origin pull/${D4J_PR}/head:extendedD4J \
		&& git checkout -q extendedD4J \
	)
fi

echo ">>> Initializing the framework"
echo
(cd $D4J_ROOT \
	&& ./init.sh
	# && ./init.sh > /dev/null 2>&1 \
)
echo

echo ">>> Checking out and compiling the dataset"
echo

echo ">>> Checking out buggy versions to:"
# python3 ${PY_SCRIPTS_ROOT}/CheckoutD4j.py ${D4J_ROOT} b ${JOBS} > /dev/null 2>&1
python3 ${PY_SCRIPTS_ROOT}/CheckoutD4j.py ${D4J_ROOT} b ${JOBS}
echo
echo ">>> Checking out fixed versions to:"
# python3 ${PY_SCRIPTS_ROOT}/CheckoutD4j.py ${D4J_ROOT} f ${JOBS} > /dev/null 2>&1
python3 ${PY_SCRIPTS_ROOT}/CheckoutD4j.py ${D4J_ROOT} f ${JOBS}

# Hack to force compiling all d4j projects
#python3 ${PY_SCRIPTS_ROOT}/TryAllCompileD4J.py ${D4J_ROOT}/b $JOBS
#python3 ${PY_SCRIPTS_ROOT}/TryAllCompileD4J.py ${D4J_ROOT}/f $JOBS
