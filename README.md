# 📊 PhonePe Data Insights Dashboard

An interactive Streamlit dashboard that visualizes PhonePe usage trends, insurance penetration, device engagement, and user behavior across Indian states and districts.

Built using data sourced from the official [PhonePe Pulse GitHub repository](https://github.com/PhonePe/pulse), this project leverages structured SQLite databases and rich visualizations to deliver business-level insights.

---

## 🔧 Tools & Technologies

| Category        | Tools Used                                       |
|----------------|---------------------------------------------------|
| Language        | Python 3.11                                      |
| Data Processing | Pandas, SQLite3                                  |
| Visualization   | Plotly, Seaborn, Matplotlib                      |
| Web App         | Streamlit                                        |
| Data Source     | [PhonePe Pulse](https://github.com/PhonePe/pulse)|
| Others          | Jupyter Notebooks, Git                           |

---

## 🗂️ Directory Structure

```

.
├── db/                     # SQLite database (auto-generated)
│   └── phonepe_data.db
├── data/                  # Raw JSON files from PhonePe Pulse
├── notebooks/             # EDA and visual insights
│   └── insights_visualization.ipynb
├── scripts/               # Scripts for DB creation & data ingestion
│   ├── create_all_tables.py
│   ├── load_aggregated_*.py
│   └── db_utils.py
├── streamlit_app/         # Streamlit Dashboard app
│   ├── app.py
│   ├── utils.py
│   ├── plots/
│   │   └── charts.py
│   └── assets/
├── requirements.txt
├── README.md
└── .gitignore

````

---

## 🚀 Setup Instructions

### ✅ 1. Clone the Repository

```bash
git clone https://github.com/your-username/phonepe-insights.git
cd phonepe-insights
````

### 📦 2. Install Dependencies

Create and activate a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate       # For Windows: venv\Scripts\activate
```

Then install required packages:

```bash
pip install -r requirements.txt
```

### 📁 3. Download Raw Data

Download the PhonePe Pulse dataset from the official repo:

👉 [https://github.com/PhonePe/pulse](https://github.com/PhonePe/pulse)

* Navigate to the `data` directory in this project.
* Copy the relevant folders such as `aggregated/` and `map/` into `/data`.

Your structure should look like:

```
/data
├── aggregated
│   ├── transaction
│   ├── user
│   └── insurance
└── map
    └── user
```

> **Important**: Keep the folder structure as above for the scripts to work correctly.

---

### 🧱 4. Generate the Database

Run the following commands one by one to create the schema and populate your SQLite database.

```bash
python scripts/create_all_tables.py
python scripts/load_aggregated_transactions.py
python scripts/load_aggregated_user.py
python scripts/load_aggregated_insurance.py
python scripts/load_map_user.py
```

> This will create `phonepe_data.db` under the `/db` folder.

---

### ▶️ 5. Launch the Streamlit Dashboard

```bash
streamlit run streamlit_app/app.py
```

Open your browser and go to [http://localhost:8501](http://localhost:8501)

---

## 📊 Dashboard Features

* **Transactions**:

  * Top 10 states by total transaction amount
  * Quarterly transaction trends of top states

* **Device Usage**:

  * Interactive year/quarter selection
  * Brand share vs registered user engagement

* **Insurance**:

  * State-level insurance penetration
  * Trend over time by geography

* **User Insights**:

  * Top districts by app opens
  * Low-conversion districts (high registration but low usage)

* **Statewise KPIs**:

  * KPI cards for selected state
  * KPI trends over time
  * Comparison with national averages

---



## 🧠 Contributions & Ideas

Feature suggestions or pull requests are welcome. Some potential improvements:

* Add district-level map visualizations
* Deploy to Streamlit Cloud or HuggingFace Spaces
* Export analysis reports to PDF
* Add filters for custom comparison

---

