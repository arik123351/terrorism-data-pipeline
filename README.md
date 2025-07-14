# Terrorism Data Analytics Pipeline

A real-time data pipeline for analyzing Global Terrorism Database (GTD) data using Apache Kafka, Apache Spark, and Elasticsearch.

## 🏗️ Architecture Overview

```
GTD Data (Kaggle) → Kafka Producer → Kafka Topic → Spark Streaming → Elasticsearch → Kibana Dashboard
```

## 📁 Project Structure

```
terrorism-pipeline/
├── docker-compose.yml          # Container orchestration
├── requirements.txt            # Python dependencies
├── README.md                  # This file
├── .env                      # Environment variables
├── data/                     # Data directory (auto-populated)
│   └── (GTD data from KaggleHub)
├── ingest/
│   └── kafka_producer.py     # Kafka data producer
├── spark/
│   ├── process_stream.py     # Stream processing
│   └── write_to_elasticsearch.py  # ES writer
├── elasticsearch/
│   └── setup_index.py        # ES index setup
└── notebooks/
    └── exploration.ipynb     # Data exploration
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.8+
- Git

### 1. Clone and Setup

```bash
git clone <repository-url>
cd terrorism-pipeline
```

### 2. Environment Setup

Create a `.env` file:
```bash
# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_TOPIC=terrorism

# Elasticsearch Configuration
ELASTICSEARCH_HOST=localhost
ELASTICSEARCH_PORT=9200
ELASTICSEARCH_INDEX=terrorism

# Spark Configuration
SPARK_MASTER_URL=spark://localhost:7077
CHECKPOINT_LOCATION=/tmp/checkpoint

# Data Configuration
BATCH_SIZE=1000
PROCESSING_INTERVAL=30s
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start Infrastructure

```bash
docker-compose up -d
```

Wait for all services to be ready (typically 2-3 minutes).

### 5. Verify Services

Check that all services are running:

```bash
# Check Kafka
docker-compose ps

# Check Elasticsearch
curl http://localhost:9200/_cluster/health

# Check Spark Master
curl http://localhost:8080

# Check Kibana (optional)
curl http://localhost:5601
```

## 📊 Running the Pipeline

### Step 1: Setup Elasticsearch Index

```bash
cd elasticsearch
python setup_index.py
```

**Expected Output:**
```
Index creation result: {'acknowledged': True, 'shards_acknowledged': True, 'index': 'terrorism'}
✅ Elasticsearch index created successfully
```

### Step 2: Start Data Ingestion

```bash
cd ingest
python kafka_producer.py
```

**Expected Output:**
```
INFO:__main__:Sent 1000 events
INFO:__main__:Sent 2000 events
...
INFO:__main__:Finished sending 181691 events with 0 errors
```

### Step 3: Process Stream Data

Choose one of the following:

**Option A: Console Output (for testing)**
```bash
cd spark
python process_stream.py
```

**Option B: Write to Elasticsearch (for production)**
```bash
cd spark
python write_to_elasticsearch.py
```

### Step 4: Explore Data

```bash
cd notebooks
jupyter notebook exploration.ipynb
```

Or run the exploration script directly:
```bash
cd notebooks
python -c "
import sys
sys.path.append('..')
from exploration import enhanced_data_exploration
enhanced_data_exploration()
"
```

## 🔧 Configuration

### Docker Services

| Service | Port | Purpose |
|---------|------|---------|
| Zookeeper | 2181 | Kafka coordination |
| Kafka | 9092 | Message streaming |
| Elasticsearch | 9200 | Data storage & search |
| Kibana | 5601 | Data visualization |
| Spark Master | 8080 | Spark cluster management |
| Spark Master | 7077 | Spark job submission |

### Key Configuration Files

**docker-compose.yml**
- Defines all services and their configurations
- Sets up persistent volumes for data
- Configures network communication

**requirements.txt**
- Lists all Python dependencies
- Pinned versions for reproducibility

**.env**
- Environment variables for configuration
- Sensitive data (if any)

## 📈 Data Flow

1. **Data Ingestion**: `kafka_producer.py` downloads GTD data from Kaggle and streams it to Kafka
2. **Stream Processing**: Spark processes the Kafka stream in real-time
3. **Data Storage**: Processed data is stored in Elasticsearch
4. **Visualization**: Kibana provides real-time dashboards

## 🎯 Features

### Real-time Processing
- Streams terrorism data in real-time
- Processes ~1000 events per second
- Low-latency data pipeline

### Data Enrichment
- Calculates total casualties (killed + wounded)
- Adds severity classification (Low/Medium/High/Critical)
- Timestamps for tracking

### Scalability
- Horizontal scaling with Spark workers
- Partitioned Kafka topics
- Elasticsearch clustering support

### Monitoring
- Comprehensive logging
- Error tracking and handling
- Performance metrics

## 📊 Sample Queries

### Elasticsearch REST API

```bash
# Get total attack count
curl -X GET "localhost:9200/terrorism/_count"

# Get attacks by year
curl -X GET "localhost:9200/terrorism/_search" -H 'Content-Type: application/json' -d'
{
  "size": 0,
  "aggs": {
    "attacks_by_year": {
      "terms": {
        "field": "iyear",
        "size": 50
      }
    }
  }
}'

# Get top countries by attack count
curl -X GET "localhost:9200/terrorism/_search" -H 'Content-Type: application/json' -d'
{
  "size": 0,
  "aggs": {
    "top_countries": {
      "terms": {
        "field": "country_txt.keyword",
        "size": 10
      }
    }
  }
}'
```

## 🐛 Troubleshooting

### Common Issues

**1. Kafka Connection Refused**
```bash
# Check if Kafka is running
docker-compose ps kafka

# Restart Kafka
docker-compose restart kafka
```

**2. Elasticsearch Index Issues**
```bash
# Delete and recreate index
curl -X DELETE "localhost:9200/terrorism"
python elasticsearch/setup_index.py
```

**3. Spark Job Failures**
```bash
# Check Spark logs
docker-compose logs spark-master

# Restart Spark cluster
docker-compose restart spark-master spark-worker
```

**4. Out of Memory Errors**
```bash
# Increase Docker memory allocation
# Edit docker-compose.yml and increase memory limits
```

### Performance Tuning

**Kafka Producer**
- Adjust `batch_size` and `linger_ms`
- Increase `buffer_memory` for higher throughput

**Spark Streaming**
- Tune `processingTime` trigger interval
- Adjust `maxOffsetsPerTrigger`

**Elasticsearch**
- Increase `refresh_interval` for better indexing performance
- Adjust `number_of_shards` based on data volume

## 📊 Monitoring & Metrics

### Kafka Monitoring
```bash
# List topics
docker exec -it $(docker-compose ps -q kafka) kafka-topics.sh --list --bootstrap-server localhost:9092

# Check topic details
docker exec -it $(docker-compose ps -q kafka) kafka-topics.sh --describe --topic terrorism --bootstrap-server localhost:9092
```

### Spark Monitoring
- Access Spark UI at `http://localhost:8080`
- Monitor streaming jobs and performance

### Elasticsearch Monitoring
```bash
# Cluster health
curl "localhost:9200/_cluster/health?pretty"

# Index statistics
curl "localhost:9200/terrorism/_stats?pretty"
```

## 🔒 Security Considerations

- Default configuration is for development only
- Production deployments should include:
  - Authentication and authorization
  - TLS encryption
  - Network security
  - Input validation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request



**Happy Analyzing! 🚀**