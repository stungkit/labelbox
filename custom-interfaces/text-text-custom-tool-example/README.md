# Text Custom editor

Why would you use a Text custom editor? 
 - Custom editors are fully customisable and enabled you to build tools that are not available in Labelbox Text editor.
 
How to set it up?
 - Refer to our guide page (Step 1&2) : https://github.com/Labelbox/labelbox/tree/text-example-custom-tool/custom-interfaces
 
 - For quick testing you can store the HTML file to a cloud storage and use the URL as your `URL to label editor`
 Note : The URL needs to be signed and accessible to `labelbox.com/*`
 ![editor setup in Labelbox](https://github.com/Labelbox/labelbox/blob/text-example-custom-tool/custom-interfaces/text-text-custom-tool-example/custom_editor_set_up.jpg)
 
 This why having a single file is beneficial in the development stage
 
 - Be aware in order to simplify the structure of the custom tool, the HMTL template include the CSS and the Javascript files 
 
What tools are included in this template?
- A checklist classification.
- A free-text input.
- A number slider with input.
 
### Upload file format

|   Parameter   |  Description                                                                                      |
| ------------- | ------------------------------------------------------------------------------------------------- |
| `row_data`    | A text string                                                                                     |
| `global_key`  | Unique on a Catalog / Organization level, each global key will only map to exactly one data row   |
| `media_type`  | Hint what data asset type they are uploading (optional)                                           | 

Upload your raw text in Labelbox (ref : https://docs.labelbox.com/reference/text-file#import-format)

Example : 
```
[
  {
    "row_data": "👋 I am a raw text string with emojis  🙏 😃",
    "global_key": "483e64b0-c2fb-41bc-9f69-82c036f1ca5c",
    "media_type": "TEXT"
  },
  {
    "row_data": "Active learning is a method of learning in which students are actively or experientially involved in the learning process and where there are different levels of active learning, depending on student involvement.[1] Bonwell & Eison (1991) states that students participate [in active learning] when they are doing something besides passively listening. According to Hanson and Moser (2003) using active teaching techniques in the classroom create better academic outcomes for students. Scheyvens, Griffin, Jocoy, Liu, & Bradford (2008) further noted that “by utilizing learning strategies that can include small-group work, role-play and simulations, data collection and analysis, active learning is purported to increase student interest and motivation and to build students ‘critical thinking, problem-solving and social skills”. In a report from the Association for the Study of Higher Education (ASHE), authors discuss a variety of methodologies for promoting active learning. They cite literature that indicates students must do more than just listen in order to learn. They must read, write, discuss, and be engaged in solving problems. This process relates to the three learning domains referred to as knowledge, skills and attitudes (KSA). This taxonomy of learning behaviors can be thought of as the goals of the learning process.[2] In particular, students must engage in such higher-order thinking tasks as analysis, synthesis, and evaluation.[3]",
    "global_key": "6a12ff36-8a3e-4e7d-aff1-261840500c96",
    "media_type": "TEXT"
  }
]
```

### Ontology (present in the html template): 

```
{
    classifications: [
      {
        name: "Asset Classifications",
        instructions: "What is this?",
        type: "checklist",
        options: [
          {
            value: "Politics",
            label: "Politics",
          },
          {
            value: "Economy",
            label: "Economy",
          },
          {
            value: "Divers",
            label: "Else",
          },
        ],
      },
      {
        name: "description",
        instructions: "Describe this text",
        type: "text",
      },
      {
        name: "choose a number",
        instructions: "Choose a number",
        type: "number",
      },
    ],
  }
```
### Interface rendering

![editor interface](https://github.com/Labelbox/labelbox/blob/text-example-custom-tool/custom-interfaces/text-text-custom-tool-example/text_custom_editor_v1.jpg)

### Label format 
``` {"Text Classification":["Divers"],"description":"Covid related","choose a number":"63"} ```
