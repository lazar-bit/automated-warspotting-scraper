# 🛰️ automated-warspotting-scraper

This Python-based automation tool periodically fetches and updates geolocated Russian equipment loss data from the [WarSpotting](https://warspotting.net) public API. It is designed for researchers, analysts, and developers interested in open-source intelligence (OSINT), conflict monitoring, and machine learning.

The scraper supports:

* ✅ **Full historical scans** (every Sunday)
* ✅ **Incremental 30-day scans** (every Monday, Tuesday, Wednesday, Thursday, Friday, Saturday)
* ✅ **Scheduled automation** via GitHub Actions
* ✅ **Output** in a single `CSV` file (`warspotting_losses.csv`), suitable for visualization and further analysis
* ✅ **Automatic upload of the updated dataset to [Kaggle](https://www.kaggle.com/datasets/zsoltlazar/automated-warspotting-equipment-losses)** for easy access and sharing

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

> **Note:** The Kaggle dataset upload process creates a temporary `kaggle_dataset` folder inside the GitHub Actions runner environment to prepare files for upload. This folder **is not created or committed** inside GitHub repository and does not affect repo structure.

## ⚙️ How It Works

* The GitHub Action (`scraper.yml`) triggers at **1:00 AM UTC**:

  * 🗓️ **Sunday:** Full scan of all available WarSpotting data
  * 🗓️ **Monday, Wednesday, Friday:** 30-day rolling scan for recent updates

* Results are written to `warspotting_losses.csv`

* If there are any changes, the file is automatically committed back to the repository

* The updated CSV dataset is then uploaded to [Kaggle](https://www.kaggle.com/datasets/zsoltlazar/automated-warspotting-equipment-losses) via the Kaggle API, keeping the public dataset current and accessible

---

## 🛠️ Requirements

* Python 3.11+
* Libraries:

  * `pandas`
  * `requests`
  * `kaggle`  *(for uploading dataset to Kaggle)*

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
* Easy data access via [Kaggle dataset](https://www.kaggle.com/datasets/zsoltlazar/automated-warspotting-equipment-losses)

---

## 🧠 Credits & Disclaimer

* Data provided by [WarSpotting.net](https://warspotting.net)
* This project is for **educational and analytical** purposes only
