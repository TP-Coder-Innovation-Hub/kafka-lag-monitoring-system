# 🚀 Kafka Lag Monitoring System (Prometheus & Grafana)

This project provides a complete, containerized stack for monitoring Kafka consumer lag in real-time using **Prometheus** for data collection and **Grafana** for visualization.

## 📦 Project Stack

| Component | Port | Description |
| :--- | :--- | :--- |
| **Kafka** | `9092` | The messaging broker. |
| **Kafka Exporter** | `9308` | Exposes Kafka metrics (including lag) for Prometheus. |
| **Prometheus** | `9090` | Time-series database that scrapes metrics from the Exporter. |
| **Grafana** | `3000` | Dashboard tool for visualizing the lag data. |
| **Zookeeper** | `2181` | Coordinates the Kafka cluster. |

## ⚙️ Prerequisites

* **Docker** and **Docker Compose** installed on your system.
* **Python 3** and `kafka-python` installed for the test scripts: `pip install kafka-python`.

## 🛠️ Setup and Installation

### 1. Project Structure

Ensure your project directory is set up correctly:

kafka-lag-monitoring-system/ 
    ├── docker-compose.yml 
    ├── src
        ├── kafka_consumer.py 
        ├── kafka_producer.py 
    └── prometheus/ 
        └── prometheus.yml

### 2. Start the Stack

Run the following command in the root of your project directory (`kafka-lag-monitoring-system/`):
```bash
docker-compose up -d
```

## 📈 Initial Grafana Setup
1. Log in to Grafana (http://localhost:3000) with admin/admin.
2. Add Prometheus Data Source:
    2.1. Go to Configuration (cog icon) > Data Sources.
    2.2. Click Add data source and select Prometheus.
    2.3. Set the URL to: http://prometheus:9090
    2.4. Click Save & test.
3. Import Dashboard (Optional but Recommended):
    3.1. Go to Dashboards > Import.
    3.2. Use Grafana.com Dashboard ID: 7589 (A general Kafka Exporter dashboard).
    3.3. Select your Prometheus data source and click Import.

## 📊 Viewing the Consumer Lag
The crucial query to use in a Grafana panel is:
```bash
sum(kafka_consumergroup_lag) by (consumergroup, topic)
```
This query aggregates the lag across all partitions and shows the total lag per consumer group and topic.

## 🧪 Monitoring Verification (The Lag Test)
To confirm the entire monitoring pipeline is working:
1. Start Producer (Terminal 1): python kafka_producer.py
2. Start Consumer (Terminal 2): python kafka_consumer.py (Lag is 0).
3. Simulate Lag: Stop the consumer in Terminal 2 (Ctrl+C). Watch the lag climb in Grafana.
4. Resume: Restart the consumer in Terminal 2. Watch the lag drop back to 0.

🛑 Stopping the Project
When finished, stop and clean up the containers:
```bash 
docker-compose down
```