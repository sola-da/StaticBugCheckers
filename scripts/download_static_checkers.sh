#!/bin/bash

# Author: Andrew Habib
# Created on: 31 August 2018

[[ ! "${#BASH_SOURCE[@]}" -gt "1" ]] && { source ./scripts/config.sh; }

# This is the ErrorProne release used in the study.
EP_VER="2.1.1"
EP_URL="https://repo1.maven.org/maven2/com/google/errorprone/error_prone_ant/${EP_VER}/error_prone_ant-${EP_VER}.jar"
# You can instead any other version by setting EP_VER accordingly.
# NOTE: EP_ROOT= the downloaded Error Prone ant jar.


# This is the Infer release used in the study.
# INF_VER="0.13.0"
# But it does not come with ready binary. It requires manual build
# and meeting all Infer dependencies. This is cumbersome but doable.
# NOTE for 0.13.0: INF_BIN: INF_ROOT/infer/bin/infer
# So instead, we use a more recent Infer release, which has a ready-made binary.
# And according to documentation, the newer release did not have any major changed
# to the Java checkers. So we expect more or less the same effectiveness in Java
# bug detetction.
INF_VER="0.15.0"
# NOTE for 0.15.0: INF_BIN=INF_ROOT/bin/infer
# Make sure to update $INF_BIN accordingly.


# This is the SpotBugs release used for the study.
SB_VER="3.1.0"
SB_URL="http://repo.maven.apache.org/maven2/com/github/spotbugs/spotbugs/${SB_VER}/spotbugs-${SB_VER}.tgz"
# NOTE: SB_BIN=SB_ROOT/lib/spotbugs.jar

if [ -d ${CHECKERS_ROOT} ]; then rm -rf ${CHECKERS_ROOT}; fi
mkdir $CHECKERS_ROOT

echo
echo ">>> Downloading and extracting static checkers <<<"

echo ">>> Preparing Google's ErrorProne"
(cd $CHECKERS_ROOT && wget -q $EP_URL)

# Infer has different binaries for Linux and MacOS
echo ">>> Preparing Facebook's Infer"
if [ $MACHINE = "Linux" ]; then
  INF_URL="https://github.com/facebook/infer/releases/download/v${INF_VER}/infer-linux64-v${INF_VER}.tar.xz"
  curl -sSL $INF_URL | tar -C $CHECKERS_ROOT -xJ
elif [ $MACHINE = "Mac" ]; then
  INF_URL="https://github.com/facebook/infer/releases/download/v${INF_VER}/infer-osx-v${INF_VER}.tar.xz"
  curl -sSL $INF_URL | tar -C $CHECKERS_ROOT -x
else
  echo "Reporting from script: $(basename $BASH_SOURCE) at line: $LINENO"
  echo "Uknown OS: $MACHINE"
  echo "Cann't get compatible Infer version"
  echo "Will exit..."
  exit 1
fi

echo ">>> Preparing SpotBugs"
wget -cq $SB_URL -O - | tar -xz -C $CHECKERS_ROOT
