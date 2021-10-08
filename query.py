#!/usr/bin/env python3

import argparse
import requests
import json
import sys
from datetime import datetime, timedelta

try:
    # optional colored output
    from rich import print
except ImportError:
    pass


API_URL = "https://intel.sansec.io/v3/detection"
MAX_RESULTS = 200


def query(**kwargs):
    api_key = kwargs.pop("key", "")
    max_results = kwargs.pop("max_results", MAX_RESULTS)

    counter = 0
    while True:
        resp = requests.get(API_URL, headers={"X-API-Key": api_key}, params=kwargs)
        obj = resp.json()

        if resp.status_code != 200 or "data" not in obj:
            print("Error:")
            print_json(obj)
            sys.exit(1)

        for item in obj["data"]:
            counter += 1
            yield item
            if counter >= max_results:
                break

        if not obj.get("next"):
            break

        if obj["query"]["page"] >= 10:  # hard page limit
            break

        kwargs["page"] = kwargs.get("page", 0) + 1


def last24h():
    # Format in RCF3339
    lasthour = datetime.utcnow() - timedelta(days=1)
    return lasthour.isoformat() + "Z"


def print_text(items):
    for item in items:
        print(
            "\n{max_trust:3d} {detected_at} {store[host]} ({store[platform]}/{store[rank_alexa]}) ".format(
                **item
            )
        )
        for det in item["detections"]:
            print("\t{confidence:3d} {source} {snippet}".format(**det))

    print(f"\nReceived {len(items)} detections.")


def print_json(obj):
    print(json.dumps(obj, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sansec Intel Query Tool")
    parser.add_argument("--key", help="License key", required=True)
    parser.add_argument("--host", help="Search for specific host/domain.")
    parser.add_argument(
        "--max-results", help="Max results to return", default=MAX_RESULTS, type=int
    )
    parser.add_argument("--platform", help="Select platform (magento, prestashop, ...)")
    parser.add_argument(
        "--json",
        help="Dump raw JSON output instead of text summary",
        action="store_true",
    )
    args = parser.parse_args()

    param = dict(max_results=args.max_results, key=args.key)

    if args.json:
        formatter = print_json
    else:
        formatter = print_text

    if args.host:
        param["host"] = args.host
    else:
        param["from"] = last24h()

    results = list(query(**param))
    formatter(results)
