# -*- coding: utf-8 -*-
import unittest
from pykdb.core import Statistics, KDBError
from datetime import datetime
import time

sd = datetime(2016, 1, 4)
ed = datetime(2016, 1, 10)


class TestStatistics(unittest.TestCase):
    inst = Statistics()

    def test_symbol(self):
        symbols = self.inst.symbols
        expected = True
        actual = 'T1' in symbols
        self.assertEqual(expected, actual)

    def test_name(self):
        names = self.inst.names
        expected = '東証1部'
        actual = names['T1']
        self.assertEqual(expected, actual)

    def test_contracts(self):
        self.assertRaises(NotImplementedError, lambda: self.inst.contracts)

    def test_price(self):
        df = self.inst.price(sd, ed, 'T1', '1d')
        expected = float(1986571900)
        actual = float(df.query("日付 == '2016-01-04'")['出来高'])
        self.assertEqual(expected, actual)

    def test_price_invalid_symbol(self):
        expected = KDBError
        actual = self.inst.price(sd, ed, 'XX', '1d')
        self.assertEqual(expected, actual)

    def test_price_invalid_freq(self):
        expected = KDBError
        actual = self.inst.price(sd, ed, 'T1', '4h')
        self.assertEqual(expected, actual)

    def test_price_all(self):
        time.sleep(5)
        df = self.inst.price_all(sd, ed)
        expected = float(1986571900)
        actual = float(df.query("日付 == '2016-01-04' and 市場 == '東証1部'")['出来高'])
        self.assertEqual(expected, actual)

    def test_price_all_invalid_session(self):
        expected = KDBError
        actual = self.inst.price_all(sd, ed, 'e')
        self.assertEqual(expected, actual)


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestStatistics))
    return suite


if __name__ == '__main__':
    unittest.main()
