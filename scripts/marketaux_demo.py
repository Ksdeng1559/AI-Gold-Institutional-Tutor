"""One-shot server/local news snapshot. No browser credentials or background polling."""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

ENDPOINT = "https://api.marketaux.com/v1/news/all"
SEARCHES = {
    "gold": 'gold | bullion | "Federal Reserve" | "dollar index" | "Treasury yields" | oil',
    "crypto": 'bitcoin | BTC | ethereum | crypto',
}


class FeedError(Exception):
    """Safe error message; never include authenticated URLs or raw provider responses."""


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise FeedError("Unexpected provider redirect; request stopped.")


def normalize(payload, topic, token):
    if not isinstance(payload, dict) or not isinstance(payload.get("data"), list):
        raise FeedError("Invalid provider response; no snapshot produced.")
    if payload.get("error") or payload.get("errors"):
        raise FeedError("Provider returned an error; no snapshot produced.")
    articles, seen = [], set()
    for row in payload["data"]:
        if not isinstance(row, dict):
            continue
        values = {name: row.get(name) for name in ("uuid", "title", "url", "source", "published_at", "language")}
        if not all(isinstance(values[k], str) and values[k] for k in ("uuid", "title", "url", "published_at")):
            continue
        if any(token in value for value in values.values() if isinstance(value, str)):
            continue
        link = urllib.parse.urlsplit(values["url"])
        if link.scheme not in ("https", "http") or not link.netloc or link.username or link.password:
            continue
        try:
            stamp = datetime.fromisoformat(values["published_at"].replace("Z", "+00:00"))
            if stamp.tzinfo is None:
                continue
        except ValueError:
            continue
        if values["uuid"] in seen:
            continue
        seen.add(values["uuid"])
        articles.append(values)
    articles.sort(key=lambda a: datetime.fromisoformat(a["published_at"].replace("Z", "+00:00")), reverse=True)
    meta = payload.get("meta")
    meta = meta if isinstance(meta, dict) else {}
    return {
        "provider": "Marketaux", "mode": "one-shot snapshot", "topic": topic,
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "coverage": "limited search results; not an exhaustive news feed",
        "query": {"search": SEARCHES[topic], "language": "en", "page": 1, "limit": 3},
        "provider_meta": {k: meta.get(k) if isinstance(meta.get(k), int) else None for k in ("found", "returned", "limit", "page")},
        "included": len(articles), "articles": articles,
    }


def fetch(topic, token, opener=None):
    if not token or token != token.strip() or any(c.isspace() for c in token):
        raise FeedError("Set MARKETAUX_API_TOKEN to the exact token in private environment settings.")
    params = {"api_token": token, "search": SEARCHES[topic], "language": "en",
              "group_similar": "true", "sort": "published_at", "limit": 3, "page": 1}
    request = urllib.request.Request(ENDPOINT + "?" + urllib.parse.urlencode(params),
                                     headers={"Accept": "application/json"})
    opener = opener or urllib.request.build_opener(NoRedirect)
    try:
        with opener.open(request, timeout=20) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as error:
        raise FeedError(f"News request failed (HTTP {error.code}); no snapshot produced.") from None
    except (urllib.error.URLError, TimeoutError, OSError, ValueError):
        raise FeedError("News request unavailable or invalid; no snapshot produced.") from None
    return normalize(payload, topic, token)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--topic", choices=SEARCHES, default="gold")
    args = parser.parse_args()
    try:
        result = fetch(args.topic, os.environ.get("MARKETAUX_API_TOKEN", ""))
    except FeedError as error:
        print(str(error), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
