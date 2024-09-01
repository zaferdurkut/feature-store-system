from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "job_average_product_review_last_30_days",
    default_args=default_args,
    description="Calculate average product review for the last 30 days and write to Redis",
    schedule_interval=timedelta(days=1),  # Runs daily
    catchup=False,
) as dag:

    # SparkSubmitOperator to run the PySpark job
    calculate_review = SparkSubmitOperator(
        dag=dag,
        task_id="job_average_product_review_last_30_days",
        application="/opt/spark-apps/job_average_product_review_last_30_days.py",  # Path to your PySpark script
        conn_id="spark_default",  # Connection ID for the Spark cluster
        executor_cores=2,
        executor_memory="2g",
        num_executors=2,
        driver_memory="2g",
        name="average_product_review_last_30_days",
        verbose=True,
        conf={
            "spark.master": "spark://spark:7077",  # Your Spark master URL
        },
    )

    # Setting the task sequence
    calculate_review
