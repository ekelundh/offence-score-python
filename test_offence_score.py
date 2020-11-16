from unittest import mock
from unittest.mock import patch, mock_open, call

import unittest

import offence_score

# execute with command 'py.test <path-to-this-file> -v'

high_risk_phrases_file_path = 'path/to/high_risk.txt'
low_risk_phrases_file_path = 'path/to/low_risk.txt'

high_risk_phrases_file_lines = [
    'Voldemort',
    'Dark Lord',
    'mundane',
    'Pinocchio',
    'ki**en',
]

low_risk_phrases_file_lines = [
    'eSolutions',
    'gangster',
    'ugliest',
    'destiny',
    'shooter',
    'plan'
]

output_file_path = 'path/to/output.txt'

special_characters_file_path = 'data/specialCharacters.txt'
mixed_case_file_path = 'data/mixedCase.txt'
multi_line_file_path = 'data/multiLine.txt'
simple_file_path = 'data/simple.txt'
no_offence_file_path = 'data/noOffence.txt'

files_to_scan = [
    mixed_case_file_path,
    multi_line_file_path,
    simple_file_path,
    special_characters_file_path,
    no_offence_file_path
]
mixed_case_file_content = "The insidious sky joins the Dark Lord and his mundane shOOteR!"
mixed_case_file_lines = ["The insidious sky joins the Dark Lord and his mundane shOOteR!"]

multi_line_file_content = """The legend of the raven's roar gambles with lives, happiness, and even destiny itself!


''''"""
multi_line_file_lines = ["The legend of the raven's roar gambles with lives, happiness, and even destiny itself!",
                         '',
                         '',
                         "''''"]

simple_file_content = "The ugliest sister engineers the animal's plan."
simple_file_lines = ["The ugliest sister engineers the animal's plan."]

special_characters_file_content = "The law modernizes the mundane impulse of eSolutions; that's amazing/."
special_characters_file_lines = ["The law modernizes the mundane impulse of eSolutions; that's amazing/."]

no_offence_file_content = "Whiskey on the table likes to take a walk in the park."
no_offence_file_lines = ["Whiskey on the table likes to take a walk in the park."]

expected_file_output = [
    '{}:{}'.format(mixed_case_file_path, '5'),
    '{}:{}'.format(multi_line_file_path, '1'),
    '{}:{}'.format(simple_file_path, '2'),
    '{}:{}'.format(special_characters_file_path, '3'),
    '{}:{}'.format(no_offence_file_path, '0')
]

expected_file_output_raw = '\n'.join(expected_file_output)


def read_file_lines_side_effects(file_path):
    if file_path == mixed_case_file_path:
        return mixed_case_file_lines
    elif file_path == multi_line_file_path:
        return multi_line_file_lines
    elif file_path == simple_file_path:
        return simple_file_lines
    elif file_path == special_characters_file_path:
        return special_characters_file_lines
    elif file_path == no_offence_file_path:
        return no_offence_file_lines
    elif file_path == high_risk_phrases_file_path:
        return high_risk_phrases_file_lines
    elif file_path == low_risk_phrases_file_path:
        return low_risk_phrases_file_lines
    else:
        raise ValueError("File path'{}' is not set up to be mocked yet.".format(file_path))


def get_offence_score_for_file_side_effects(high_risk, low_risk, file_path):
    if high_risk != high_risk_phrases_file_lines or low_risk != low_risk_phrases_file_lines:
        raise ValueError('The high or low risk phrases passed in have not been mocked yet')

    if file_path == mixed_case_file_path:
        return 5
    elif file_path == multi_line_file_path:
        return 1
    elif file_path == simple_file_path:
        return 2
    elif file_path == special_characters_file_path:
        return 3
    elif file_path == no_offence_file_path:
        return 0
    else:
        raise ValueError("File path'{}' is not set up to be mocked yet.".format(file_path))


class WriteFileLinesTests(unittest.TestCase):
    @staticmethod
    def test_should_write_string_list_to_file():
        with patch("builtins.open", mock_open()) as mock_file:
            offence_score.write_file_lines(expected_file_output, output_file_path)
            mock_file.assert_called_once_with(output_file_path, 'w')

            mock_handle = mock_file()
            mock_handle.write.assert_called_once_with(expected_file_output_raw)


class ReadFileLinesTests(unittest.TestCase):
    def test_should_correctly_read_simple_file_content(self):
        with patch("builtins.open", mock_open(read_data=simple_file_content)) as mock_file:
            lines = offence_score.read_file_lines(simple_file_path)
            mock_file.assert_called_once_with(simple_file_path)
            self.assertEqual(simple_file_lines, lines)

    def test_should_correctly_read_special_characters_file_content(self):
        with patch("builtins.open", mock_open(read_data=special_characters_file_content)) as mock_file:
            lines = offence_score.read_file_lines(special_characters_file_path)
            mock_file.assert_called_once_with(special_characters_file_path)
            self.assertEqual(special_characters_file_lines, lines)

    def test_should_correctly_read_multi_line_file_content(self):
        with patch("builtins.open", mock_open(read_data=multi_line_file_content)) as mock_file:
            lines = offence_score.read_file_lines(multi_line_file_path)
            mock_file.assert_called_once_with(multi_line_file_path)
            self.assertEqual(multi_line_file_lines, lines)


# tests 'get_offence_score_for_file' explicitly and 'get_substr_count_in_str' implicitly.
class CalculateOffenceScoreTests(unittest.TestCase):
    @mock.patch('offence_score.read_file_lines')
    def test_should_correctly_score_files_with_mixed_case_phrases(self, mock_read_file_lines):
        mock_read_file_lines.side_effect = read_file_lines_side_effects
        score = offence_score.get_offence_score_for_file(high_risk_phrases_file_lines, low_risk_phrases_file_lines,
                                                         mixed_case_file_path)
        mock_read_file_lines.assert_called_once_with(mixed_case_file_path)
        self.assertEqual(5, score)

    @mock.patch('offence_score.read_file_lines')
    def test_should_correctly_score_file_with_multiple_lines(self, mock_read_file_lines):
        mock_read_file_lines.side_effect = read_file_lines_side_effects
        score = offence_score.get_offence_score_for_file(high_risk_phrases_file_lines, low_risk_phrases_file_lines,
                                                         multi_line_file_path)
        mock_read_file_lines.assert_called_once_with(multi_line_file_path)
        self.assertEqual(1, score)

    @mock.patch('offence_score.read_file_lines')
    def test_should_correctly_score_simple_file(self, mock_read_file_lines):
        mock_read_file_lines.side_effect = read_file_lines_side_effects
        score = offence_score.get_offence_score_for_file(high_risk_phrases_file_lines, low_risk_phrases_file_lines,
                                                         simple_file_path)
        mock_read_file_lines.assert_called_once_with(simple_file_path)
        self.assertEqual(2, score)

    @mock.patch('offence_score.read_file_lines')
    def test_correctly_scores_file_with_special_characters(self, mock_read_file_lines):
        mock_read_file_lines.side_effect = read_file_lines_side_effects

        score = offence_score.get_offence_score_for_file(
            high_risk_phrases_file_lines,
            low_risk_phrases_file_lines,
            special_characters_file_path)

        mock_read_file_lines.assert_called_once_with(special_characters_file_path)
        self.assertEqual(3, score)

    @mock.patch('offence_score.read_file_lines')
    def test_should_correctly_score_file_with_offences(self, mock_read_file_lines):
        mock_read_file_lines.side_effect = read_file_lines_side_effects
        score = offence_score.get_offence_score_for_file(high_risk_phrases_file_lines, low_risk_phrases_file_lines,
                                                         no_offence_file_path)
        mock_read_file_lines.assert_called_once_with(no_offence_file_path)
        self.assertEqual(0, score)


# tests main fuction
class WriteOffenceScoresTests(unittest.TestCase):
    @mock.patch('offence_score.write_file_lines')
    @mock.patch('offence_score.read_file_lines')
    @mock.patch('offence_score.get_offence_score_for_file')
    def test_scan_files_and_write_results_to_output_file_in_order(
            self,
            mock_get_offence_score_for_file,
            mock_read_file_lines,
            mock_write_file_lines):
        mock_get_offence_score_for_file.side_effect = get_offence_score_for_file_side_effects
        mock_read_file_lines.side_effect = read_file_lines_side_effects
        result = offence_score.write_offence_scores_to_file(
            high_risk_phrases_file_path,
            low_risk_phrases_file_path,
            output_file_path,
            files_to_scan)

        mock_read_file_lines.assert_has_calls([
            call(high_risk_phrases_file_path), call(low_risk_phrases_file_path)],
            any_order=False)

        self.assertEqual(2, mock_read_file_lines.call_count)

        mock_get_offence_score_for_file.assert_has_calls([
            call(high_risk_phrases_file_lines,
                 low_risk_phrases_file_lines,
                 mixed_case_file_path),
            call(high_risk_phrases_file_lines,
                 low_risk_phrases_file_lines,
                 multi_line_file_path),
            call(high_risk_phrases_file_lines,
                 low_risk_phrases_file_lines,
                 simple_file_path),
            call(high_risk_phrases_file_lines,
                 low_risk_phrases_file_lines,
                 special_characters_file_path),
            call(high_risk_phrases_file_lines,
                 low_risk_phrases_file_lines,
                 no_offence_file_path)],
            any_order=False)

        self.assertEqual(5, mock_get_offence_score_for_file.call_count)

        mock_write_file_lines.assert_called_once_with(expected_file_output, output_file_path)
        self.assertEqual(1, mock_write_file_lines.call_count)
        self.assertEqual(0, result)


# tests argument parsing
class ArgumentTests(unittest.TestCase):
    @mock.patch('os.path.isfile')
    def test_parse_args_happy_path(self, mock_isfile):
        input_args = ['offence_score.py', high_risk_phrases_file_path, low_risk_phrases_file_path, output_file_path]
        for file in files_to_scan:
            input_args.append(file)

        def side_effect(filename):
            if filename != output_file_path:
                return True
            return False

        mock_isfile.side_effect = side_effect

        args = offence_score.parse_args(input_args)
        self.assertEqual(args.high_risk_phrases_file_path, high_risk_phrases_file_path)
        self.assertEqual(args.low_risk_phrases_file_path, low_risk_phrases_file_path)
        self.assertEqual(args.output_file_path, output_file_path)
        self.assertEqual(args.files_to_score, files_to_scan)

    @mock.patch('os.path.isfile')
    def test_parse_args_fails_when_no_high_risk_exists(self, mock_isfile):
        input_args = ['offence_score.py', high_risk_phrases_file_path, low_risk_phrases_file_path, output_file_path]
        for file in files_to_scan:
            input_args.append(file)

        def side_effect(filename):
            if filename != output_file_path and filename != high_risk_phrases_file_path:
                return True
            return False

        mock_isfile.side_effect = side_effect
        with self.assertRaises(SystemExit):
            offence_score.parse_args(input_args)

    @mock.patch('os.path.isfile')
    def test_parse_args_fails_when_no_low_risk_exists(self, mock_isfile):
        input_args = ['offence_score.py', high_risk_phrases_file_path, low_risk_phrases_file_path, output_file_path]
        for file in files_to_scan:
            input_args.append(file)

        def side_effect(filename):
            if filename != output_file_path and filename != low_risk_phrases_file_path:
                return True
            return False

        mock_isfile.side_effect = side_effect
        with self.assertRaises(SystemExit):
            offence_score.parse_args(input_args)

    @mock.patch('os.path.isfile')
    def test_parse_args_fails_when_output_file_already_exists(self, mock_isfile):
        input_args = ['offence_score.py', high_risk_phrases_file_path, low_risk_phrases_file_path, output_file_path]
        for file in files_to_scan:
            input_args.append(file)

        def side_effect(filename):
            return True

        mock_isfile.side_effect = side_effect
        with self.assertRaises(SystemExit):
            offence_score.parse_args(input_args)
