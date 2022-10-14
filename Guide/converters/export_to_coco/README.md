# Credits

Author: Raphael Jafri

# Overview

This script will convert all annotation types for images into the COCO format. 

For polylines
- Technially, COCO does not directly support polylines - instead, COCO supports "keypoints" and in the "categories" section, theres a key called "skeleton" which tells COCO how the keypoints connect. We leverage this structure to work polylines into the COCO format.

For polygons
- Technically, COCO does not directly support polygons, however COCO does support segmentation masks. So for polygons, we will treat them as segmentation masks. 

Key Assumptions of the Converter:

    Info Section
        - description = project name
        - url = project URL
        - version = always just "1.0"
        - year = time of export
        - contributor = email of whoever created the Labelbox project
        - date_created = time of export
    Licenses Section
        - url = N/A
        - id = always just "1"
        - name = N/A
    Images Section
        - file_name = data row external ID
        - date_captured = data row created at value
        - id = data row ID
    Annotations Section - covers all object annotations
        - image_id = data row ID
        - category_id = defaults to the tool's schemaId encoded value, but checks for nested classes and if any radio / checklist answers exist, pulls the first one
        - id = annotation feature ID
        ** All `iscrowd` values are 0 for segmentation masks / polygons
    Categories Section
        - All tools and 1st-layer nested classes will populate in the categories section
        - Polylines and Points fall into the COCO "keypoints" schema:
            - For polylines, the `max_keypoints` value is found by iterating over all annotations and grabbing the global maximum
            - For points, the `skeleton` is [0, 0] and `max_keypoints` is 0
        - Segementation masks and polygons fall into the segmentation COCO schema
        - Bounding boxes fall into the bounding box COCO schema


# How to Use It

- In terminal, run `python3 path/export_to_coco.py -api_key "" -project_id "" -save_to ""`

- The script will save the resulting dataset in the same directory as this .py file with the name `projectID_coco_dataset.json`

# Usage

This script was given to CBP as part of our agreement is to deliver the export in their desired format. 
