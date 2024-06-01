import unittest

from src.DoremiSubscription import DoremiSubscription


class DoRemiSubscriptionTest(unittest.TestCase):
    def test_valid_date_for_subscription(self):
        _obj = DoremiSubscription()
        result = _obj.run_command("START_SUBSCRIPTION", "22-89-23")
        self.assertEqual(result, "ADD_SUBSCRIPTION_FAILED INVALID_DATE", "Date should be invalid")

    def test_is_command_valid(self):
        _obj = DoremiSubscription()
        result = _obj.run_command("STOP_SUBSCRIPTION", "23-12-23")

        self.assertEqual(result, "INVALID_COMMAND", "Command should be invalid")

    def test_print_renewal_details_on_empty_subscription(self):
        _obj = DoremiSubscription()
        result = _obj.run_command("PRINT_RENEWAL_DETAILS")

        self.assertEqual(result, "SUBSCRIPTIONS_NOT_FOUND", "No subscription should be present")

    def test_subscription_duplicate_category(self):
        _obj = DoremiSubscription()
        _obj.run_command("START_SUBSCRIPTION", "23-12-2023")
        _obj.run_command("ADD_SUBSCRIPTION", "MUSIC", "PREMIUM")
        result = _obj.run_command("ADD_SUBSCRIPTION", "MUSIC", "PREMIUM")

        self.assertEqual(result, "ADD_SUBSCRIPTION_FAILED DUPLICATE_CATEGORY", "Duplicate category should not be added")

    def test_topup_duplicate_category(self):
        _obj = DoremiSubscription()
        _obj.run_command("START_SUBSCRIPTION", "23-12-2023")
        _obj.run_command("ADD_SUBSCRIPTION", "MUSIC", "PREMIUM")
        _obj.run_command("ADD_TOPUP", "FOUR_DEVICE", "1")
        result = _obj.run_command("ADD_TOPUP", "FOUR_DEVICE", "1")

        self.assertEqual(result, "ADD_TOPUP_FAILED DUPLICATE_TOPUP", "Duplicate topup should not be added")

    def test_topup_fails_on_empty_subscription(self):
        _obj = DoremiSubscription()
        _obj.run_command("START_SUBSCRIPTION", "22-12-2121")
        result = _obj.run_command("ADD_TOPUP", "FOUR_DEVICE", "1")

        self.assertEqual(result, "SUBSCRIPTIONS_NOT_FOUND", "No subscription should be present")

    def test_print_renewals_details(self):
        _obj = DoremiSubscription()
        _obj.run_command("START_SUBSCRIPTION", "20-02-2022")
        _obj.run_command("ADD_SUBSCRIPTION", "MUSIC", "PERSONAL")
        _obj.run_command("ADD_SUBSCRIPTION", "VIDEO", "PREMIUM")
        _obj.run_command("ADD_SUBSCRIPTION", "PODCAST", "FREE")
        _obj.run_command("ADD_TOPUP", "FOUR_DEVICE", "3")
        result = _obj.run_command("PRINT_RENEWAL_DETAILS")

        self.assertEqual(str(result),
                         "['RENEWAL_REMINDER MUSIC 10-03-2022', 'RENEWAL_REMINDER VIDEO 10-05-2022', 'RENEWAL_REMINDER PODCAST 10-03-2022', 'RENEWAL_AMOUNT 750']",
                         "Subscription details should be printed")


if __name__ == '__main__':
    unittest.main()
