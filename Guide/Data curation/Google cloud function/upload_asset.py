import labelbox
from labelbox import Client, Dataset

# Add your API key below
LABELBOX_API_KEY = ""
client = Client(api_key=LABELBOX_API_KEY)


def upload_asset(event, context):
    """Uploads an asset to Catalog when a new asset is uploaded to GCP bucket. 
       If a bucket with object_name exists, then an asset is added to that dataset. Otherwise, a new dataset is created.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    file = event
    bucket_name = file['bucket']
    object_name = file["name"]
    datasets = client.get_datasets(where=Dataset.name == bucket_name)
    dataset = next(datasets, None)
    if not dataset:
      dataset = client.create_dataset(name=bucket_name, iam_integration='DEFAULT')
    url = f"gs://{bucket_name}/{object_name}"
    dataset.create_data_row(row_data=url, global_key=object_name)
