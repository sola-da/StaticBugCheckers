# Original results published in the ASE2018 paper and more.

**Note 1:**
These results are based upon the specific version of Defects4J obtained through
pull request (pr) [#112](https://github.com/rjust/defects4j/pull/112).
Please see [here](../README.md).

**Note 2:**
We will use figures and tables numbers analogous to what is in the paper.

## Defects4J properties
In the following, we show some statistics about Defects4J bugs used in our study.

<image src="defects4j/hist_file-1.png" width=450/>
(a) Number of buggy files.


<image src="defects4j/hist_diff-1.png" width=450/>
(b) Total size of diffs between buggy and fixed files.


<image src="defects4j/hist_loc-1.png" width=450/>
(c) Total size of buggy files.


**Figure 3: Properties of the studied bugs.**

## Detected bugs
In the following, we first show the total number of bugs detected by each tool
and the overlap between the checkers. Then, we present extra tables showing
which bugs are detected by which static checker according to our findings.

### Bugs detected by the three tools together
<image src="found_bugs_all_tools-1.png" width=257 />

| Tool              | Number of bugs |
|-------------------|---------------:|
| SpotBugs          |             18 |
| Error Prone       |              8 |
| Infer             |              5 |
| **Total:**        |         **31** |
| **Total unique:** |         **27** |

**Figure 4: Total number of bugs found by all three static checkers and their
overlap.**


The following tables are not in the paper due to space limitation.
### Bugs detected by SpotBugs
| Count | Bug Id             | Bug type                                           | Message as reported by SpotBugs |
|------:|--------------------|----------------------------------------------------|---------------------------------|
|     1 | Chart-1            | NP_ALWAYS_NULL                                | Null pointer dereference of ? in org.jfree.chart.renderer.category.AbstractCategoryItemRenderer.getLegendItems()
|     2 | Chart-4            | NP_NULL_ON_SOME_PATH                          | Possible null pointer dereference of ? in org.jfree.chart.plot.XYPlot.getDataRange(ValueAxis)
|     3 | Chart-17           | CN_IDIOM_NO_SUPER_CALL                        | org.jfree.data.time.TimeSeries.clone() does not call super.clone()
|     4 | Chart-22           | UC_USELESS_CONDITION                          | Useless condition: it's known that local$3 >= 0 at this point
|     5 | Chart-24           | DLS_DEAD_LOCAL_STORE                          | Dead store to $L3 in org.jfree.chart.renderer.GrayPaintScale.getPaint(double)
|     6 | CommonsCodec-22    | SI_INSTANCE_BEFORE_FINALS_ASSIGNED            | Static initializer for org.apache.commons.codec.language.RefinedSoundex creates instance before all static final fields assigned
|     7 | JacksonDatabind-13 | NP_BOOLEAN_RETURN_NULL                        | com.fasterxml.jackson.databind.ser.std.EnumSerializer._isShapeWrittenUsingIndex(Class, JsonFormat$Value, boolean) has Boolean return type and returns explicit null
|     8 | JacksonDatabind-32 | VA_FORMAT_STRING_EXTRA_ARGUMENTS_PASSED       | Format-string method String.format(String, Object[]) called with format string "Can not construct Map key of type %s from String "%s": " wants 2 arguments but is given 3 in com.fasterxml.jackson.databind.DeserializationContext.weirdKeyException(Class, String, String)
|     9 | Jsoup-22           | UUF_UNUSED_PUBLIC_OR_PROTECTED_FIELD          | Unused public or protected field: org.jsoup.parser.TreeBuilder.currentToken
|    10 | Lang-3             | DLS_DEAD_LOCAL_STORE                          | Dead store to $L9 in org.apache.commons.lang3.math.NumberUtils.createNumber(String)
|    11 | Lang-23            | EQ_DOESNT_OVERRIDE_EQUALS                     | org.apache.commons.lang3.text.ExtendedMessageFormat doesn't override java.text.MessageFormat.equals(Object)
|    12 | Lang-56            | SE_BAD_FIELD                                  | Class org.apache.commons.lang.time.FastDateFormat defines non-transient non-serializable instance field mRules
|    13 | Lang-62            | SF_DEAD_STORE_DUE_TO_SWITCH_FALLTHROUGH       | Value of ? from previous case is overwritten here due to switch statement fall through
|       | Lang-62            | SF_SWITCH_NO_DEFAULT                          | Switch statement found in org.apache.commons.lang.Entities.unescape(Writer, String) where default case is missing
|    14 | Math-50            | FE_FLOATING_POINT_EQUALITY                    | Test for floating point equality in org.apache.commons.math.analysis.solvers.BaseSecantSolver.doSolve()
|    15 | Math-91            | CO_COMPARETO_INCORRECT_FLOATING               | org.apache.commons.math.fraction.Fraction.compareTo(Fraction) incorrectly handles double value
|    16 | Mockito-1          | DLS_DEAD_LOCAL_STORE                          | Dead store to $L2 in org.mockito.internal.invocation.InvocationMatcher.captureArgumentsFrom(Invocationi)
|    17 | Mockito-11         | EQ_CHECK_FOR_OPERAND_NOT_COMPATIBLE_WITH_THIS | org.mockito.internal.creation.DelegatingMethod.equals(Object) checks for operand being a reflect.Method
|    18 | Mockito-23         | SE_BAD_FIELD                                  | Class org.mockito.internal.stubbing.defaultanswers.ReturnsDeepStubs defines non-transient non-serializable instance field mockitoCore

### Bugs detected by Error Prone
| Count | Bug Id             | Bug type                            | W / E   | Message as reported by Error Prone |
|------:|--------------------|-------------------------------------|---------|------------------------------------|
|     1 | Chart-8            | ChainingConstructorIgnoresParameter | Error   | The called constructor accepts a parameter with the same name and type as one of its caller's parameters, but its caller doesn't pass that parameter to it.  It's likely that it was intended to.
|     2 | JacksonDatabind-32 | FormatString                        | Error   | extra format arguments: used 2, provided 3
|     3 | Lang-51            | FallThrough                         | Error   | Execution may fall through from the previous case; add a `// fall through` comment before this line if it was deliberate
|     4 | Lang-62            | FallThrough                         | Error   | Execution may fall through from the previous case; add a `// fall through` comment before this line if it was deliberate
|     5 | Math-57            | NarrowingCompoundAssignment         | Warning | Compound assignments from double to int hide lossy casts
|     6 | Math-66            | MissingOverride                     | Warning | optimize overrides method in AbstractUnivariateRealOptimizer; expected @Override
|       |                    | MissingOverride                     | Warning | optimize overrides method in AbstractUnivariateRealOptimizer; expected @Override
|     7 | Math-77            | MissingOverride                     | Warning | getLInfNorm overrides method in AbstractRealVector; expected @Override
|     8 | Mockito-19         | MissingOverride                     | Warning | filterCandidate implements method in MockCandidateFilter; expected @Override
|       |                    | MissingOverride                     | Warning | filterCandidate implements method in MockCandidateFilter; expected @Override

### Bugs detected by Infer
| Count | Bug Id             | Bug type         | Message as reported by Infer |
|------:|--------------------|------------------|------------------------------|
|     1 | Chart-1            | NULL_DEREFERENCE | object `dataset` last assigned on line 1796 could be null and is dereferenced at line 1800.
|     2 | Chart-4            | NULL_DEREFERENCE | object `r` last assigned on line 4473 could be null and is dereferenced at line 4493.
|     3 | Jsoup-59           | NULL_DEREFERENCE | object returned by `ownerDocument()` could be null and is dereferenced at line 363.
|     4 | JacksonDatabind-12 | RESOURCE_LEAK    | resource of type `com.fasterxml.jackson.databind.util.TokenBuffer` acquired by call to `new()` at line 573 is not released after line 603.
|     5 | Math-87            | NULL_DEREFERENCE | object returned by `getBasicRow(this,(getArtificialVariableOffset()+artificialVar))` could be null and is dereferenced at line 249.
