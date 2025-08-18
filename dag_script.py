from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from Extraction import run_extraction 
from Transformation import run_transformation
from Loading import run_loading


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 8, 17),
    'email': 'lindamicheal15@gmail.com',
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'zipco_foods_pipeline',
    default_args=default_args,
    description='ETL pipeline for Zipco Foods',
    schedule_interval=timedelta(days=1),
)

extraction = PythonOperator(
    task_id='extraction',
    python_callable=run_extraction,
    dag=DAG
)

transformation = PythonOperator(
    task_id='transformation',
    python_callable=run_transformation,
    dag=DAG
)

loading = PythonOperator(
    task_id='loading',
    python_callable=run_loading,
    dag=DAG
)

extraction >> transformation >> loading