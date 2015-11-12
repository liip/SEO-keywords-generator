# Keywords generator
## Introduction

The keyword generator provide multiple commands in order to create keyphrases for SEO monitoring tools such as AWRCloud, the tool currently used at Liip for internal SEO.

Commands:
| compare-awr  | Compare generated keywords with AWR Cloud keyword export                                   |   |   |   |
|--------------|--------------------------------------------------------------------------------------------|---|---|---|
| download-awr | Download keyphrases from AWR cloud into a file *AWR Cloud keyword export*                  |   |   |   |
| generate     | Generate keywords from an input directory and save it into a file *generated keyword file* |   |   |   |
| upload-awr   | Upload keyphrases and groups to AWR Cloud using *generated keyword file*                   |   |   |   |

run
```shell
kwgen [COMMAND] --help
```
to know options for each commands

## Installation

```shell
sudo python setup.py install
```

## More information about the *generate* command
**Given:**

1 - a list of *patterns* composed by *keyword_placeholders* separated by spaces such as:
- service location
- service theme

2 - a list of langages to output:
- fr
- en

3 - a list of *localized_possibilities* for each *keyword_placeholders* such as:

service:
- development, en
- développement, fr

location:
- Geneva, en
- Genève, fr
- Genf, de

theme:
- Drupal, en-fr
- AEM, en-fr-de

**The script will output:**

- development Geneva
- development Drupal
- development AEM
- développement Genève
- développement Drupal
- développement AEM

### Input directory structure
This directory must contain the following structure:
```
ROOT_DIR
|
+-- patterns.csv
+-- languages.csv
+-- keyword_placeholders
    +-- [keyword_file_1].csv
    +-- ...
```

#### Input files description
##### patterns.csv
Contains a list of patterns composed by *keyword_placeholders* separated by spaces

exemple:
```
service location
theme service
```

##### langage.csv
Contains the list of languages to output
exemple:
```
fr
de
en
```


##### keyword_files.csv
for each *keyword_placeholders* KP defined in **patterns.csv**, there must exist a file named "KP.csv". This file contains the list of *localized_possibilities* that the corresponding placeholder will take during the generation. The localized possibilities are the languages separated by '-'

exemple:
file "theme.csv"
```
web,en-fr-de
web,en-fr-de
expéricence utilisateur,fr
```