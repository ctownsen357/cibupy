import unittest
from datetime import date
from violations import get_violations

class TestViolations(unittest.TestCase):
    def test_get_violations(self):
        date_start = date(year=2017,month=1,day=1)
        date_end = date(year=2017, month=1, day=3)
        response = get_violations(date_start, date_end)
        self.assertEqual(len(response), 18)

if __name__ == '__main__':
    unittest.main()