#!/bin/bash
set -e

/usr/bin/curl -X POST http://spark:6066/v1/submissions/create \
  -H 'Content-Type: application/json' \
  -d '{
    "action": "CreateSubmissionRequest",
    "appResource": "/opt/spark-apps/jobs/kpi_aggregation.py",
    "clientSparkVersion": "3.5.1",
    "mainClass": "org.apache.spark.deploy.PythonRunner",
    "appArgs": [],
    "environmentVariables": {
      "PYSPARK_PYTHON": "python3"
    },
    "sparkProperties": {
      "spark.master": "spark://spark:7077",
      "spark.submit.deployMode": "cluster"
    }
  }'
