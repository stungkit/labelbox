# Custom Editor SDK
If you find that the Labelbox Editor does not have the functionality you need, you can build your own custom labeling interface. Explore some of our open-source custom editors [here](https://github.com/Labelbox/Labelbox/tree/master/custom-interfaces). We also offer a JavaScript SDK you can use to programmatically fetch assets and submit labels.

With a custom editor, you can label:
* point clouds
* medical DICOM imagery
* multiple assets at once

Not supported:
* Ontologies (label tooling)
* Benchmarks and consensus
* Model-assisted labeling
* Project analytics
* Issues and comments
* Model diagnostics
* Data catalog

Note:
* Interface customizations must be self-developed, hosted, and maintained
* Limited support for existing framework


To set up a simple custom labeling interface, follow these steps:

## Step 1: Run a localhost server
1. Set up your custom interface locally. You can use this [Hello world script](https://github.com/Labelbox/labelbox/blob/master/custom-interfaces/hello-world/index.html) as an example.
1. Start the localhost server in a directory containing your custom interface frontend files. For example, run the server inside `custom-interfaces/hello-world` to run the Hello world custom interface locally.
`python -m http.server`
1. Open your browser and navigate to the `<localhost> endpoint provided by the server.
1. Customize the labeling frontend by making changes to `index.html`.
1. Restart the server and refresh the browser to see the updates.

## Step 2: Install your custom editor in Labelbox
Upload your index.html file to a cloud service that exposes a URL for Labelbox to fetch the file. Then, install your custom editor in Labelbox by pointing to the hosted version of it. If you don’t have a hosting service on-hand, follow these steps to launch your custom editor with [Vercel](https://vercel.com/home).

1. Create an account at [Vercel](https://vercel.com/home).
1. Download and install [vercel](https://vercel.com/cli).
1. With Vercel installed, navigate to the directory with your custom editor (where your `index.html` is located) and launch Vercel in your terminal by typing `vercel`. The Vercel service will provide a link to your hosted labeling interface file. See [Vercel docs](https://vercel.com/docs/cli#commands/dev) for more information.
1. Within the labeling interface menu of the **Settings** tab of your Labelbox project, choose **Custom** and paste the link in the **URL to the labeling frontend** field.

## Step 3: Create the import file
Include the following information when you import your data for labeling.

Parameter | Description
--------- | -----------
`instructions` | Text that will appear when the labeler opens the asset(s) in the labeling interface.
`referenceImage` | Can be used to upload a larger reference image to help labelers.
`externalId` | User-generated identifier used to index the asset in user’s system.
`imageUrl` | HTTPS path to an external image file.

Below is a sample JSON import file.

```JSON
[
    {
        "instructions": "<p>Which cars do you like the most?</p>",
        "referenceImage":"https://storage.googleapis.com/labelbox-example-datasets/tesla/104836109-p100d-review-5.1910x1000.jpeg",
        "externalId":"abadsf99w11",
        "data": [
            {
                "externalId": "ab65d5e99w12",
                "imageUrl": "https://storage.googleapis.com/labelbox-example-datasets/tesla/104836109-p100d-review-5.1910x1000.jpeg"
            },
            {
                "externalId": "abadsf99w13",
                "imageUrl": "https://storage.googleapis.com/labelbox-example-datasets/tesla/104836109-p100d-review-5.1910x1000.jpeg"
            }
        ]
    }
]
```

## Sample script
Use this script to create a minimal custom interface that fetches and submits labels programmatically.

```javascript
// Attach the Labelbox client-side API
<script src="https://api.labelbox.com/static/labeling-api.js"></script>
<div id="form"></div>

<script>

// Fetch an asset to label then submit the label
function label(label){
    Labelbox.setLabelForAsset(label, "Any").then(() => {
        Labelbox.fetchNextAssetToLabel();
    });
}

// Draw the next asset
Labelbox.currentAsset().subscribe((asset) => {
    if (asset){
        drawItem(asset.data);
    }}
)

//Display the labeling interface
function drawItem(dataToLabel){
    const labelForm = `
        <img src="${dataToLabel}" style="width: 300px;"></img>
        <div style="display: flex;">
            <button onclick="label('bad')">Bad Quality</button>      
            <button onclick="label('good')">Good Quality</button>    
        </div>
    `;
    document.querySelector('#form').innerHTML = labelForm;
}

</script>
```

## Reference
If you would like to create your own labeling interface instead of using our out-of-the-box Editor, you can use the following functions. Below is a list of asset fields.

Parameter | Description
--------- | -----------
`asset.id` | Labelbox ID for this asset.
`asset.data` | Data imported into Labelbox (e.g. image URL)
`asset.label` | Submitted label. Will be undefined if the asset has not been labeled yet.
`asset.next` | Next assetId in the labeling queue.
`asset.previous` | Previous assetId in the labeling queue.
`asset.createdAt` | Datetime for when this asset was created.
`asset.createdBy` | Email of the user that labeled that asset.
`asset.TypeName` | Label schema. Can be either Any or Skip.

### Get current asset
Use `Labelbox.currentAsset` to get information about the asset in the Editor. Make sure to have all your drawing logic behind this function so that Labelbox can tell your frontend which asset to render.

For example, if a user opens your interface from an existing label, this function would receive the data about that asset but also its label information.

When you append information such as `asset.next` or `asset.previous` onto the asset, `Labelbox.currentAsset().subscribe(...)` will emit multiple times for the same asset because multiple network requests are appending information onto the asset.

```javascript
const subscription = Labelbox.currentAsset().subscribe((asset) => {
  // Asset can be undefined
  if (!asset){
    return;
  }

  console.log(asset.id);
  console.log(asset.data);  console.log(asset.label);
  console.log(asset.previous);
  console.log(asset.next);
  console.log(asset.createdAt);
  console.log(asset.createdBy);
  console.log(asset.typeName);
})

// Stop receiving updates
subscription.unsubscribe();
```

### Fetch next asset
This function will set the `currentAsset` to be the next unlabeled asset. For example, after submitting a label if you want to advance to the next unlabeled asset you can run `Labelbox.fetchNextAsset`. `Labelbox.currentAsset` will emit the new asset as soon as it is fetched.

```javascript
function label(label){
  Labelbox.setLabelForAsset(label, "Any").then(() => {
    Labelbox.fetchNextAssetToLabel();
  });
}
```

### Back to previous asset
Labelbox will automatically emit `currentAssets` when a user performs some action, such as jumping through the review screen. However, you can use `Labelbox.setLabelAsCurrentAsset` to add a button to go back to a previous asset.

```javascript
function goBack(){
  Labelbox.setLabelAsCurrentAsset(asset.previous)
}
```

### Save label
The `Labelbox.setLabelForAsset` function takes a string (`JSON.stringify(myJsonLabel`) and will return a promise for when the label has been saved.

```javascript
Labelbox.setLabelForAsset('good').then(() => console.log('Success!'));
```

### Skip asset
`Labelbox.skip` is identical to `setLabelForAsset(‘Skip’, ‘Skip’)`. The Label that will be seen in your export will be set to Skip.
Updating a label prevously `Skip` should reflect in the export.


```javascript
Labelbox.skip().then(() => console.log('Skipped!'))
```

### Enable preloading
Labelbox automatically preloads a labeling queue. However, you can improve the loading speed of labels by running `Labelbox.enablePreloading` on each preloaded asset. This preloading function must return a promise.

The sample script below preloads images in the DOM before the user sees the asset. It is cached by the time the user reaches that asset.

```javascript
const preloadFunction = (asset: Asset) => {
  const loadImageInDom = (url: string) => {
    return new Promise((resolve) => {
      const img = document.createElement('img');
      img.src = url;
      img.onload = () => {
        img.remove();
        resolve();
      };
      img.style.display = 'none',
      img.style.width = '0px',
      img.style.height = '0px',
      document.body.appendChild(img);
    });
  }
  return loadImageInDom(asset.data);
}

Labelbox.enablePreloading({preloadFunction})
```

### Get ontology
Use `Labelbox.getTemplateCustomization` to get the ontology JSON. Ontology always comes in as JSON, but may not be supported by your template. Make sure to add some error handling here.

```JSON
// Ontology looks like this
{
  "instructions":"Label This",
  "tools": [{"name": "Tool one"}]
}
```

```javascript
// Get ontology

Labelbox.getTemplateCustomization().subscribe((customization) => {
  if (customization.instructions && customization.tools) {
     updateTemplateWithCustomization(customization);
  }
})
```

### Use predictions
Use `Labelbox.currentAsset` to get the predictions information about the asset in the Editor.

Parameter | Description
--------- | -----------
`asset.labelTemplates` | Provides an array of all available predictions for the current asset. Each entry has an id attribute that can be matched against asset.labelTemplateId to determine the correct prediction to show.
`asset.labelTemplateId` | ID of the prediction that was created by the project's currently active prediction model.
`asset.label` | Contains the data the custom editor should use as a starting point for initializing the label. The exact schema of this data is dependent upon the labeling interface in use. For a custom interface, you will need to ensure that the format of the labels submitted when creating predictions conform to the schema expected by the custom labeling interface.

```javascript
const subscription = Labelbox.currentAsset().subscribe((asset) => {
  // Asset can be undefined
  if (!asset){
    return;
  }

  console.log(asset.labelTemplates); // A (nullable) array of the Predictions for this asset, if any exist
  console.log(asset.labelTemplateId); // A (nullable) string id of the Prediction created by the project's active prediction model, if it exists
    const labelTemplate = (asset.labelTemplates || []).find(
      (template) => template.id === asset.labelTemplateId
    ); // Gets the Prediction created by the Project's active prediction model
    console.log(labelTemplate.label); // The data to use for initializing the label
})

// If you want to stop recieving updates.
// However, I would recommend having a single subscription for your entire application.
subscription.unsubscribe();
```
