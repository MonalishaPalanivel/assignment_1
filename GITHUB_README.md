
# 🎬 IMDb 2024 — Data Scraping & Visualizations

---

## 📌 Overview

**IMDb 2024 Data Scraping & Visualizations** is an end-to-end project that scrapes movie data for 2024 from IMDb using **Selenium**, stores it in **MySQL**, and provides an **interactive Streamlit dashboard** for exploring top movies, genres, durations, votes, and ratings.

---

## 🚀 Skills & Tech Stack

- **Languages:** Python
- **Libraries:** Selenium, Pandas, SQLAlchemy, Streamlit, Plotly
- **Database:** MySQL
- **Concepts:** Web Scraping · Data Cleaning · Data Analysis · Visualization · Interactive Filtering

---

## ✅ Problem Statement

- Scrape all IMDb feature films released in 2024.
- Extract: **Title**, **Genre**, **Rating**, **Votes**, **Duration**.
- Store genre-wise CSVs → merge → upload to **SQL**.
- Build an **interactive dashboard** for dynamic visual insights.

---

## 📂 Project Structure

```
📁 imdb_2024_project/
 ├── scrape_imdb.py
 ├── upload_to_sql.py
 ├── dashboard.py
 ├── interactive_filter.py
 ├── 📁 csv/
 ├── README.md
```

---

## 🔗 How It Works

### 1️⃣ Scraping
- Uses Selenium to load IMDb’s 2024 movie page.
- Extracts data and saves genre-wise CSV files.

### 2️⃣ Database Upload
- Merges CSVs into one DataFrame.
- Uploads to MySQL using SQLAlchemy.

### 3️⃣ Interactive Dashboard
- Streamlit app with:
  - Top 10 movies by **Rating** & **Votes**
  - **Genre Distribution**
  - **Average Duration** by Genre
  - **Voting Trends**
  - **Heatmaps**, **Histograms**, **Correlation**
  - Shortest & Longest movies
  - Genre-based leaders
  - **Advanced Filter Page**: filter by duration, votes, ratings, genre

---

## ⚙️ Getting Started

### 📦 Install

```bash
pip install selenium pandas sqlalchemy pymysql streamlit plotly
```

### ▶️ Run Scraper

```bash
python scrape_imdb.py
```

### ⬆️ Upload to SQL

```bash
python upload_to_sql.py
```

### 🖥️ Launch Dashboard

```bash
streamlit run dashboard.py
```

### 🎯 Open Advanced Filter

```bash
streamlit run interactive_filter.py
```

---

## 🗃️ Database

- **Name:** `DATA_2024`
- **Table:** `imdb_movies`
- **Fields:** Title · Genre · Rating · Votes · Duration

---

## 📊 Key Visuals

✔️ Top 10 Movies  
✔️ Genre Distribution  
✔️ Average Durations  
✔️ Voting Patterns  
✔️ Rating Histograms & Boxplots  
✔️ Genre Leaders  
✔️ Correlation (Votes vs Ratings)  
✔️ Interactive Filtering  

---


---


---

