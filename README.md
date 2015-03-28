# randomizelabel.py

### Purpose

The purpose of this script is to:

1. randomize a list of participants into treatment and control groups
2. create a label for each participant that can be affixed to his or her experimental materials
3. create a master table that links each participant to his or her assignment 

### Rationale

This script was initially designed for use with a randomized control trial (RCT) among students based in classrooms. Students were to be randomized into experimental condition within classrooms. The randomization scheme required the flexibility to block randomization by student characteristics. The script may be extended, however, to any RCT in which participants are known ahead of time, who may be nested within groups, and who have observable and known characteristics upon which further stratification is required.

This script assumes that treatment and control group members will receive different written materials but are unaware of the difference, that is, the materials themselves will not indicate experimental condition. It's important, therefore, that each participant gets the correct materials, especially if participants take part in the experiment concurrently (e.g., all students within a class tested at the same time). As part of its randomzation routine, this script automatically creates labels that can be affixed to the proper materials ahead of time.

### Supplementary file requirements
  
1. [Requires this code](https://pyfpdf.googlecode.com/hg-history/png_alpha/pdflabels.py) in the same directory saved as `pdflabels.py`. If not found, the script automatically downloads and saves the file.
2. Requires a `*.csv` file with participant names and any information required if sampling should be blocked within groups (e.g., classroom id, student geneder, student race or ethnicity)

## To Use

### Initialize

In terminal (works on OS X...not tested in other systems):

```
cd ./randomizelabel
python randomizelabel.py
```

### Locate `*.csv` file

You will be prompted for the location of the `*.csv` file. The script will first search the local directory for all `*.csv` files and list them:

```
( 1 ) fakeclasslist.csv
( 2 ) File not in this directory

Which CSV file contains the names of those to be randomized?
```
If you place the names file in the same directory, you can just choose it from here. If you don't, you should select the number for `File not in this directory`. You will then be prompted with:

```
Please give full path to CSV file:
```

You should give the full path (no `~`); for example:

```
/Users/<username>/randomizelabel/fakeclasslist.csv
```

### Choose primary unit of randomization

```
( 1 ) id
( 2 ) name
( 3 ) racecat
( 4 ) classid

Which column contains the randomization unit?
```

### Decide if you want to randomize within groups
```
Are you randomizing with groups (choose a number)?
        
(1) Yes     
(2) No
```
If you choose `yes` then:

```
( 1 ) id
( 2 ) name
( 3 ) racecat
( 4 ) classid

Which column contains the groups?
```
*NB: You cannot group on the primary randomization unit.*

### Decide if you want to stratify the randomization
*NB: If you don't choose to randomize within groups, you won't be given the option to stratify. If you want to stratify across, for example, race/ethnicity or gender, but not within classrooms, then you should just chose to GROUP on that category*

```
Should randomization be stratified (choose a number)?
            
(1) Yes          
(2) No
```
If you choose `yes` then:
```
( 1 ) id
( 2 ) name
( 3 ) racecat
( 4 ) classid

Which column contains the stratification category?
NOTE: Stratification category must be integer.
```
*NB: To prevent the potential for over-stratification based on different spellings or naming conventions (e.g., `female` vs `Female` vs `F` within the same column), the stratification category needs to be an integer. This may require preformatting of your input participant roster.*

### Decide the number of treatment groups

The default is to only have a control group. It is likely that you will want more. Choosing `1` means you want to have one treatment and one control group.

```
How many treatment conditions, excluding control?
        
Please enter an integer (choosing 0 means only control group)
```
### Choose the type of labels
```
( 1 ) Apli-01277
( 2 ) Avery-L7163
( 3 ) Avery-3422
( 4 ) Avery-5160
( 5 ) Avery-5161
( 6 ) Avery-5162
( 7 ) Avery-5163
( 8 ) Avery-5164
( 9 ) Avery-8600

Which labels will you use?
```
### Choose what you want on the labels
```
( 1 ) id
( 2 ) name
( 3 ) racecat
( 4 ) classid
( 5 ) assign

What do you want on the printed labels 
(select desired columns by number, separated by commas)?
```
The order matters. For example, `2,1,4`, would give:
```
name
id
classid
```
## Output

Two primary files are placed in the working directory:

1. `assignment.csv`
2. `assignmentlabels_*.pdf` sheets with the labels

#### `assignment.csv`

Is a long file that contains, the randomization column and the treatment condition. Example:

id      | assign  
:-----: | :------:
q4NSkKLNNags | C  
NRIL0Ewhq8A5	| T
UXCFYfIM6JGn	| T
MMNjGO4CtvlL	| T
5Pe8c9rHidi8	| C

For merging purposes, it's probably a good idea to randomize using a uniquely identifiable variable.

#### `assignmentlabels_*.csv`

There will be one `*.pdf` for the labels for each experimental group. If you only have one treatment and one control, the you will have two files:

```
assignmentlabels_T.csv
assignmentlabels_C.csv
```
If you have, for example, two treatment groups and one control, you will have:
```
assignmentlabels_T1.csv
assignmentlabels_T2.csv
assignemntlabels_C.csv
```
The labels themselves **will not** indicate experimental group status (for obvious reasons) so this printing scheme will mitigate mix ups. The number of pages for each group will depend on the types of labels choosen.

## Acknowledgements
* Originators and contributors to [PyFPDF](https://code.google.com/p/pyfpdf/)
* [List of random names](http://listofrandomnames.com/) and [Mark Heckmann at ryouready](https://ryouready.wordpress.com/2008/12/18/generate-random-string-name/) for helping me generate my fake class data
