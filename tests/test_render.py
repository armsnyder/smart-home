from unittest import TestCase
from ConfigParser import ConfigParser

from infrastructure.install_scripts import render


class RenderText(TestCase):
    text_no_variables = "kjh45iu43f5;43pjt['vt43u532\nsadfjkg23ouir43tp[43tk\wef\nasdfkjh3q4t4[3\teraothjkq34;"
    text_with_variables = "kjh45${ex_group.ex_item}pjt['vt43u532\nsadfjkg23ouir${jkl234.23}[43tk\wef\nasdfkjh3q4"

    def test_no_variables_anywhere(self):
        self.assertEqual(self.text_no_variables, render.render_text(self.text_no_variables, {}))

    def test_no_variables_in_text(self):
        self.assertEqual(self.text_no_variables, render.render_text(self.text_no_variables, {'a': 2, 1: 5}))

    def test_with_variables(self):
        self.assertEqual("kjh4512pjt['vt43u532\nsadfjkg23ouir   [43tk\wef\nasdfkjh3q4", render.render_text(
            self.text_with_variables, {'ex_group.ex_item': 12, 'jkl234.23': '   ', 12: 'fa', 'jkg': 'qw'}))


class ConfigToDictionary(TestCase):
    def test(self):
        config = ConfigParser()
        config.add_section('a')
        config.add_section('b')
        config.set('a', '1', '2')
        config.set('a', 'foo', 'bar')
        config.set('b', 'a.c', '')
        self.assertEqual({'a.1': '2', 'a.foo': 'bar', 'b.a.c': ''}, render.config_to_dictionary(config))


class MapInputToOutput(TestCase):
    def test_single_file(self):
        self.assertEqual(['/c/d.biz'], render.map_input_to_output(['/a/b.txt'], '/c/d.biz'))

    def test_single_file_no_output_extension(self):
        self.assertEqual(['/c/d'], render.map_input_to_output(['/a/b.txt'], '/c/d'))

    def test_single_file_no_input_extension(self):
        self.assertEqual(['/c/d.biz'], render.map_input_to_output(['/a/b'], '/c/d.biz'))

    def test_single_file_output_is_dir(self):
        self.assertRaises(ValueError, render.map_input_to_output, ['/a/b.txt'], '/c/')

    def test_single_file_recursive(self):
        self.assertEqual(['/c/d/b.txt'], render.map_input_to_output(['/a/b.txt'], '/c/d', True))

    def test_single_file_recursive_trailing_slash(self):
        self.assertEqual(['/c/d/b.txt'], render.map_input_to_output(['/a/b.txt'], '/c/d/', True))

    def test_single_file_recursive_output_extension(self):
        self.assertEqual(['/c/d.biz/b.txt'], render.map_input_to_output(['/a/b.txt'], '/c/d.biz', True))

    def test_multi_file_recursive_output_extension(self):
        self.assertEqual(['/c/d.biz/b.txt', '/c/d.biz/j.doc'], 
                         render.map_input_to_output(['/a/b.txt', '/g/f/j.doc'], '/c/d.biz', True))

    def test_multi_file_not_recursive(self):
        self.assertRaises(ValueError, render.map_input_to_output, ['/a/b.txt', '/g/f/j.doc'], '/c/d.biz')
        
    def test_single_file_no_output(self):
        self.assertEqual(['/a/b.txt'], render.map_input_to_output(['/a/b.txt'], None))

    def test_single_file_no_input_extension_no_output(self):
        self.assertEqual(['/a/b'], render.map_input_to_output(['/a/b'], None))

    def test_single_file_recursive_no_output(self):
        self.assertEqual(['/a/b.txt'], render.map_input_to_output(['/a/b.txt'], None, True))

    def test_multi_file_recursive_output_extension_no_output(self):
        self.assertEqual(['/a/b.txt', '/g/f/j.doc'], render.map_input_to_output(['/a/b.txt', '/g/f/j.doc'], None, True))

    def test_multi_file_not_recursive_no_output(self):
        self.assertRaises(ValueError, render.map_input_to_output, ['/a/b.txt', '/g/f/j.doc'], None)
