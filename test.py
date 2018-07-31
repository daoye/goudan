#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest

if __name__ == '__main__':
    suite = unittest.TestSuite()

    # tests = [SamplePoolTest("test_get_one")]
    # suite.addTests(tests)
    suite.addTests(unittest.TestLoader().loadTestsFromName(
        'tests.samplePoolTest.SamplePoolTest'))
    suite.addTests(unittest.TestLoader().loadTestsFromName(
        'tests.checkerTest.CheckerTest'))
    suite.addTests(unittest.TestLoader().loadTestsFromName(
        'tests.piplineTest.PiplineTest'))

    # runner = unittest.TextTestRunner(verbosity=1)
    runner = unittest.TextTestRunner()
    runner.run(suite)
    unittest.main()
