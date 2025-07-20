
# 🚢 Shipping a Data Product: From Raw Telegram Data to an Analytical API

An end-to-end data pipeline project that processes raw Telegram data and transforms it into enriched, queryable analytics. The pipeline integrates modern data tools such as **Dagster**, **dbt**, **PostgreSQL**, and **YOLOv8** for automated orchestration, transformation, and AI-driven enrichment.

---

## 📦 Project Overview

This project demonstrates how to build and deploy a complete data product:

1. **Data Ingestion** from Telegram using a bot that listens to a channel or group.
2. **Storage** of raw data into PostgreSQL via a streaming pipeline.
3. **Transformation** using `dbt` for cleaning, modeling, and aggregating Telegram data.
4. **Enrichment** of data with image processing using `YOLOv8` for object detection.
5. **Orchestration** using `Dagster` for scheduling and monitoring.
6. **Exposure** via an analytical API (optional).

---

## 🧰 Tech Stack

| Layer              | Tools Used                |
|-------------------|---------------------------|
| Ingestion         | Python Telegram Bot       |
| Storage           | PostgreSQL                |
| Transformation    | dbt                       |
| Enrichment        | YOLOv8 (Ultralytics)      |
| Orchestration     | Dagster                   |
| Deployment        | Docker + docker-compose   |
| Logging & Testing | Python logging, Pytest    |

---

## 📁 Project Structure

```bash
telegram_data_pipeline/
├── dags/                    # Dagster pipeline definitions
├── dbt/                     # dbt models and transformation logic
├── ingestion/               # Telegram bot and raw data ingestion
├── enrichment/              # YOLOv8 image tagging and metadata extraction
├── api/                     # (Optional) FastAPI service for data queries
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
````

---

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/Bisrath1/telegram_data_pipeline.git
cd telegram_data_pipeline
```

### 2. Create `.env` File

```env
# .env
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin123
POSTGRES_DB=telegram_db
```

### 3. Run with Docker

```bash
docker-compose up --build
```

This will spin up:

* PostgreSQL DB
* Dagster web UI (`localhost:3000`)
* Your ingestion & enrichment pipeline

---

## 🧠 Features

* 📥 **Telegram Listener**: Continuously scrapes messages from a Telegram channel or group.
* 📸 **YOLOv8 Integration**: Detects objects in images posted on Telegram and stores metadata.
* 🧹 **dbt Transformation**: Applies SQL-based data modeling to raw data.
* 🔁 **Dagster Orchestration**: Automates the pipeline and monitors health of tasks.
* 📊 **API-Ready Data**: Final outputs can be connected to BI tools or served via API.

---

## 🧪 Testing

Run tests locally:

```bash
pytest
```

---

## 📈 Future Improvements

* Add FastAPI for querying enriched data
* Integrate Superset for dashboards
* Add alerting on pipeline failure
* Add CI/CD for auto-deployments

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a PR if you'd like to contribute or suggest a feature.

---

## 📄 License

MIT License. See `LICENSE` file for details.

---

## 🙋‍♂️ Author

**Bisrat Haile**  
Python Developer   
ML Intern | AI Enthusiast  
📧 bisrathaile1919@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/bisrat-haile) | [GitHub](https://github.com/Bisrath1)

---
