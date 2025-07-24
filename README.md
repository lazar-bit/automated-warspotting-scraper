# 🛰️ automated-warspotting-scraper

This Python-based automation tool periodically fetches and updates geolocated Russian equipment loss data from the [WarSpotting](https://warspotting.net) public API. It is designed for researchers, analysts, and developers interested in open-source intelligence (OSINT), conflict monitoring, and machine learning.

The scraper supports:

* ✅ **Full historical scans** (every Sunday)
* ✅ **Incremental 30-day scans** (on Monday, Thursday, and Friday)
* ✅ **Scheduled automation** via GitHub Actions
* ✅ **Output** in a single `CSV` file (`warspotting_losses.csv`), suitable for visualization and further analysis

---

## 📦 Repository Structure

```
automated-warspotting-scraper/
├── .github/
│   └── workflows/
│       └── scraper.yml         # GitHub Actions workflow (runs automatically)
├── automated_warspotting_scraper.py  # Main scraping script
├── warspotting_losses.csv     # Output data file (auto-updated)
└── README.md
```

---

## ⚙️ How It Works

* The GitHub Action (`scraper.yml`) triggers at **1:00 AM UTC**:

  * 🗓️ **Sunday:** Full scan of all available WarSpotting data
  * 🗓️ **Monday, Thursday, Friday:** 30-day rolling scan for recent updates
* The scraper collects data from both belligerents (Russia and Ukraine)
* Results are written to `warspotting_losses.csv`
* If there are any changes, the file is automatically committed back to the repository

---

## 🚀 Manual Execution

You can also run the script manually using GitHub's **"Run workflow"** button or locally with:

```bash
python automated_warspotting_scraper.py
```

Make sure Python 3.11+ is installed and dependencies (`pandas`, `requests`) are available.

---

## 🛠️ Requirements

* Python 3.11+
* Libraries:

  * `pandas`
  * `requests`

Install dependencies with:

```bash
pip install -r requirements.txt
```

(or manually if you prefer)

---

## 📊 Use Cases

* OSINT analysis of battlefield trends
* ML training data for predictive models
* Conflict monitoring dashboards
* Visualizing geospatial loss distributions

---

## 🧠 Credits & Disclaimer

* Data provided by [WarSpotting.net](https://warspotting.net)
* This project is for **educational and analytical** purposes only
* Not affiliated with WarSpotting or any official organization

---