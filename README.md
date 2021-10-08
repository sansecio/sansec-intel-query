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

API endpoint URL: https://intel.sansec.io/v3/detection

API parameters can be given as GET query strings or POST form data. All parameters are optional.

| Param    | Meaning                                                                                                                                              |
| -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| host     | Limit results to this parent host/domain.                                                                                                            |
| platform | Limit results to this platform. Can be used multiple times. Possible platforms: magento, bigcommerce, prestashop, opencart. More to be added.        |
| limit    | Maximum number of results per page. Defaults to 20.                                                                                                  |
| page     | For pagination, first `page` has index 0. It is recommended though to use the `next` link, which will be given if there are more results availalble. |
| from, to | Limit detections that were made after `from` and/or before `to`. Timestamps should be specified in RFC3339 format like this: `2021-10-26T15:20:30Z`  |
