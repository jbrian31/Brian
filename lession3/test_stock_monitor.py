import unittest
import stock_monitor
import datetime as datetime


class TestStock_Monitor(unittest.TestCase):

    def test_weekday_too_early(self):
        weekday_too_early = datetime.datetime(2021, 1, 4, 5, 0, 0)
        result = stock_monitor.is_within_schedule(weekday_too_early)
        self.assertEqual(result, False)

    def test_weekday_too_late(self):
        weekday_too_late = datetime.datetime(2021, 1, 6, 17, 0, 0)
        result = stock_monitor.is_within_schedule(weekday_too_late)
        self.assertEqual(result, False)

    def test_weekday_within_schedule(self):
        weekday_within_schedule = datetime.datetime(2021, 1, 5, 14, 0, 0)
        result = stock_monitor.is_within_schedule(weekday_within_schedule)
        self.assertEqual(result, True)

    def test_weekend_outof_schedule(self):
        weekend_outof_schedule = datetime.datetime(2021, 1, 3, 14, 0, 0)
        result = stock_monitor.is_within_schedule(weekend_outof_schedule)
        self.assertEqual(result, False)

    def test_weekend_out_of_time(self):
        weekend_out_of_time = datetime.datetime(2021, 1, 2, 21, 0, 0)
        result = stock_monitor.is_within_schedule(weekend_out_of_time)
        self.assertEqual(result, False, msg="outside of schedule")


if __name__ == "__main__":
    unittest.main()
