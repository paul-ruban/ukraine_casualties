## Data

This folder contains JSON files with the information extracted from the publicly available sources.

At the moment the data comes in the following formats (from most common to least):

* `jpg` or `jpeg` - images of typed or written text
* `gdoc` - Google Doc files
* `pdf`
* `xlsx` - Microsoft Spreadsheets
* `docx` - Microsoft Documents

### Data Entry Format

The main goal is to extract the peoples names and the source of the data. The following format is used for each entry:

```
{
    "name": <personal_info>,
    "source": <public_link_to_source>,
    "path": <path_within_the_source>
}
```
