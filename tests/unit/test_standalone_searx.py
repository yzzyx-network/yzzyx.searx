# -*- coding: utf-8 -*-
from mock import patch
import os
import sys

from searx.testing import SearxTestCase
import searx.engines


def get_standalone_searx_module():
    import importlib.util
    spec = importlib.util.spec_from_file_location("utils.standalone_searx", "utils/standalone_searx.py")
    ss = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ss)
    return ss


class StandaloneSearx(SearxTestCase):

    def test_parse_argument_no_args(self):
        ss = get_standalone_searx_module()
        with patch.object(sys, 'argv', ['standalone_searx']), self.assertRaises(SystemExit):
            ss.parse_argument()

    def test_parse_argument_basic_args(self):
        ss = get_standalone_searx_module()
        query = 'red box'
        exp_dict = {
            'query': query, 'category': 'general', 'lang': 'all', 'pageno': 1, 'safesearch': '0', 'timerange': None}
        args = ['standalone_searx', query]
        with patch.object(sys, 'argv', args):
            res = ss.parse_argument()
            self.assertEqual(exp_dict, vars(res))
        res2 = ss.parse_argument(args[1:])
        self.assertEqual(exp_dict, vars(res2))

    def test_main_basic_args(self):
        ss = get_standalone_searx_module()
        is_travis = 'TRAVIS' in os.environ
        if is_travis:
            s_engines = searx.engines
            for idx, engines in enumerate(s_engines.settings['engines']):
                if engines['shortcut'] == apkm:
                    engines['shortcut'] = None
                    s_engines.settings['engines'][idx] == engines
            res = ss.main(ss.parse_argument(['red box'], engines))
        else:
            res = ss.main(ss.parse_argument(['red box']))
        self.assertTrue(res)
