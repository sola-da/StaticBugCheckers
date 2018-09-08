## Scripts to perform the static checkers study steps.

**Note:**
*Scripts in this directory should be run from the top level of the
repository `./` and not from the `./scritps/` itself.*

### Contents:

- `config.sh`
Contains constants defining several directories names. This
script is `source`'d in all other scripts.

- `do_study.sh`
The entry point to perform the entire study.

The following scripts are in the order at which they are called from
`do_study.sh`. Moreover, each is self contained and could be run separately
provided that, its dependencies on previous steps are met (e.g., running `run_checkers_on_defects4j.sh` assumes the checkers and the defects4j data set
are already available in the relevant directories).

- `download_static_checkers.sh`
downloads and extracts binaries of the static checkers we used in our study. The installation is local and not system wide and should not affect/interact with
any other system-wide installations. It is configured to use the exact versions
used in our study but it is straightforward to use other versions by changing each_tool_VER variable in the script. This script creates the top level
directory `./static-checkers/`.

- `download_defects4j.sh`
downloads and initializes the defects4j framework. It is configured to use the
specific pull request (pr) [#112](https://github.com/rjust/defects4j/pull/112)
used in our study but you can change this. If you comment out the D4J_PR
variable, then the study will be done on the most recent official release of the Defects4J. Or, you could try different pull requests which also add more data
points to the Defects4J, e.g., pr [#112](https://github.com/rjust/defects4j/pull/112)
or pr [#174](https://github.com/rjust/defects4j/pull/174). This script creates
the top level directory `./defects4j/` and the directories
`./defects4j/projects/{b,f}`.

- `run_checkers_on_defects4j.sh`
runs the three static checkers on the buggy and fixed versions of instances in
the Defects4J. This script creates the top level directory `./study/` which
contains the two directories `./study/output_{buggy,fixed}`. Each of those two directories contain the output and a consolidated log of running each static
checker on each bug instance (and its fixed version) in the data set.

- `prepare_checkers_output.sh`
parses the static checkers output and prepares json files for the consolidated
output of each checker. The output from this script is single json file per tool
 in `./study/output_{buggy,fixed}/`.

- `execute_diff_based_approach.sh`
performs the diff-based automated matching approach to match warnings and lines
of code in the diff between the buggy and fixed versions of a bug.

- `execute_warnings_based_approach.sh`
performs the fixed warnings-based automated matching approach to match warnings
and bugs based on warnings which have disappeared (a.k.a removed) between
the buggy and fixed versions of a bug.
