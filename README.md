# Mood-Analytics: Bridging the gap between physical interaction and digital insight.

![](images/bar%20chart.png)
![](images/summary.png)

This repository provides a specialized data analysis pipeline and an interactive web dashboard designed to transform raw emotional logs into actionable insights. It serves as the **Software Engine** for the [PicoW-Mood-Tracker](https://github.com/KELEE0810/pico-w-mood-tracker) project.

## 0. Introduction
Data is most powerful when it tells a story. While the **Pico W Mood-Tracker** device focuses on the tactile "Click" to capture emotions in the physical world, this project focuses on the "Analysis" to understand the patterns behind those clicks.
This system helps you visualize your emotional well-being and track long-term trends.

### Project Ecosystem
This analytics suite is the second half of a two-part ecosystem:
1. **The Logger ([PicoW-Mood-Tracker](https://github.com/KELEE0810/pico-w-mood-tracker))**: An IoT device that logs moods to Google Sheets.
2. **The Analyzer (This Repo)**: A Python-based suite that fetches, processes, and visualizes that data.

---

## 1. Key Analytical Features

### 1. Trend Forecasting (Linear Regression)

![Forecasting Your Moods](images/regression%20line.png)

By mapping qualitative mood labels to quantitative scores, the system calculates a **Regression Slope** to determine your emotional trajectory over time.
* **Positive Slope**: Indicates a steady upward trend in your well-being.
* **Negative Slope**: Suggests a downward trend, signaling a need for rest.


### 2. Emotional Volatility Analysis

![Volatility of Your Moods](images/vix%20chart.png)

This script analyzes the stability of your emotions through advanced statistical metrics:
* **Standard Deviation (SD)**: Measures how much your mood scores deviate from the average.
* **Average Mood Swing**: Calculates the mean of absolute differences between consecutive records to quantify emotional turbulence.
* **Volatility Visualization (VIX)**: A dedicated chart that plots score changes between entries to identify stability patterns.


### 3. Visual Insights

![Time Series of Your Moods](images/time%20series.png)
![WordCloud of Your Moods](images/wordcloud.png)

* **Frequency Analysis**: Identify dominant emotions using Seaborn-powered bar charts.
* **Time-Series Tracking**: Maps every emotional data point over a timeline to identify specific patterns.
* **Emoji WordCloud**: Generates an intuitive visual cloud of your most frequently recorded emojis.

---

## 2. Quick Start

### 1. Installation
Install the necessary dependencies:
```bash
pip install pandas seaborn matplotlib scikit-learn wordcloud
```

### 2. Connection
Update the url variable in main.py with your Google Sheets CSV URL:

1) Go to Google Sheets > File > Share > Publish to web.
2) Select Comma-separated values (.csv) and click Publish.
3) Copy and paste the link into the code.

### 3. Usage
For local analysis: python3 main.py
