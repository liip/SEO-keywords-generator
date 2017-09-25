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

A project directory with the following structure:

```
ROOT_DIR
|
+-- patterns.csv
+-- keyword_placeholders
    +-- [placeholder_1].csv
    +-- ...
```

`patterns.csv` file which lists keyphrases *patterns*, which are composed by *keyword_placeholders* separated by spaces (or plus sign for compound words). Note how patterns are attributed to one or many language (the same will go for placeholder files):

```
pattern,languages,tag,example keyphrase
theme,fr|en|de,priority-1|words-1,'web'
theme organisation,en|de,priority-2|words-2,'web agentur'
theme+organisation,de,priority-2|words-2,'webagentur'
organisation theme,fr,priority-2|words-2,'agence web'
theme service,en|de, priority-3|words-2,'web development'
service theme,fr,priority-3|words-2,'développement web'
```

A `/keyword_placeholders/` folder of `[PLACEHOLDER].csv` files detailing the real keywords behind each placeholder (in the above defined patterns, there are three placeholders: `theme`, `organisation`, and `service`):

`/keyword_placeholders/theme.csv`:

```
keyword,languages
web,fr|en
internet,fr|en
```

`/keyword_placeholders/organisation.csv`:

```
keyword,languages
agentur,de
agency,en
agence,fr
```

`/keyword_placeholders/service.csv`:

```
keyword,languages
design,en|fr|de
développement,fr
development,en
entwicklung,de
```

**... the script will output all possible keyword combinations in the following `keywords.csv` file:**


```
keyphrase,lang,topics,tags
agence internet,fr,organisation|theme,priority-2|words-2
agence web,fr,organisation|theme,priority-2|words-2
design internet,fr,service|theme,priority-3|words-2
design web,fr,service|theme,priority-3|words-2
développement internet,fr,service|theme,priority-3|words-2
développement web,fr,service|theme,priority-3|words-2
internet,de|en|fr,theme,priority-1|words-1
internet agency,en,organisation|theme,priority-2|words-2
internet agentur,de,organisation|theme,priority-2|words-2
internet design,de|en,service|theme,priority-3|words-2
internet development,en,service|theme,priority-3|words-2
internet entwicklung,de,service|theme,priority-3|words-2
internetagentur,de,organisation|theme,priority-2|words-2
web,de|en|fr,theme,priority-1|words-1
web agency,en,organisation|theme,priority-2|words-2
web agentur,de,organisation|theme,priority-2|words-2
web design,de|en,service|theme,priority-3|words-2
web development,en,service|theme,priority-3|words-2
web entwicklung,de,service|theme,priority-3|words-2
webagentur,de,organisation|theme,priority-2|words-2
```

## Group management

### pattern groups


It is possible to attribute groups to patterns – in our above example, we assign the 'prio-1' and 'prio-2' groups to the patterns. Multiple groups can be associated to a pattern by separating them with "|".


### Keyword groups associated during keyword upload
When uploading keyphrases to AWRCloud, keyword groups will automatically be associated to uploaded keywords.

The using the command

```
kwgen upload-awr
```
The following groups will be created in AWRCloud:

- for each pattern underlying a keyphrase, a group 'pattern_[PATTERN-NAME]' will be assigned
- for each language associated with the keyphrase, a group 'lang_[LANGUAGE]' will be assigned
- a group corresponding to each placeholder associated with the pattern will be assigned. For example, if the pattern is "service location", the associated group will be : "pattern_service-location".

### Configuration

Store your username and password in the file [HOME_DIRECTORY]/.kwgen/config.ini using the following structure:

```
[authentication]
username = xxx
password = yyy
```