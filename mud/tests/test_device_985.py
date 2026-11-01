"""The Romppainen–Fujita device: helmets, the four-a-day rule and save-safe state (#985).

The rules these tests pin are the ones a player feels: you cannot run the test with one helmet, you cannot run
it five times in a day, and the counter survives a save. None of them may make a case unsolvable.
"""
import unittest

from nopunk_mud.consciousness import (
    DAILY_TEST_LIMIT,
    DEVICE_NAME,
    FIELD_OFFICE,
    DeviceError,
    DeviceState,
    begin_test,
    check_fit,
    remaining,
)


class DeviceIdentityTests(unittest.TestCase):
    def test_the_device_carries_the_approved_name(self) -> None:
        # Romppainen-Fujita with an en dash; the Japanese character belongs to her, not to this constant.
        self.assertEqual(DEVICE_NAME, "Romppainen\u2013Fujita")

    def test_it_is_helsinki_only_equipment(self) -> None:
        self.assertEqual(FIELD_OFFICE, "helsinki")

    def test_the_cap_is_four(self) -> None:
        self.assertEqual(DAILY_TEST_LIMIT, 4)


class HelmetTests(unittest.TestCase):
    def test_both_helmets_satisfy_the_fit(self) -> None:
        check_fit(administrator_helmet=True, subject_helmet=True)

    def test_a_missing_administrator_helmet_is_refused(self) -> None:
        with self.assertRaises(DeviceError):
            check_fit(administrator_helmet=False, subject_helmet=True)

    def test_a_missing_subject_helmet_is_refused(self) -> None:
        with self.assertRaises(DeviceError):
            check_fit(administrator_helmet=True, subject_helmet=False)

    def test_a_refused_fit_records_nothing(self) -> None:
        state = DeviceState(day=3, used=0)
        with self.assertRaises(DeviceError):
            begin_test(state, day=3, administrator_helmet=False, subject_helmet=True)
        self.assertEqual(state.used, 0)


class DailyCapTests(unittest.TestCase):
    def test_four_tests_in_a_day_are_allowed(self) -> None:
        state = DeviceState(day=1, used=0)
        for expected in range(1, DAILY_TEST_LIMIT + 1):
            state = begin_test(state, day=1, administrator_helmet=True, subject_helmet=True)
            self.assertEqual(state.used, expected)

    def test_a_fifth_test_is_refused(self) -> None:
        state = DeviceState(day=1, used=DAILY_TEST_LIMIT)
        with self.assertRaises(DeviceError) as refused:
            begin_test(state, day=1, administrator_helmet=True, subject_helmet=True)
        self.assertIn("goofy", str(refused.exception))

    def test_remaining_counts_down(self) -> None:
        state = DeviceState(day=2, used=1)
        self.assertEqual(remaining(state, day=2), DAILY_TEST_LIMIT - 1)

    def test_the_counter_rolls_over_on_a_new_day(self) -> None:
        spent = DeviceState(day=2, used=DAILY_TEST_LIMIT)
        self.assertEqual(remaining(spent, day=3), DAILY_TEST_LIMIT)
        fresh = begin_test(spent, day=3, administrator_helmet=True, subject_helmet=True)
        self.assertEqual((fresh.day, fresh.used), (3, 1))

    def test_a_refused_cap_does_not_reset_the_counter(self) -> None:
        spent = DeviceState(day=2, used=DAILY_TEST_LIMIT)
        with self.assertRaises(DeviceError):
            begin_test(spent, day=2, administrator_helmet=True, subject_helmet=True)
        self.assertEqual((spent.day, spent.used), (2, DAILY_TEST_LIMIT))


class SaveTests(unittest.TestCase):
    def test_the_counter_survives_a_save_round_trip(self) -> None:
        state = DeviceState(day=7, used=3)
        restored = DeviceState.from_dict(state.to_dict())
        self.assertEqual(restored, state)
        self.assertEqual(remaining(restored, day=7), 1)

    def test_an_empty_save_starts_a_fresh_agent(self) -> None:
        restored = DeviceState.from_dict({})
        self.assertEqual(remaining(restored, day=0), DAILY_TEST_LIMIT)


if __name__ == "__main__":
    unittest.main()
