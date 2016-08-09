## Purpose

The purpose of this script is to:

1. randomize a list of participants into treatment and control groups
2. create a label for each participant that can be affixed to his or her experimental materials
3. create a master table that links each participant to his or her assignment 

## Rationale

The script may be used for any randomized control trial (RCT) in which participants are known ahead of time, who may be nested within groups, and who have observable and known characteristics upon which further stratification is required.

This script assumes that treatment and control group members will receive different materials but are unaware of the difference, that is, the materials themselves will not indicate experimental condition. It's important, therefore, that each participant gets the correct materials, especially if participants take part in the experiment concurrently. As part of its randomization routine, this script automatically creates labels that can be affixed to the proper materials ahead of time.

## Supplementary file requirements
  
1. [Requires this code](https://raw.githubusercontent.com/reingart/pyfpdf/master/tools/pdflabels.py) in the same directory saved as `pdflabels.py`. If not found, the script automatically downloads and saves the file.
2. Requires a `*.csv` file with participant names and any information required if sampling should be blocked within groups (e.g., classroom id, student gender, student race or ethnicity)

## To Use

### Initialize

In terminal (works on OS X...not tested in other systems), navigate to the script directory and type: 

```bash
./randomizelabel.py
```

or, if you want to set the Python interpreter manually:

```
python<3> randomizelabel.py
```

Note that this script requires Python 3.x.

## Choose task

```
-----------------------
What do you want to do?
-----------------------

( 1 ) Randomize and make labels
( 2 ) Generate labels from prior randomization

CHOICE: 
```
If you've already randomized a roster and simply want to reprint the labels, choose the second option (see instructions below).

## (1) Randomize and make labels

### Locate `*.csv` file

You will be prompted for the location of the `*.csv` file. The script will first search the local directory for all `*.csv` files and list them:

```
------------------------------------------------------------
Which CSV file contains the names of those to be randomized?
------------------------------------------------------------

( 1 ) fakeclasslist.csv
( 2 ) File not in this directory

CHOICE: 
```
If you place the names file in the same directory, you can just choose it from here. If you don't, you should select the number for `File not in this directory`. You will then be prompted with:

```
Please give path to CSV file:
```

You can give the full or relative paths. For example, each of the below should work:

```
/Users/<username>/randomizelabel/fakeclasslist.csv
~/randomizelabel/fakeclasslist.csv
./randomizelabel/fakeclasslist.csv
```

### Set seed
```
Give integer seed of at least 6 digits:
```
This seed is saved as `seed.txt` in the working directory. If you lose all assignment files, but have the roster and seed, you should be able to reproduce the same assignments.

### Choose primary unit of randomization

```
---------------------------------------------
Which column contains the randomization unit?
---------------------------------------------

( 1 ) classid
( 2 ) id
( 3 ) name
( 4 ) gender
( 5 ) racecat

CHOICE: 
```
*NB: Randomization unit column cannot contain duplicate values.*

### Decide if you want to block randomize
```
------------------------------------
Should random assignment be blocked?
------------------------------------

( 1 ) Yes
( 2 ) No

CHOICE: 
```
If you choose `yes` then:

```
----------------------------------------
On which column(s) do you wish to block?
----------------------------------------

( 1 ) classid
( 2 ) id
( 3 ) name
( 4 ) gender
( 5 ) racecat
```
You may choose more than one category. Separate multiple choices with a space.  

*NB: You cannot block on the primary randomization unit.*


### Check your options

To make that you get what you are expecting, the program will give you some descriptive information about your randomization choices. For example, if you chose to randomize on `id`, group on `classid`, and stratify across `gender` and `racecat`, you will see the following:

```
================================================================================

For the randomization unit: id

................................................................................

Number of unique values = 400

================================================================================


================================================================================

For the grouping category: classid

................................................................................

Number of unique values = 17
Unique values: 

ENGL101.01
ENGL101.02
ENGL101.03
ENGL101.04
ENGL101.05
ENGL101.06
ENGL101.07
ENGL101.08
ENGL101.09
ENGL101.10
ENGL101.11
ENGL101.12
ENGL101.13
ENGL101.14
ENGL101.15
ENGL101.16
ENGL101.17

================================================================================


================================================================================

For the stratification category: gender

................................................................................

Number of unique values = 2
Unique values: 

Female
Male

================================================================================


================================================================================

For the stratification category: racecat

................................................................................

Number of unique values = 3
Unique values: 

1
2
3

================================================================================


```

### Decide the number of treatment groups


```
-------------------------------------------------
How many treatment conditions, excluding control?
-------------------------------------------------

( 1 ) 1
( 2 ) 2
( 3 ) 3
( 4 ) 4
( 5 ) 5

CHOICE: 
```

### Choose the type of labels  
  

```
--------------------------
Which labels will you use?
--------------------------

( 1 ) Apli-01277
( 2 ) Avery-3422
( 3 ) Avery-5160
( 4 ) Avery-5161
( 5 ) Avery-5162
( 6 ) Avery-5163
( 7 ) Avery-5164
( 8 ) Avery-8600
( 9 ) Avery-L7163

CHOICE: 
```

### Choose what you want on the labels  


```
---------------------------------------
What do you want on the printed labels?
---------------------------------------

( 1 ) classid
( 2 ) id
( 3 ) name
( 4 ) gender
( 5 ) racecat

CHOICE: 
```

Separate multiple options with a space keeping in mind that the order matters. For example, `3 2 1`, would gives labels that showed: 


```
<name>
<id>
<classid>
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

## (2) Generate labels from prior randomization

If you have already randomized your roster and want to reprint the labels, choose the second option from the first prompt. You will be asked:

```
-----------------------------------
Which CSV file contains the roster?
-----------------------------------

( 1 ) assignment.csv
( 2 ) fakeclasslist.csv
( 3 ) File not in this directory

CHOICE: 
```
which should be the original roster file, and,  

```
---------------------------------------
Which CSV file contains the assignment?
---------------------------------------

( 1 ) assignment.csv
( 2 ) fakeclasslist.csv
( 3 ) File not in this directory

CHOICE: 
```
which should be the `assigment.csv` file generated the first time. These two files will be merged on the randomization column. After these steps, you will once again be asked to choose the types of labels and what you want printed on them.

### Adjustments to labels

When reprinting labels, you will able to adjust the printing placement of the labels as well as the font size.

```
-----------------------------------------------------
Do you want to adjust label margins and/or font size?
-----------------------------------------------------

( 1 ) Yes
( 2 ) No
```
If you say yes, you will get the following options:

```
Please enter horizontal adjustment (negative number for left): 
Please enter vertical adjustment (negative number for up):
Please enter font size from 7 to 15 (default is 11):
```
Horizontal/vertical adjustments are additive. A positive number moves the labels to the right and down. Negative numbers are reverse the direction. Units are in millimeters.

Font size must be one of the following options: `7, 8, 9, 10, 11, 12, 13, 14, 15`.


## Acknowledgements
* Originators and contributors to [PyFPDF](https://code.google.com/p/pyfpdf/)
* [List of random names](http://listofrandomnames.com/) and [Mark Heckmann at ryouready](https://ryouready.wordpress.com/2008/12/18/generate-random-string-name/) for helping me generate my fake class data
