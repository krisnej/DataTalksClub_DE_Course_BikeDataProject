import os

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.contrib.operators.gcs_to_bq import GoogleCloudStorageToBigQueryOperator

DATA_BUCKET = os.environ["GCS_BUCKET"] + "/data"

BIKE_GCS_FILES = "berlin_bike_data.csv"
LOR_GCS_FILES = "berlin_lor_data.csv"
DISTRICTS_GCS_FILES = "berlin_districts_data.csv"
DATASET = 'berlin_bike_data'

default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    dag_id="bike_gcs_to_bq_dag",
    schedule_interval="0 6 30 * *",
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
    tags=['dtc-de'],
) as bike_dag:

    BIKE_GCS_to_BQ = GoogleCloudStorageToBigQueryOperator(
        task_id='bike_gcs_to_bq',
        bucket=DATA_BUCKET,
        source_objects=[BIKE_GCS_FILES],
        destination_project_dataset_table=f'{DATASET}.berlin_bike_data',
        schema_fields=[
            {'name': 'created_at', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'time_of_crime_start_day', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'time_of_crime_start_hour', 'type': 'INTEGER', 'mode': 'NULLABLE'},
            {'name': 'time_of_crime_end_day', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'time_of_crime_end_hour', 'type': 'INTEGER', 'mode': 'NULLABLE'},
            {'name': 'LOR', 'type': 'INTEGER', 'mode': 'NULLABLE'},
            {'name': 'amount_of_damage', 'type': 'FLOAT', 'mode': 'NULLABLE'},
            {'name': 'attempt', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'type_of_bike', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'offence', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'reason_of_data_capture', 'type': 'STRING', 'mode': 'NULLABLE'},
        ],
        skip_leading_rows=1,
        source_format='CSV',
        create_disposition='CREATE_IF_NEEDED',
        write_disposition='WRITE_TRUNCATE',
    )

    BIKE_GCS_to_BQ

with DAG(
    dag_id="lor_gcs_to_bq_dag",
    schedule_interval="0 6 30 * *",
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
    tags=['dtc-de'],
) as lor_dag:

    LOR_GCS_to_BQ = GoogleCloudStorageToBigQueryOperator(
        task_id='lor_gcs_to_bq',
        bucket=DATA_BUCKET,
        source_objects=[LOR_GCS_FILES],
        destination_project_dataset_table=f'{DATASET}.berlin_lor_data',
        schema_fields=[
            {'name': 'PLR_ID', 'type': 'INTEGER', 'mode': 'NULLABLE'},
            {'name': 'PLR_NAME', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'BEZ', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'STAND', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'GROESSE_M2', 'type': 'STRING', 'mode': 'NULLABLE'},
        ],
        skip_leading_rows=1,
        source_format='CSV',
        create_disposition='CREATE_IF_NEEDED',
        write_disposition='WRITE_TRUNCATE',
    )

    LOR_GCS_to_BQ

with DAG(
    dag_id="districts_gcs_to_bq_dag",
    schedule_interval="0 6 30 * *",
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
    tags=['dtc-de'],
) as districts_dag:

    DISTRICTS_GCS_to_BQ = GoogleCloudStorageToBigQueryOperator(
        task_id='districts_gcs_to_bq',
        bucket=DATA_BUCKET,
        source_objects=[DISTRICTS_GCS_FILES],
        destination_project_dataset_table=f'{DATASET}.berlin_districts_data',
        schema_fields=[
            {'name': 'gml_id', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'Gemeinde_name', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'Gemeinde_schluessel', 'type': 'INTEGER', 'mode': 'NULLABLE'},
            {'name': 'Land_name', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'Land_schluessel', 'type': 'INTEGER', 'mode': 'NULLABLE'},
            {'name': 'Schluessel_gesamt', 'type': 'STRING', 'mode': 'NULLABLE'},
        ],
        skip_leading_rows=1,
        source_format='CSV',
        create_disposition='CREATE_IF_NEEDED',
        write_disposition='WRITE_TRUNCATE',
    )

    DISTRICTS_GCS_to_BQ
