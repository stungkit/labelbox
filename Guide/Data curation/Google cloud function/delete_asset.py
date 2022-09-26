import labelbox
from labelbox import Client
from labelbox.schema.data_row import DataRow

# Add your API key below
LABELBOX_API_KEY = ""
client = Client(api_key=LABELBOX_API_KEY)


def delete_asset(event, context):
    """Deletes the asset from Catalog when the asset is deleted from GCP bucket using global key.
    Args:
          event (dict): Event payload.
          context (google.cloud.functions.Context): Metadata for the event.
    """
    file = event

    # Sets the file's name as global key
    global_key = file["name"]
    res = client.get_data_row_ids_for_global_keys(global_key)

    if res["status"] == "SUCCESS":
        delete_datarow_id = res["results"][0]
        data_row = client._get_single(DataRow, delete_datarow_id)
        data_row.delete()
    else:
        print("Global key does not exist")
