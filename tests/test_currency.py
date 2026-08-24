"""
run from the root:  `python -m unittest discover`
"""

import os
import unittest
from unittest.mock import patch

os.environ.setdefault("SMTP_SERVER", "smtp.example.com")
os.environ.setdefault("SMTP_PORT", "465")
os.environ.setdefault("EMAIL_SENDER", "sender@example.com")
os.environ.setdefault("EMAIL_PASSWORD", "secret")
os.environ.setdefault("EMAIL_RECEIVER", "receiver@example.com")
os.environ.setdefault("EXCHANGE_API_KEY", "test-key")
os.environ.setdefault("EXCHANGE_URL", "https://example.com/latest.json")
os.environ.setdefault("LIST_CURRENCIES", "USD,EUR,RSD")

import currency


class FakeResponse:
    """Stands in for the object requests.get() normally returns."""

    def raise_for_status(self) -> None:
        pass

    def json(self) -> dict:
        return {"rates": {"USD": 1.0, "EUR": 0.5, "RSD": 100.0}}


class ByCurrencyTest(unittest.TestCase):

    @patch("currency.requests.get", return_value=FakeResponse())
    def test_converts_both_directions(self, fake_get):
        rates = currency.by_currency("RSD")

        # 1 EUR is 0.5 USD and 1 RSD is 100 USD, so 1 EUR = 200 RSD
        self.assertEqual(rates["EUR"]["EUR_RSD"], 200.0)
        self.assertEqual(rates["EUR"]["RSD_EUR"], 0.005)

    @patch("currency.requests.get", return_value=FakeResponse())
    def test_skips_the_base_currency(self, fake_get):
        rates = currency.by_currency("RSD")

        self.assertNotIn("RSD", rates)
        self.assertEqual(set(rates), {"USD", "EUR"})

    @patch("currency.requests.get", return_value=FakeResponse())
    def test_accepts_lowercase_symbol(self, fake_get):
        rates = currency.by_currency("rsd")

        self.assertEqual(set(rates), {"USD", "EUR"})

    @patch("currency.requests.get", return_value=FakeResponse())
    def test_rejects_unsupported_currency(self, fake_get):
        with self.assertRaises(ValueError):
            currency.by_currency("JPY")


class FetchRatesTest(unittest.TestCase):

    @patch("currency.requests.get", return_value=FakeResponse())
    def test_request_has_a_timeout(self, fake_get):
        currency.fetch_rates(["USD", "RSD"])

        self.assertEqual(fake_get.call_args.kwargs["timeout"], currency.TIMEOUT)


if __name__ == "__main__":
    unittest.main()
