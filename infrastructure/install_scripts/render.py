import argparse
import os

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('input_file', type=str)
arg_parser.add_argument('output_file', type=str, nargs='?')
arg_parser.add_argument('-e', type=str)
args = arg_parser.parse_args()

input_files = []
if os.path.isdir(args.input_file):
    for dir_path, _, files in os.walk(args.input_file):
        input_files.extend([os.path.join(dir_path, f) for f in files if not args.e or f.endswith(args.e)])
else:
    input_files.append(args.input_file)

for input_file in input_files:
    with open(input_file) as opened_file:
        if args.output_file:
            pass