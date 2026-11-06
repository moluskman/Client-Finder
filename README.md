# Client Finder (AU Edition) 

A Python-based desktop application (GUI) designed for web developers to streamline client acquisition. This tool automatically searches local Australian business directories to find companies that completely lack a website, giving you a highly targeted list of leads who need web design services.

---

## Features

* **Simple Desktop GUI:** Built using Tkinter for a clean, lightweight user interface.
* **Background Threading:** Scraping tasks run on a separate thread, keeping the app responsive (no freezing) while fetching data.
* **403 Forbidden Bypass:** Powered by `curl_cffi` to mimic a real Chrome browser's TLS fingerprint, completely stopping anti-bot blocks.
* **Automatic Filtering:** Instantly filters out any businesses that already have a website listed.
* **CSV Export:** Saves your fresh leads into a structured `leads.csv` file automatically.
* **One-Click Clear:** Includes a built-in reset button to wipe your spreadsheet clean between searches.

---
