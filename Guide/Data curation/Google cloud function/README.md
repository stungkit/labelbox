# Credits

Author: Rahul Sharma

# Purpose
You can sync your cloud storage with Catalog by using two cloud functions: upload_asset.py, triggered upon uploading a new asset to the bucket, and delete_asset.py, triggered when an asset has been deleted from the bucket.

# Use
upload_asset.py is responsible for uploading asset to Catalog

delete_asset.py is responsible for deleting asset from Catalog

# How to run
1. Create new cloud functions 
2. One for uploading assets upon creating an asset and the trigger name is "On (finalizing/creating) file in the selected bucket"
3. One for deleting assets upon an asset has been deleted from bucket and the trigger name is "On (deleting) file in the selected bucket"
4. Add library dependecy to requirements.txt (both scripts have same requirements and add Labelbox API key to your main scripts)
5. Selete Python 3.7, paste the code and deploy
6. Upload and delete a file from cloud storage

# Loom
Upload asset: https://www.loom.com/share/85eb5f6da86c4e2f94050b4b98c7cfb5

Delete asset: https://www.loom.com/share/1b0bc26eeba54325893e86621da67c36
