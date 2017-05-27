import unittest
import sys
from violations import get_violations

class TestViolations(unittest.TestCase):
    def test_get_violations(self):
        smonth, sday, syear = 1,1,2017
        emonth, eday, eyear = 1,3,2017
        response = get_violations(smonth, sday, syear, emonth, eday, eyear)
        self.assertEqual(len(response), 18)

if __name__ == '__main__':
    unittest.main()