# Sansec Intel Query Tool

This is the reference (Python) client for the [Sansec Early Breach Detection Feed](https://sansec.io/kb/other/magecart-feed) (SEBDEF). This feed contains malware detections for over a million online stores, which are checked continuously by our crawler network. The feed exposes the following information:

- Recent detections for specific store URLs. A detection denotes a new or changed presence of suspicious code on a specific site. Multiple crawls of the same malware do not produce multiple "detections". Detection timestamps are always in UTC standard time.
- Confidence levels (1-100). A confidence level of 100 indicates that we do not expect false positive hits for this specific match. Sub-100 detections may point to a false positive.
- Malware detection snippets with parent URL (may be a child asset of the the root URL)
- Meta information about the store, such as Alexa rank and detected platform name.

The default mode of the reference client is to return all detections for the previous 24h in text format.

![](https://buq.eu/screenshots/RGnypk3rxGlF44WYPglZHwyo.png)

Recommended usage is to poll daily, which is the default mode for the Python client. Use the `--json` flag in that case:

![](https://buq.eu/screenshots/2XbbSCumJGnyTcBZv15Awi9t.png)

# API reference

## Request

API endpoint URL: https://intel.sansec.io/v3/detection

API authentication requires a `X-API-Key` HTTP header with your given license key.

API parameters can be given as GET query strings or POST form data. All parameters are optional.

| Param    | Usage                                                                                                                                                |
| -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| host     | Limit results to this parent host/domain.                                                                                                            |
| platform | Limit results to this platform. Can be used multiple times. Possible platforms: magento, bigcommerce, prestashop, opencart. More to be added.        |
| limit    | Maximum number of results per page. Defaults to 20.                                                                                                  |
| page     | For pagination, first `page` has index 0. It is recommended though to use the `next` link, which will be given if there are more results availalble. |
| from, to | Limit detections that were made after `from` and/or before `to`. Timestamps should be specified in RFC3339 format like this: `2021-10-26T15:20:30Z`  |
| period   | Use `yesterday` to automatically select yesterday's detections (in UTC timezone).                                                                    |
| format   | Returns data in `json` or `csv`. Using `json` is recommended and default.                                                                            |

Curl usage examples

```sh
# Default response in JSON:
curl -H "X-API-Key: demo-key" https://intel.sansec.io/v3/detection?platform=opencart

# Get yesterday's detections in CSV:
curl -H "X-API-Key: demo-key" https://intel.sansec.io/v3/detection?format=csv&period=yesterday
```

## Response in JSON

A response contains zero or more detections. A "detection" is a change in our registered malware status for a particular store. It can be triggered by one of these events:

1. Malware code is either added to or removed from a store. When a new malware is injected, it will trigger a new injection. When an infected store is down for maintenance and serves an empty page, it will trigger a new detection ("all clear")
2. Sansec adds or removes signatures that may trigger for a particular store. For example, when we change the confidence level for a particular signature from "experimental" to "accurate", it will likely produce new detections.

NB. This means that not all detections are induced by the behavior of scanned stores.

| Param              | Semantic                                                                                                                                                                                                                                            |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| detected_at        | The RFC3339 timestamp for a site visit by our crawler that led to a new detection.                                                                                                                                                                  |
| max_trust          | The maximum confidence level of all matched signatures for a particular store detection. With max_trust = 100, we do not expect any false positives. Special case: with max_trust = 0, none of our signatures matched and the site is likely clean. |
| store.url          | The canonical URL of a store (after redirects)                                                                                                                                                                                                      |
| detections.snippet | The actual (malware) code that matched one of our signatures. The actual malware may be bigger than just the snippet.                                                                                                                               |
| detections.source  | The URL serving the detected malware. This may differ from the store.url, as malware is often hidden in embedded JS files.                                                                                                                          |

## Response in CSV

CSV format uses a single line per affected store.

| Field         | Semantic                                                                                                                                          |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| Timestamp     | UTC timestamp for last new detection                                                                                                              |
| Domain        | Domain name of store                                                                                                                              |
| Platform      | Platform name, such as magento, woocommerce, shopware                                                                                             |
| Confidence    | Maximum of confidence levels for all detections for this specific store. Range 1-100.                                                             |
| Canonical URL | The main canonical URL for the store (after any redirections)                                                                                     |
| Parent URL    | The URL that contained malicious code. This may equal the Canonical URL, but can also be an external URL that was referenced by the Canonical URL |
| Snippet       | The specific piece of code that triggered our detection signature                                                                                 |
