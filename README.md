# An empirical study of static bug checkers and how many bugs do they find.

*Static bug detection tools* such as Google's [Error Prone](https://errorprone.info/),
Facebook's [Infer](http://fbinfer.com), and [SpotBugs](https://spotbugs.github.io/)
are widely used nowadays not only by academic researchers but also by major
software development companies and in general by developers in various
industries.

As such tools are becoming more and more famous and widely adopted, we
performed an empirical study on the **recall** of these three state-of-the-art
static bug checkers using a representative set of 594 real world Java bugs from
15 popular projects. In other words, our study answers the question of *how many
of a set of known bugs do these static checkers find* in reality.

This work is detailed and published in our ASE 2018 paper:

    How Many of All Bugs Do We Find? A Study of Static Bug Detectors.
    Andrew Habib and Michael Pradel.
    In Proceedings of the 33rd ACM/IEEE International Conference on Automated Software Engineering (ASE),
    pp. 317-328. ACM, 2018.

This repository contains the source code of the analysis pipeline we implemented
to perform our study. It is intended to be used to replicate our study results
and to perform further similar studies.

Also, the repository includes more elaborate results on our findings in the
ASE 2018 paper.

## Requirements to install and run

- ### Our scripts
  - `bash`
  - `curl` (on Linux, use `apt-get install curl`)
  - `wget` (on MacOS, if you have [brew](https://brew.sh/), use `brew install wget`)
  - `python 3` (also `joblib` is required. Use `pip3 install joblib`)

  - *For MacOS users*, `coreutils` is required too. Use `brew install coreutils`

  - Based on our testing, `Java 8` is the most compatible with the static analyzers 
  and Defects4J framework.

- ### 3rd party tools
  - [Defects4J](https://github.com/rjust/defects4j) requirements has to be met.

## Repository structure and contents

Study results:

- [`./results/`](results)
contains tables, figures, and charts detailing the findings of our study. You
will find more data available in this folder than what is in the ASE2018 paper
due to space limitation while publishing the paper.

**All ``bash`` and ``python`` scripts have descriptive names.**

- [`./scripts/`](scripts)
contains the driver script `do_study.sh` which runs the entire study
pipeline. This directory also contains modular scripts to run many parts of the
study separately provided that the specific scripts requirements are met.
*All scripts in this directory should be run from the top level of the
repository ```./``` and not from the ```./scritps/``` itself.*

- [`./python/`](python)
contains all python scripts which perform the actual study steps such as
checking out the actual bugs from Defects4J, running the static analyzers
on the bugs set, analyzing the checkers output, ..., etc. These python scripts
are called by the driver scripts in `./scripts/`. But they also could be
called directory by providing the appropriate input for each script.

Running the entire study pipeline by invoking `./scripts/do_study.sh` would
create three more directories in the top level `./`:

- `./static-checkers/`
contains the downloaded binaries of three static checkers we use
in the study: [Error Prone](https://errorprone.info/), [Infer](http://fbinfer.com),
and [SpotBugs](https://spotbugs.github.io/).

- `./defects4j/`
contains the cloned [Defects4J](https://github.com/rjust/defects4j) framework.
In this directory, our scripts also create the following sub-directories:
  - `./defects4j/projects/{b,f}` which contain the checked out (b)uggy
  and (f)ixed versions of each benchmark in the Defects4J bug set.

- `./study`
contains output from all study steps such as the logs and output of Running
the static analyzers on the bug set, the line diffs between buggy and fixed
versions, the pairs of warnings and bugs obtained from the different matching
methodologies we explain in the paper, and so on. It has two sub-directories
for the output of running the checkers on buggy and fixed versions from the
benchmark respectively:
  - `./study/output-buggy/`
  - `./study/output-fixed/`

**Important Note:**
In our study, we used an unofficial version from the Defects4J through a pull
request (pr) [#112](https://github.com/rjust/defects4j/pull/112) to obtain more
data (596 bugs instead of 395 bugs in the official release).
Unfortunately, this pull request is not clean and many of the new bug instances
included in it have wrong values for Defects4J properties. We had to identify
and fix those issues manually in an adhoc manner.
Therefore currently, if you use the exact same pull request, you will not obtain
the same results because some of the benchmarks will not be analyzed correctly.
We will create our own snapshot of the Defects4J along with the pull request
we used in our study and the corrected issues so that reproducing our results is
easier to achieve.
