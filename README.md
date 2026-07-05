# Website Defacement Monitor

A defensive security tool written in Python designed to track web page integrity and instantly detect unauthorized alterations or defacement attempts.

## 🚀 Features

* **Integrity Hashing (SHA-256)**: Computes and continuously verifies the cryptographic hash signature of the target page's source code.
* **Signature/Keyword Matching**: Scans the target page content for well-known indicator terms frequently used by threat actors (e.g., "Hacked", "Security Failed").
* **Local Lab Simulation Setup**: Supports parsing local staging `.html` layouts out-of-the-box to simulate defensive testing workflows safely.

## 🛠️ Configuration (`config.json`)

```json
{
    "target_url": "test-samples/hacked-page.html",
    "check_interval_seconds": 10,
    "is_local_file": true,
    "alert_keywords": ["hacked", "defaced", "security has failed"]
}


```
- target_url: The link or local path to watch.
- is_local_file: Toggle true for file system templates, false for active live URLs (http://...).

## 💻 Usage
Run the tracking loop straight from your terminal:

Bash

python monitor.py
