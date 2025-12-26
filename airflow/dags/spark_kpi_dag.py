from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=1)
}

dag = DAG(
    dag_id="spark_kpi_pipeline",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule_interval="*/1 * * * *",   # runs every 30 minutes
    catchup=False
)

run_spark_job = BashOperator(
    task_id="run_spark_kpi_job",
    dag=dag,
    bash_command="bash /opt/scripts/run_spark_kpi.sh"

)

'''
    bash_command="""
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
            "spark.submit.deployMode": "cluster",
            "spark.driver.supervise": "false"
        }
    }'
    """
'''
run_spark_job
