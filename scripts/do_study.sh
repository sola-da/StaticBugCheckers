#!/bin/bash

# Author: Andrew Habib
# Created on: 31 August 2018

source ./scripts/config.sh

echo
echo "**********************************************************************************************"
echo "Running the study of static bug checkers and their effectiveness by Habib and Pradel [ASE2018]"
echo "**********************************************************************************************"

bash ./scripts/download_static_checkers.sh

bash ./scripts/download_defects4j.sh

bash ./scripts/run_checkers_on_defects4j.sh

bash ./scripts/prepare_checkers_output.sh

bash ./scripts/execute_diff_based_approach.sh

bash ./scripts/execute_warnings_based_approach.sh

echo
echo "*************************"
echo "Done performing the study"
echo "*************************"
echo
echo "Check the results in:"
echo $STUDY_ROOT
echo
