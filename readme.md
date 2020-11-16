### System Requirements

You will need to have python 3 (only tested on 3.9.0) and py.test (only tested version 6.1.2) if you wish to run the unit tests

### Usage

```bash
python <path-to-offence_score.py> <path-to-high-risk-phrase-file> <path-to-low-risk-phrase-file> <path-to-output-file> <file1> [<file2>....<fileN>]
```

#### Testing
There are unit tests contained in the `test_offence_score.py` file to validate the script's correctness. I have based the test cases off of the 15 input files provided.

You will need py.test to run these tests yourself, and they are written using the standard python unit test framework `unittest`.
I used pytest-6.1.2 in development/testing of the script.

The tests can then be run with the following command:

```bash
py.test <path-to-test_offence_score.py> -v
```
After executing that command, you should see something similar to the following:


```
======================================================================================================== test session starts ========================================================================================================
platform win32 -- Python 3.9.0, pytest-6.1.2, py-1.9.0, pluggy-0.13.1 -- c:\users\henry\appdata\local\programs\python\python39\python.exe
cachedir: .pytest_cache
rootdir: C:\Henry\python
collected 14 items

test_offence_score.py::WriteFileLinesTests::test_should_write_string_list_to_file PASSED                                                                                                                                       [  7%]
test_offence_score.py::ReadFileLinesTests::test_should_correctly_read_multi_line_file_content PASSED                                                                                                                           [ 14%]
test_offence_score.py::ReadFileLinesTests::test_should_correctly_read_simple_file_content PASSED                                                                                                                               [ 21%]
test_offence_score.py::ReadFileLinesTests::test_should_correctly_read_special_characters_file_content PASSED                                                                                                                   [ 28%]
test_offence_score.py::CalculateOffenceScoreTests::test_correctly_scores_file_with_special_characters PASSED                                                                                                                   [ 35%]
test_offence_score.py::CalculateOffenceScoreTests::test_should_correctly_score_file_with_multiple_lines PASSED                                                                                                                 [ 42%]
test_offence_score.py::CalculateOffenceScoreTests::test_should_correctly_score_file_with_offences PASSED                                                                                                                       [ 50%]
test_offence_score.py::CalculateOffenceScoreTests::test_should_correctly_score_files_with_mixed_case_phrases PASSED                                                                                                            [ 57%]
test_offence_score.py::CalculateOffenceScoreTests::test_should_correctly_score_simple_file PASSED                                                                                                                              [ 64%]
test_offence_score.py::WriteOffenceScoresTests::test_scan_files_and_write_results_to_output_file_in_order PASSED                                                                                                               [ 71%]
test_offence_score.py::ArgumentTests::test_parse_args_fails_when_no_high_risk_exists PASSED                                                                                                                                    [ 78%]
test_offence_score.py::ArgumentTests::test_parse_args_fails_when_no_low_risk_exists PASSED                                                                                                                                     [ 85%]
test_offence_score.py::ArgumentTests::test_parse_args_fails_when_output_file_already_exists PASSED                                                                                                                             [ 92%]
test_offence_score.py::ArgumentTests::test_parse_args_happy_path PASSED                                                                                                                                                        [100%]

======================================================================================================== 14 passed in 0.14s =========================================================================================================
```

#### Remarks
You need to make sure the output file does not exist; the script will not override any files.

The unit test cases are not entirely exhaustive, however they cover the cases I felt were important (input checking and validation of main logic)

The input checking itself is fairly rudementary, and primarily exists to avoid filesystem errors. 

### Assumptions

- Special characters/whitespace/newlines breaking up a 'risky phrase' should not be matched. ie `pl an` would not be matched, given that `plan` is a 'risky word'.
- Variations of matched words that differ only by casing _should_ be matched; that is to say `PLAN` as well as `pLan` or `PlAN` would be matched, given that `plan` is a 'risky word'.
- All input files are well-formed if they exist; for example, I don't check to see if you passed in a JSON file instead of a newline delimited list of phrases.
- Characters can be part of multiple matches; for example, suppose you have a file with contents `sss`, and `ss` is considered a low risk risky word. This script will mark the score of this file as 2; the first match would be the first and second s, and the second match would be the second and third s. This case is sort of unlikely to occur, but I wanted to mention it regardless.






