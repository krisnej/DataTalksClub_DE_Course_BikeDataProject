terraform {
  required_version = ">= 1.0"
  backend "local" {}  # Can change from "local" to "gcs" (for google) or "s3" (for aws), if you would like to preserve your tf-state online
  required_providers {
    google = {
      source  = "hashicorp/google"
    }
  }
}

provider "google" {
  project = var.project
  region = var.region
}


# DWH: BigQuery
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset
resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.BQ_DATASET
  project    = var.project
  location   = var.region
}

# Airflow: Google Cloud Composer
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/composer_environment
resource "google_composer_environment" "cloud_composer" {
  name   = "dtc-de-project"
  region = "europe-west6"
  config {
    software_config {
      image_version = "composer-2.0.1-airflow-2.1.4"
    }
  }
}
