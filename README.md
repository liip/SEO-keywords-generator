# Keywords generator
## Introduction

The keyword generator provide multiple commands in order to create keyphrases for SEO monitoring tools such as AWRCloud, the tool currently used at Liip for internal SEO.

Commands:

| Command      | Description                                                                                |
|--------------|--------------------------------------------------------------------------------------------|
| compare-awr  | Compare generated keywords with AWR Cloud keyword export                                   |
| download-awr | Download keyphrases from AWR cloud into a file *AWR Cloud keyword export*                  |
| generate     | Generate keywords from an input directory and save it into a file *generated keyword file* |
| upload-awr   | Upload keyphrases and groups to AWR Cloud using *generated keyword file*                   | 

## Command synthax
run
```shell
kwgen
```
to get general help on the keyword generator

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

It is possible to give a name to patterns, so additional groups will be associated to corresponding patterns. Multiple names can be associated to a pattern. If so, they must be separated with "|"

```
service location
theme service,name 1
theme service location,name 2|other
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

### Keyword groups associated during keyword upload
When uploading keyphrases to AWRCloud, keyword groups will automatically associated to uploaded keywords.

The using the command

```
kwgen upload-awr
```
The following patterns will be created:

- for each language of the associated with the keyword, a group 'lang_[LANGUAGE]' will be associated
- for each name of the pattern, a group 'pattern_[LANGUAGE]' will be associated
- a group corresponding to the topics associated with the pattern will be associated. If the topics composing the pattern are : "service", "location", the groupe associated will be : "pattern_service-location"

### Configuration

It's possible to store your username and password in the file [HOME_DIRECTORY]/.kwgen/config.ini using the following structure:

```
[authentication]
username = xxx
password = yyy
```