import argparse
import os
import sys


# extracted functionality to make testing easier
def read_file_lines(file_path: str) -> list[str]:
    with open(file_path) as file:
        content = file.read().splitlines()
    return content


def write_file_lines(content: list[str], file_path: str) -> None:
    with open(file_path, 'w') as output_file:
        output_file.write('\n'.join(content))
    return


# Fetches arguments and performs simple validation on them before script logic runs.
def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("high_risk_phrases_file_path", help="Path to the high risk phrases file.",
                        type=str)
    parser.add_argument("low_risk_phrases_file_path", help="Path to the low risk phrases file.",
                        type=str)
    parser.add_argument("output_file_path", help="Path to the output file",
                        type=str)
    parser.add_argument("files_to_score", help="list of paths of text files to score", nargs='+',
                        type=str)

    args = parser.parse_args(argv[1:])

    if not os.path.isfile(args.high_risk_phrases_file_path):
        parser.print_help()
        print('High risk phrase file \'{}\' is not found.'.format(args.high_risk_phrases_file_path))
        exit(1)

    if not os.path.isfile(args.low_risk_phrases_file_path):
        parser.print_help()
        print('Low risk phrase file \'{}\' is not found.'.format(args.low_risk_phrases_file_path))
        exit(1)

    if os.path.isfile(args.output_file_path):
        parser.print_help()
        print('Output file \'{}\' already exists.'.format(args.output_file_path))
        exit(1)

    for file in args.files_to_score:
        if not os.path.isfile(file):
            print('File to scan \'{}\' is not found.'.format(file))
            exit(1)

    return args

# returns number of substring instances found within the target string
def get_substr_count_in_str(substrings: list[str], target_string: str) -> int:
    count = 0
    target_string_normalized = target_string.casefold()
    for substr in substrings:
        substr_normalized = substr.casefold()
        target_string_index = 0
        # python does not have a do while loop, so this is a workaround for that
        while True:
            occurrence_index = target_string_normalized.find(substr_normalized, target_string_index)
            if occurrence_index == -1:
                break
            count += 1
            target_string_index = occurrence_index + 1

    return count


# returns the offence score for a specified file given lists of high risk and low risk phrases
# high risk phrases have double the 'offence score' of a low risk phrase.
def get_offence_score_for_file(
        high_risk_phrases: list[str],
        low_risk_phrases: list[str],
        file_path: str) -> int:
    file_lines = read_file_lines(file_path)
    offence_score = 0
    for line in file_lines:
        offence_score = (offence_score +
                         get_substr_count_in_str(low_risk_phrases, line) +
                         get_substr_count_in_str(high_risk_phrases, line) * 2)
    return offence_score


# writes the offence score of the specified files to the specified output file.
# offence score is calculated from lists of high risk and low risk phrases.
def write_offence_scores_to_file(
        high_risk_phrases_file_path: str,
        low_risk_phrases_file_path: str,
        output_file_path: str,
        files_to_scan: list[str]):
    high_risk_phrases = read_file_lines(high_risk_phrases_file_path)
    low_risk_phrases = read_file_lines(low_risk_phrases_file_path)

    offence_scores_by_file = {}
    for file_path in files_to_scan:
        offence_scores_by_file[file_path] = get_offence_score_for_file(high_risk_phrases, low_risk_phrases, file_path)
    output = []
    for file_path in files_to_scan:
        file_result = '{}:{}'.format(file_path, offence_scores_by_file[file_path])
        output.append(file_result)
    write_file_lines(output, output_file_path)
    return 0

# parses inputs and calls the main logic
def main(argv: list[str]) -> int:
    args = parse_args(argv)
    return write_offence_scores_to_file(
        args.high_risk_phrases_file_path,
        args.low_risk_phrases_file_path,
        args.output_file_path,
        args.files_to_score
    )


if __name__ == '__main__':
    sys.exit(main(sys.argv))
