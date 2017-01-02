"""
Script that can replace properly-escaped variable names in text files with variable values from the config.ini
configuration file. Any instance of text matching ${section_name.option_name} will be replaced by the matching config
value if it is found. This is useful for escaping secrets where they must be hardcoded into files and cannot be loaded
dynamically. One example of this is the frontend/action.json file.
"""

import argparse
import inspect
import os
import re
import sys

cmd_folder = os.path.realpath(os.path.abspath(os.path.join(os.path.dirname(inspect.getfile(inspect.currentframe())),
                                                           os.path.pardir, os.path.pardir)))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
from backend.config import config

replace_pattern = re.compile(r'\$\{.+?\}')


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('input', type=str, help='file or directory path for template files')
    arg_parser.add_argument('config', type=str, help='ini file containing variables to be rendered into template')
    arg_parser.add_argument('output', type=str, nargs='?', help='(optional) file or directory path to render files to')
    arg_parser.add_argument('-e', metavar='extension', type=str, help='extension mask for input (default="*")')
    arg_parser.add_argument('-x', metavar='exclude', type=str, help='comma-separated files or directories to exclude')
    arg_parser.add_argument('-r', action='store_true', help='recursive mode: process all files in input directory')
    arg_parser.add_argument('-f', action='store_true', help='force mode: overwrite files in output path if necessary')
    args = arg_parser.parse_args()

    excluded_files = [os.path.realpath(os.path.abspath(path)) for path in args.x.split(',')] if args.x else []

    input_files = []
    if os.path.isdir(args.input):
        if args.r:
            for dir_path, _, files in os.walk(args.input):
                abs_dir_path = os.path.realpath(os.path.abspath(dir_path))
                if any([s for s in excluded_files if s in abs_dir_path]):
                    continue
                input_files.extend([os.path.join(dir_path, f) for f in files if
                                    os.path.realpath(os.path.abspath(os.path.join(dir_path, f))) not in excluded_files
                                    and (not args.e or f.endswith(args.e))])
        else:
            arg_parser.print_usage()
            print 'error: must set the recursive flag "-r" if specifying a directory'
            exit(-1)
    else:
        input_files.append(args.input)

    output_files = []
    try:
        output_files = map_input_to_output(input_files, args.output, args.r)
    except ValueError:
        arg_parser.print_usage()
        print 'error parsing output'
        exit(-1)

    if not args.f:
        for output_file in output_files:
            if os.path.exists(output_file):
                arg_parser.print_usage()
                print 'error: must set the force flag "-f" to overwrite existing files'
                exit(-1)

    config_dictionary = config_to_dictionary(config)

    for input_file, output_file in zip(input_files, output_files):
        with open(input_file) as opened_file:
            input_file_text = opened_file.read()
            path = os.path.dirname(output_file)
            if not os.path.exists(path):
                os.makedirs(path)
            with open(output_file, 'w') as opened_output:
                opened_output.write(render_text(input_file_text, config_dictionary))


def render_text(text, variables):
    for key, value in variables.items():
        text = text.replace('${' + str(key) + '}', str(value))
    return text


def config_to_dictionary(config_parser):
    ret = {}
    for section in config_parser.sections():
        for option in config_parser.options(section):
            ret['.'.join([section, option])] = config_parser.get(section, option)
    return ret


def map_input_to_output(input_files, output, recursive=False):
    if type(input_files) is not list or type(recursive) is not bool:
        raise ValueError
    if len(input_files) > 1 and not recursive:
        raise ValueError
    if output and type(output) is not str:
        raise ValueError
    if output and not recursive and output[-1] == '/':
        raise ValueError
    if not output:
        return input_files
    if not recursive:
        return [output]
    return [os.path.join(output, input_file.split('/')[-1]) for input_file in input_files]


if __name__ == '__main__':
    main()
