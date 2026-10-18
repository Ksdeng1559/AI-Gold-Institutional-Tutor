import io
import json
import sys
import unittest
import urllib.error
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from marketaux_demo import FeedError, NoRedirect, fetch, normalize

TOKEN = "test-secret-not-a-real-key"


def article(uid="one", **updates):
    return {"uuid": uid, "title": "Fixture headline", "url": "https://example.org/story",
            "source": "example.org", "published_at": "2026-10-18T12:00:00Z", **updates}


class FeedTests(unittest.TestCase):
    def test_dedup_and_safety(self):
        payload = {"data": [article(), article(), article("two", url="javascript:alert(1)"),
                            article("three", title=TOKEN), article("four", published_at="invalid")]}
        result = normalize(payload, "gold", TOKEN)
        self.assertEqual(result["included"], 1)
        self.assertNotIn(TOKEN, json.dumps(result))

    def test_failure_is_not_empty_success(self):
        for payload in ({"error": "bad"}, {"data": {}, "meta": {}}, {"data": [], "error": "bad"}):
            with self.assertRaises(FeedError):
                normalize(payload, "gold", TOKEN)

    def test_empty_feed_and_missing_meta(self):
        result = normalize({"data": [], "meta": None}, "crypto", TOKEN)
        self.assertEqual(result["included"], 0)
        self.assertEqual(result["topic"], "crypto")

    def test_request_and_error_redaction(self):
        class Fake:
            def open(self, request, timeout):
                self.request = request
                return io.StringIO(json.dumps({"data": [article()]}))
        fake = Fake()
        self.assertEqual(fetch("gold", TOKEN, fake)["included"], 1)
        self.assertIn("api.marketaux.com/v1/news/all?", fake.request.full_url)
        class Reject:
            def open(self, request, timeout):
                raise urllib.error.HTTPError(request.full_url, 403, TOKEN, {}, None)
        with self.assertRaises(FeedError) as caught:
            fetch("gold", TOKEN, Reject())
        self.assertNotIn(TOKEN, str(caught.exception))
        self.assertNotIn("api_token", str(caught.exception))

    def test_no_secret_no_network_and_no_redirect(self):
        with self.assertRaises(FeedError):
            fetch("gold", "")
        with self.assertRaises(FeedError):
            NoRedirect().redirect_request(None, None, 302, "", {}, "https://example.org")


if __name__ == "__main__":
    unittest.main()
