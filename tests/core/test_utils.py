import datetime
from unittest import TestCase

from apps.core.utils import chain, convert_to_snake_case, get_future_date


class UtilsTestCase(TestCase):

    def test_get_future_date(self):
        now = datetime.datetime.now()
        future_date_str = get_future_date(60)
        extra_days = datetime.datetime.strptime(future_date_str, "%a, %d-%b-%Y %H:%M:%S GMT") - now
        # +- 1 day is acceptable here
        assert extra_days.days in range(59, 60)

    def test_convert_to_snake_case(self):
        test_string = "Some Test String"
        assert "some_test_string" == convert_to_snake_case(test_string)

    def test_chain(self):
        l1 = (1, 2, 3)
        l2 = [4, 5, 6]

        assert [*l1, *l2] == list(chain(l1, l2))
