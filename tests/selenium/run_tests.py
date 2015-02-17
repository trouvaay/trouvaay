"""
Created on Feb 14, 2015

@author: sergey@lanasoft.net
"""

import config
import unittest

if __name__ == "__main__":
    for browser in config.BROWSERS_TO_TEST:
        if(browser == 'chrome'):
            from test_members import ChromeTests

        if(browser == 'firefox'):
            from test_members import FirefoxTests

    unittest.main()
