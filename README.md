 # Keywords generator
## Introduction

The keyword generator provide multiple commands in order to generate and manage a set of keyphrases for SEO monitoring tools such as AWRCloud, the tool currently used at Liip for internal SEO. It takes an unusual yet powerful generative approach: given a list of *patterns* composed by *keyword_placeholders*, and given a list of keywords for each *keyword_placeholder*, the tool generates all keyphrases (= keyword combinations) corresponding to the patterns based on the keywords listed for each *keyword_placeholder*, accordingly to the languages associated with each keyword.

For a more basic keyword composition tool, see [MergeWords](http://mergewords.com/).

Commands:

| Command      | Description                                                                                |
|--------------|--------------------------------------------------------------------------------------------|
| generate     | Generate keywords from an input directory and save it into a file *generated keyword file* |
| download-awr | Download keyphrases from AWR cloud into a file *AWR Cloud keyword export*                  |
| compare-awr  | Compare generated keywords with AWR Cloud keyword export                                   |
| upload-awr   | Upload keyphrases and groups to AWR Cloud using *generated keyword file*                   |

## Command synthax
To get general help on the keyword generator:
```shell
kwgen
```

To know options for each commands:
```shell
kwgen [COMMAND] --help
```

## Installation

Download or clone the repository from github.

Then:

```shell
sudo python setup.py install
```

## More information about the *generate* command

A short example.

**Given ...**

1 - a `languages.csv` file listing all langages concerning that project:

```
lang
en
fr
```

2 - a `patterns.csv` file listing *patterns*, which are composed by *keyword_placeholders* separated by spaces:

```
pattern,group,example keyphrase
theme,prio-1,'e-commerce'
theme organisation,prio-2,'e-commerce agency'
theme service,prio-1,i'e-commerce development'
```

3 - a */keyword_placeholders/* folder of `[PLACEHOLDER].csv` files detailing the real keywords behind each placeholder (in the above defined patterns, there are three placeholders: `theme`, `organisation`, and `service`):

`theme.csv`:

```
keyword,lang
web,fr-en
internet,fr-en
```

`organisation.csv`:

```
keyword,lang
agency,en
agence,fr
```

`service.csv`:

```
keyword,lang
design,en-fr
développement,fr
development,en
```

**... the script will output a `keywords.csv` file:**



```
keyphrase,lang,topics,pattern name
web,en|fr,theme,prio-1
internet,en|fr,theme,prio-1
web agency,en,organisation|theme,prio-2
internet agency,en,organisation|theme,prio-2
web design,en|fr,service|theme,prio-1
web development,en,service|theme,prio-1
internet design,en|fr,service|theme,prio-1
internet development,en,service|theme,prio-1
web agence,fr,organisation|theme,prio-2
internet agence,fr,organisation|theme,prio-2
web développement,fr,service|theme,prio-1
internet développement,fr,service|theme,prio-1
```

### Input directory structure
This directory must contain the following structure:

```
ROOT_DIR
|
+-- patterns.csv
+-- languages.csv
+-- keyword_placeholders
    +-- [placeholder_1].csv
    +-- ...
```

#### Input files description
##### 
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

##### [placeholder].csv
for each *keyword_placeholders* `KP` defined in **patterns.csv**, there must exist a file named `KP.csv`. This file contains the list of *keywords* that the corresponding placeholder will take during the generation.

exemple:
file "theme.csv"
```
web,en-fr-de
web,en-fr-de
expéricence utilisateur,fr
```

### Keyword groups associated during keyword upload
When uploading keyphrases to AWRCloud, keyword groups will automatically be associated to uploaded keywords.

The using the command

```
kwgen upload-awr
```
The following groups will be created:

- for each pattern underlying a keyphrase, a group 'pattern_[PATTERN-NAME]' will be assigned
- for each language associated with the keyphrase, a group 'lang_[LANGUAGE]' will be assigned
- a group corresponding to each placeholder associated with the pattern will be assigned. For example, if the placeholders composing the pattern are : "service", "location", the groupe associated will be : "pattern_service-location".

### Configuration

It's possible to store your username and password in the file [HOME_DIRECTORY]/.kwgen/config.ini using the following structure:

```
[authentication]
username = xxx
password = yyy
```
