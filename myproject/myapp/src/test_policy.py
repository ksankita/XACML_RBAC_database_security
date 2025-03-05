import unittest
from policy_evaluator import PolicyEvaluator

class TestPolicyEvaluator(unittest.TestCase):
    def setUp(self):
        self.evaluator = PolicyEvaluator("../policies/policy.xml")

    def test_manager_access_anytime_anywhere(self):
        self.assertEqual(self.evaluator.evaluate_request("manager", "office", 2), "Permit")
        self.assertEqual(self.evaluator.evaluate_request("manager", "home", 23), "Permit")
        self.assertEqual(self.evaluator.evaluate_request("manager", "cafe", 5), "Permit")

    def test_employee_access_office_hours(self):
        self.assertEqual(self.evaluator.evaluate_request("employee", "office", 10), "Permit")
        self.assertEqual(self.evaluator.evaluate_request("employee", "office", 17), "Permit")

    def test_employee_access_outside_office_hours(self):
        self.assertEqual(self.evaluator.evaluate_request("employee", "office", 8), "Deny")
        self.assertEqual(self.evaluator.evaluate_request("employee", "office", 18), "Deny")

    def test_employee_access_outside_office(self):
        self.assertEqual(self.evaluator.evaluate_request("employee", "home", 14), "Deny")
        self.assertEqual(self.evaluator.evaluate_request("employee", "cafe", 10), "Deny")

if __name__ == '__main__':
    unittest.main()
