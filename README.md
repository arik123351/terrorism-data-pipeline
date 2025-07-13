
# 🧠 Terrorism Big Data Pipeline

This project builds a real-time ETL pipeline to analyze global terrorism data using HDFS, Apache Kafka, Spark, and Elasticsearch. Visualizations are generated using Jupyter notebooks.

---

## 🚀 Technologies Used
- HDFS (data lake storage)
- Apache Kafka (streaming ingestion)
- Apache Spark (stream processing)
- Elasticsearch (NoSQL storage & search)
- JupyterLab (data exploration & visualization)
- Docker Compose (orchestration)

---

## 📦 Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd terrorism-data-pipeline
```

### 2. Place Dataset
Download the Global Terrorism Database from Kaggle and place `gtd.csv` into the `data/` folder.

### 3. Start the Infrastructure
```bash
docker-compose up -d
```
This launches Zookeeper, Kafka, Elasticsearch, HDFS, and Spark.

### 4. Upload Raw Data to HDFS
```bash
bash hdfs/upload_to_hdfs.sh
```

### 5. Create Elasticsearch Index
```bash
python3 elasticsearch/setup_index.py
```

### 6. Start Kafka Producer
```bash
python3 ingest/kafka_producer.py
```
This simulates a real-time stream of terrorism events.

### 7. Run Spark Job to Write to Elasticsearch
```bash
spark-submit spark/write_to_elasticsearch.py
```

### 8. Explore the Data
Start Jupyter:
```bash
jupyter lab
```
Open the notebook at `notebooks/exploration.ipynb`.

---

## 📊 Example Visualizations
- Number of attacks per year
- Casualties per region
- Top active terrorist groups

---

## 📁 Directory Structure
```
.
├── data/                  # Original GTD CSV
├── ingest/                # Kafka producer
├── spark/                 # Stream processors
├── elasticsearch/         # Index setup
├── hdfs/                  # HDFS upload script
├── notebooks/             # JupyterLab analytics
├── docker-compose.yml     # Service orchestration
└── requirements.txt       # Python dependencies
```

---

## ✅ To Do
- Add REST API for real-time query
- Deploy Kibana for rich dashboards
- Add unit tests and monitoring

---

Feel free to fork, contribute, or reach out with questions!