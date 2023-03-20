# 📕 INT3402_20

Midterm project for Compiler course

## 📜Table of Contents

- [📕 INT3402_20](#📕-int3402_20)
  - [📜Table of Contents](#📜table-of-contents)
  - [💻 Lexical Scanner](#💻-lexical-scanner)
    - [💡 Introduction](#💡-introduction)
    - [🔧 Prerequisites](#🔧-prerequisites)
    - [💾 Data Files](#💾-data-files)
    - [⚙️ Config file](#⚙️-config-file)
    - [⏯ Run](#⏯-run)

## 💻 Lexical Scanner

### 💡 Introduction

This is a lexical analyzer for a subset of C language (VC) implemented using Python 3. The lexical analyzer is able to recognize tokens, comments and throw errors for invalid tokens. The language definition is defined in [VC Language Definition](https://drive.google.com/file/d/181xaizB7Ki5dnOb7vYxOKgWwmQWvev7g/view).

### 🔧 Prerequisites

-   [Python 3.9](https://www.python.org/downloads/) (you can also try other versions).
-   [Hydra](https://www.hydra.cc) to read config files
-   A `.dat` file containing information about the Deterministic finite automata (DFA) used in the lexical analyzer, the format of the file is defined in [💾 Data File](#💾-data-files).
-   A source code file written in VC language (`.vc` file).

### 💾 Data Files

-   The data file is in json format but the extension is _.dat_, there's a [sample data](dfa.dat) file in the root directory of this project. The data file contains the following fields:
    -   `keywords`: a list of keywords in target the language.
    -   `special_literals`: a list of special literals used in target the language.
    -   `separators`: a list of characters used to separate tokens in target the language.
    -   `terminal_types`: a list of types of tokens in target the language.
    -   `nodes`: a list of nodes in the DFA, this includes:
        -   the key of each node is the name of the node.
        -   `children` is a list of children of the node, each child is a map from a list of characters to the name of the child node
        -   if the node is the starting node, it will include a field `start` with value _true_.
        -   if the node is terminal, it will include a field `terminal` with value _true_ and a field `terminal_type` with the type of the token from `terminal_types`, else it will have a field `terminal` with value _false_.

### ⚙️ Config File
The config files is in `yaml` format. They're read by Hydra framwork. There are 3 variables:
- `file_name` (string): .vc file to scan through (default: _data/example_fib.vc_)
- `data_file` (string): .dat file which stores DFA's states (defailt: _dfa.dat_)
- `no_comments` (boolean): whether to output comments or not (default: _True_)  

### ⏯ Run

To run the lexical scanner, run the following command in the terminal:

```
python src/lexical.py
```

To override .vc file for scanning, do:
```
python src/lexical.py file_name=<source_code_file>
```
For example:
```
python src/lexical.py file_name=data/example_gcd.vc
```
If prefered, comments can be put to ouput:
```
python src/lexical.py no_comments=False
```
To see more information about the command, run the following command in the terminal:

```
python src/lexical.py -h
```
