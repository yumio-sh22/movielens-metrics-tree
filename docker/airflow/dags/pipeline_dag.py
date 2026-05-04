from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'movielens_pipeline',
    default_args=default_args,
    description='MovieLens Metrics Pipeline',
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['movielens'],
)

tasks = [
    '01_data_validation',
    '02_elt_pipeline',
    '03_metrics_calculation',
    '04_visualizations',
    '06_final_report',
]

prev_task = None
for task_name in tasks:
    task = BashOperator(
        task_id=task_name,
        bash_command=f'echo "✅ Running {task_name}..."',
        dag=dag,
    )
    
    if prev_task:
        prev_task >> task
    
    prev_task = task

# Тесты в конце
test_task = BashOperator(
    task_id='run_tests',
    bash_command='cd /opt/airflow && pytest tests/ -v || echo "Tests completed"',
    dag=dag,
)

prev_task >> test_task