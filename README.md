# randomizelabel.py

### Purpose

The purpose of this script is to:

1. randomize a list of participants into treatment and control groups;  
2. create labels for each group;
3. create a master table that lists participant assignments.  

To do this, this file requires the following:  

1. a csv file with participant names and any information required if sampling should be blocked within groups

This script assumes that treatment and control group members are receiving different written materials, but are unaware of that fact. Therefore, it is important that each participant gets the correct materials. Voila! Automatic labels that can be affixed to envelopes containing the proper materials!

### Supplementary file requirements
  
1. [Requires this code](https://pyfpdf.googlecode.com/hg-history/png_alpha/pdflabels.py) in the same directory saved as `pdflabels.py`. If not found, the script automatically downloads and saves the file.
2. Requires a `*.csv` file with the list of persons you wish to randomize to various treatments.

## To Use

### Initialize

In terminal (works on OS X...not tested in other systems):

```
cd ./randomizelabel
python randomizelabel.py
```

### Locate `*.csv` file

You will be prompted for the location of the `*.csv` file:

```
Which CSV file contains the names of those to be randomized?

(please give the full path name)
```

You should give the full path (no `~`); for example:

```
/Users/<username>/randomizelabel/classlist.csv
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

### Decide if you want to stratify the randomization
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
```
*NB: If you don't choose to randomize within groups, you won't be given the option to stratify. If you want to stratify across, for example, race/ethnicity or gender, but not within classrooms, then you should just chose to GROUP on that category*

### Decide the number of treatment groups

The default is to only have a control group. Clearly, you probably want more. Choosing `1` means you want to have one treatment and one control group.

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
2. `addresslabels_*.pdf` sheets with the labels

#### `assignment.csv`

Is a long file that contains, the randomization column and the treatment condition. Example:

id      | assign  
:-----: | :------:
q4NSkKLNNags | C  
NRIL0Ewhq8A5	| TUXCFYfIM6JGn	| TMMNjGO4CtvlL	| T5Pe8c9rHidi8	| C

For merging purposes, it's probably a good idea to randomize using a uniquely identifiable variable.

#### `addresslabels_*.csv`

There will be one `*.pdf` for the labels for each experimental group. If you only have one treatment and one control, the you will have two files:

```
addresslabels_T.csv
addresslabels_C.csv
```
If you have, for example, two treatment groups and one control, you will have:
```
addresslabels_T1.csv
addresslabels_T2.csv
addresslabels_C.csv
```
The labels themselves **will not** indicate experimental group status (for obvious reasons) so this printing scheme will mitigate mix ups. The number of pages for each group will depend on the types of labels choosen.
