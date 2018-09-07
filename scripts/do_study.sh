#!/bin/bash

# Author: Andrew Habib
# Created on: 31 August 2018

source ./scripts/config.sh

echo 

bash ./scripts/download_static_checkers.sh

bash ./scripts/download_defects4j.sh

bash ./scripts/run_checkers_on_defects4j.sh

bash ./scripts/prepare_checkers_output.sh

bash ./scripts/execute_diff_based_approach.sh

bash ./scripts/execute_warnings_based_approach.sh

echo