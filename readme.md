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
================================================= test session starts =================================================
platform win32 -- Python 3.9.0, pytest-6.1.2, py-1.9.0, pluggy-0.13.1 -- c:\users\henry\appdata\local\programs\python\python39\python.exe
cachedir: .pytest_cache
rootdir: C:\Henry\offence-score-python
collected 15 items

test_offence_score.py::WriteFileLinesTests::test_should_write_string_list_to_file PASSED                         [  6%]
test_offence_score.py::ReadFileLinesTests::test_should_correctly_read_multi_line_file_content PASSED             [ 13%]
test_offence_score.py::ReadFileLinesTests::test_should_correctly_read_simple_file_content PASSED                 [ 20%]
test_offence_score.py::ReadFileLinesTests::test_should_correctly_read_special_characters_file_content PASSED     [ 26%]
test_offence_score.py::CalculateOffenceScoreTests::test_correctly_scores_file_with_special_characters PASSED     [ 33%]
test_offence_score.py::CalculateOffenceScoreTests::test_should_correctly_score_file_with_multiple_lines PASSED   [ 40%]
test_offence_score.py::CalculateOffenceScoreTests::test_should_correctly_score_file_with_offences PASSED         [ 46%]
test_offence_score.py::CalculateOffenceScoreTests::test_should_correctly_score_files_with_mixed_case_phrases PASSED [ 53%]
test_offence_score.py::CalculateOffenceScoreTests::test_should_correctly_score_simple_file PASSED                [ 60%]
test_offence_score.py::WriteOffenceScoresTests::test_scan_files_and_write_results_to_output_file_in_order PASSED [ 66%]
test_offence_score.py::ArgumentTests::test_parse_args_fails_when_a_target_file_does_not_exist PASSED             [ 73%]
test_offence_score.py::ArgumentTests::test_parse_args_fails_when_no_high_risk_exists PASSED                      [ 80%]
test_offence_score.py::ArgumentTests::test_parse_args_fails_when_no_low_risk_exists PASSED                       [ 86%]
test_offence_score.py::ArgumentTests::test_parse_args_fails_when_output_file_already_exists PASSED               [ 93%]
test_offence_score.py::ArgumentTests::test_parse_args_happy_path PASSED                                          [100%]

================================================= 15 passed in 0.12s ==================================================
```

#### Remarks
You need to make sure the output file does not exist; the script will not override any files.

The unit test cases are not entirely exhaustive, however they cover the cases I felt were important (input checking and validation of main logic)

The input checking itself is fairly rudimentary, and primarily exists to avoid filesystem errors. 

### Assumptions

- Special characters/whitespace/newlines breaking up a 'risky phrase' should not be matched. ie `pl an` would not be matched, given that `plan` is a 'risky word'.
- Variations of matched words that differ only by casing _should_ be matched; that is to say `PLAN` as well as `pLan` or `PlAN` would be matched, given that `plan` is a 'risky word'.
- suppose `barf` is a 'risky phrase'; `barfing` (or rather the first 4 characters of `barfing`) would be matched.
- All input files are well-formed if they exist; for example, I don't check to see if you passed in a JSON file instead of a newline delimited list of phrases.
- Characters can be part of multiple matches; for example, suppose you have a file with contents `sss`, and `ss` is considered a low risk risky word. This script will mark the score of this file as 2; the first match would be the first and second s, and the second match would be the second and third s. This case is sort of unlikely to occur, but I wanted to mention it regardless.






