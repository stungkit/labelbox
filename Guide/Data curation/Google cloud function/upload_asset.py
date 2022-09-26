import labelbox
from labelbox import Client

# Add your API key below
LABELBOX_API_KEY = ""
client = Client(api_key=LABELBOX_API_KEY)


def upload_asset(event, context):
    """Uploads an asset to Catalog when a new asset is uploaded to GCP bucket.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    file = event
    bucket_name = file['bucket']
    object_name = file["name"]
    dataset = client.create_dataset(
        name=bucket_name, iam_integration='DEFAULT')
    url = f"gs://{bucket_name}/{object_name}"
    dataset.create_data_row(row_data=url, global_key=object_name)
