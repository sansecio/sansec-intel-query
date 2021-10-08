# Sansec Intel Query Tool

This is the reference (Python) client for the [Sansec Early Breach Detection Feed](https://sansec.io/kb/other/magecart-feed) (SEBDEF), which covers over a million online stores globally. The feed is updated continuously and shows:

- Recent detections for specific store URLs. A detection denotes a new or changed presence of suspicious code on a specific site. Multiple crawls of the same malware do not produce multiple "detections".
- Confidence levels (1-100). A confidence level of 100 indicates that we do not expect false positive hits for this specific match. Sub-100 detections may point to a false positive.
- Malware detection snippets with parent URL (may be a child asset of the the root URL)
- Meta information about the store, such as Alexa rank and detected platform name.

The default mode of the reference client is to return all detections for the previous 24h in text format.

![](https://buq.eu/screenshots/RGnypk3rxGlF44WYPglZHwyo.png)

Recommended usage is to poll daily, which is the default mode for the Python client. Use the `--json` flag in that case:

![](https://buq.eu/screenshots/2XbbSCumJGnyTcBZv15Awi9t.png)
