Real-Time E-Commerce Streaming Analytics Pipeline

This project implements a real-time Big Data analytics pipeline for an e-commerce domain using the Olist Brazilian dataset as the behavioral foundation. The system continuously ingests simulated streaming orders, performs minute-level KPI aggregation using Spark, orchestrates workflows using Airflow, stores fresh data in MongoDB, archives historical data in Hadoop, and serves live KPIs through a Flask-based BI dashboard.

The solution demonstrates end-to-end streaming analytics, dimensional KPI modeling, and automated batch+stream orchestration.

**🎯 Business Problem**

E-commerce managers need real-time visibility into:

- regional demand trends
- revenue and order surges
- product category performance
- operational anomalies (refund spikes, drops in orders)

Traditional batch reporting introduces delays that impact:

- stock allocation
- marketing response time
- logistics operations
- customer experience

This system enables real-time decision support via continuously updating dashboards.

**🧱 System Architecture**

Pipeline Overview

Data Generator ➝ MongoDB (Hot Storage) ➝ Spark Aggregation ➝ KPI Store ➝ Flask API ➝ Dashboard

Historic Data ➝ Archived to Hadoop (HDFS)

Airflow orchestrates the entire workflow.

🛠️ Technologies Used
- Containerization: Docker & Docker Compose
- Streaming Storage:	MongoDB
- Processing Engine:	Apache Spark
- Workflow Orchestration:	Apache Airflow
- Archive Storage:	Hadoop HDFS
- Serving Layer:	Flask API
- Dashboard UI:	HTML + JS (auto refresh)

**🧩 Data Model**
**Streaming Collection — orders_stream**
Stores live incoming orders.

Field              	Description
order_id	          unique order identifier
timestamp	          event time
customer_state	    buyer region
items[]	            product list with quantity & price
payment_value	      total purchase value

**Aggregated KPI Collection — kpi_minute**
Computed via Spark per-minute batches.

**Field**	             **Description**
minute	               aggregation time window
customer_state	       region dimension
product_category	     product dimension
total_orders	         number of orders
total_items	           quantity sold
total_sales	           total revenue
avg_order_value	       mean order value

Supports GROUP BY / HAVING dimensional queries.

**🗄️ Archiving Policy**

To prevent uncontrolled growth of streaming storage:

✔ MongoDB maintains ~300MB of recent data
✔ Older partitions are archived to HDFS (Parquet format)
✔ Archive metadata is logged (batch id, size, time window, path)

This preserves:

- replayability
- auditability
- low-latency hot storage

**⚙️ Pipeline Orchestration (Airflow)**

The Airflow DAG:

- runs on a periodic schedule (demo: ~1 minute)
- triggers Spark KPI aggregation
- updates Mongo KPI collection
- refreshes dashboard data source

DAG: spark_kpi_pipeline
Task: run_spark_kpi_job

**🚀 Running the Project**

**Clone repository:**
git clone git@github.com:<your-user>/bdaproject.git
cd bdaproject

**Start full stack:**
docker compose up -d

**Verify services:**

docker ps

**✅ Access Components**
Service	URL
Dashboard API	http://localhost:5000
Airflow Web UI	http://localhost:8080

Mongo Console	inside container
Spark Master UI	if exposed → 7077 / 8081
Login (Airflow)

Default admin user (or your manually created credentials):

username: admin
password: admin

📡 Demo Verification Commands

Latest incoming streaming records:

docker exec -it mongo \
mongo bda_project --eval \
'db.orders_stream.find().sort({timestamp:-1}).limit(5)'


Latest KPI document:

docker exec -it mongo \
mongo bda_project --eval \
'db.kpi_minute.find().sort({minute:-1}).limit(1)'


Airflow DAG runs:

docker exec -it airflow-scheduler \
airflow dags list-runs -d spark_kpi_pipeline

🖥️ Dashboard

The Flask dashboard exposes live KPIs via:

/kpi/latest
/kpi/query?category=<cat>
/kpi/query?state=<state>


Front-end refreshes automatically to simulate live BI streaming analytics.

🧪 Validation Outcomes

✔ Streaming ingestion works continuously
✔ Spark computes dimensional KPIs
✔ Airflow schedules aggregation runs
✔ Dashboard updates from live collection
✔ Archiving strategy prevents storage overflow

Dataset basis: Olist Brazilian E-Commerce Public Dataset
Project developed as part of Big Data Analytics coursework.
