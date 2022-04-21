### Setup

1. Have your gcp-service-accounts-credentials file stored as `google_credentials.json`
& in your $HOME directory
```
    cd ~ && mkdir -p ~/.google/credentials/
    mv <path/to/your/service-account-authkeys>.json ~/.google/credentials/google_credentials.json
```
2. You may need to upgrade your docker-compose version to v2.x+, 
and set the memory for your Docker Engine to minimum 5GB (ideally 8GB). 
If enough memory is not allocated, it might lead to airflow-webserver continuously 
restarting.

3. Set the Airflow user:

On Linux, the quick-start needs to know your host user-id and needs to have group id set to 0. 
Otherwise, the files created in dags, logs and plugins will be created with root user. 
You have to make sure to configure them for the docker-compose:
```
mkdir -p ./dags ./logs ./plugins
echo -e "AIRFLOW_UID=$(id -u)" > .env
```
### Execution

1. Build the image (only first-time, or when there's any change in the `Dockerfile`):
Takes ~15 mins for the first-time
```shell
docker-compose build
```

2. Initialize the Airflow scheduler, DB, and other config
```shell
docker-compose up airflow-init
```

3. Kick up the all the services from the container:
```shell
docker-compose up
```

4. Login to Airflow web UI on `localhost:8080` with default creds: `airflow/airflow`

5. Run your DAG on the Web Console.

6. On finishing your run or to shut down the container/s:
```shell
docker-compose down
```

### Alternative

Set up a Google Cloud Composer environment in GCP and upload the dag files to
the corresponding GCS bucket.
