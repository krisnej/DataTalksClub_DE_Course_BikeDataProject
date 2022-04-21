import os
from datetime import datetime

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
DATA_BUCKET = os.environ["GCS_BUCKET"] + "/data"

default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 1,
}


def download_data_to_gcs(
    dag,
    dataset,
    download_url,
    csv_file,
):
    """
    task definition:
    download the csv file to Google Cloud Storage (data folder inside Composer bucket)
     using a bash curl command
    """
    with dag:
        download_dataset_task = BashOperator(
            task_id=f"download_{dataset}_task",
            bash_command=f"curl -sSLf {download_url} > /home/airflow/gcs/data/{csv_file}"
        )

        download_dataset_task


"""
Download bike theft data every day:
New data is added every day to the existing file, 
so we need to overwrite the file we have
"""
BIKE_URL = 'https://www.internetwache-polizei-berlin.de/vdb/Fahrraddiebstahl.csv'
BIKE_CSV_FILE = 'berlin_bike_data.csv'

bike_data_dag = DAG(
    dag_id="bike_data_dag",
    schedule_interval="0 6 * * *",
    start_date=datetime(2022, 3, 1),
    default_args=default_args,
    catchup=False,
    max_active_runs=3,
    tags=['dtc-de-project'],
)

download_data_to_gcs(
    dag=bike_data_dag,
    dataset='bike',
    download_url=BIKE_URL,
    csv_file=BIKE_CSV_FILE,
)


"""
Download the information on LOR (Lebensweltlich orientierte Räume):
LOR: a geographic basis for planning, forecasting and monitoring demographic 
and social developments in Berlin
CSV includes some empty or unnecessary columns, which we will filter out later 
"""
LOR_URL = 'https://tsb-opendata.s3.eu-central-1.amazonaws.com/lor_prognoseraeume_2021/lor_prognoseraeume_2021.csv'
LOR_CSV_FILE = '/berlin_lor_data.csv'

lor_data_dag = DAG(
    dag_id="lor_data_dag",
    schedule_interval="0 6 * * *",
    start_date=datetime(2022, 3, 1),
    default_args=default_args,
    catchup=False,
    max_active_runs=3,
    tags=['dtc-de-project'],
)

download_data_to_gcs(
    dag=lor_data_dag,
    dataset='lor',
    download_url=LOR_URL,
    csv_file=LOR_CSV_FILE,
)


"""
Download the information on Berlin districts:
Needed to assign LORs to districts
CSV includes some empty or unnecessary columns, which we will filter out later 
"""
DISTRICTS_URL = 'https://tsb-opendata.s3.eu-central-1.amazonaws.com/bezirksgrenzen/bezirksgrenzen.csv'
DISTRICTS_CSV_FILE = '/berlin_districts_data.csv'

districs_data_dag = DAG(
    dag_id="districs_data_dag",
    schedule_interval="@once",
    start_date=datetime(2022, 3, 1),
    default_args=default_args,
    catchup=False,
    max_active_runs=3,
    tags=['dtc-de-project'],
)

download_data_to_gcs(
    dag=districs_data_dag,
    dataset='districts',
    download_url=DISTRICTS_URL,
    csv_file=DISTRICTS_CSV_FILE,
)
