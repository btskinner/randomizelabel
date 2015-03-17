################################################################################
#
# FILE: randomizelabel.py
# AUTH: Benjamin Skinner
# INIT: 13 March 2015
#
################################################################################

# PURPOSE ----------------------------------------------------------------------
#
# The purpose of this file is to:
#
# (1) randomize a list of participants into treatment and control groups
# (2) create labels for each group
# (3) create a master table that lists participant assignments
#
# To do this, this file requires the following:
#
# (1) a csv file with participant names and any information required if
#     sampling should be blocked within groups
#   
# NB: requires this code in the same directory saved as pdflabels.py
# https://pyfpdf.googlecode.com/hg-history/png_alpha/pdflabels.py
# ------------------------------------------------------------------------------

# //////////////////////////////////////////////////////////////////////////////
# LIBRARIES
# //////////////////////////////////////////////////////////////////////////////

import pandas as pd                       # for working with csv
from random import randint, shuffle       # for randomizing
import math
from fpdf import FPDF                     # for printing labels
import os                                 # for checking for local file
import urllib                             # for downloading file

# don't need warning about this
pd.options.mode.chained_assignment = None  # default='warn'

# check for pdflabels.py; download if not there
if not os.path.exists('./pdflabels.py'):
    print('\nrequired file nonexistent...downloading...')
    url = 'https://pyfpdf.googlecode.com/hg-history/png_alpha/pdflabels.py'
    urllib.urlretrieve(url, 'pdflabels.py')

import pdflabels

# //////////////////////////////////////////////////////////////////////////////
# PYTHON FUNCTIONS
# //////////////////////////////////////////////////////////////////////////////

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# USER PROMPTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def whichCSV():
    while True:
        prompt = '\nWhich CSV file contains the names of those to be randomized?\n\n'
        print '\n'
        csvfiles = []
        for f in os.listdir('./'):
            if f.endswith('.csv'):
                csvfiles.append(f)
        csvfiles.append('File not in this directory')
        for f in csvfiles:
            print '(', csvfiles.index(f) + 1, ')', os.path.basename(f)
        csvfilenum = raw_input(prompt)

        # error handling: only digits allowed
        if not csvfilenum.isdigit():
            print('\nERROR: Only digits are accepted; choose again.')
            continue
        else:
            csvfilenum = int(csvfilenum) - 1

        # error handling: only proper integers allowed
        if csvfilenum > len(csvfiles) - 1 or csvfilenum < 0:
            print('\nERROR: Number out of range; choose again.')
            continue
        else:
            break
    while True:
        if csvfilenum == len(csvfiles) - 1:
            prompt = '\n give full path to CSV file:\n\n'
            csvfile = raw_input(prompt)
        else:
            csvfile = os.path.abspath(csvfiles[csvfilenum])

        # error handling
        if not csvfile:
            print('\nERROR: No csv file given; choose a file.')
            continue
        else:
            break

    return csvfile
    
def whichColumns(csvf):   

    # open csv file; read csv file
    df = pd.read_csv(csvf)

    # figure out which columns are which: randomization unit
    headings = list(df.columns.values)
    while True:
        prompt = "\n\nWhich column contains the randomization unit?\n\n"
        print '\n'
        for name in headings:
            print '(', headings.index(name) + 1, ')', name
        unitcol = raw_input(prompt)

        # error handling: only digits allowed
        if not unitcol.isdigit():
            print('\nERROR: Only digits are accepted; choose again.')
            continue
        else:
            unitcol = int(unitcol) - 1

        # error handling: only proper integers allowed
        if unitcol > len(headings) - 1 or unitcol < 0:
            print('\nERROR: Number out of range; choose again.')
            continue
        else:
            pass

        # randomization unit not unique: exit program
        if len(df.iloc[:,unitcol]) > len(df.iloc[:,unitcol].unique()):
            print('\nRandomization unit not unique; choose another unit.')
            continue
        else:
            break

    # figure out which columns are which: blocking level
    while True:
        prompt = """\n\nAre you randomizing with groups (choose a number)?
        \n(1) Yes
        \n(2) No
        \n\n"""
        wish = raw_input(prompt)
        options = ['1','2']

        # error handling
        if wish not in options:
            print('\nERROR: Number not in options; choose again')
            continue
        else:
            break

    # randomize within groups
    if wish == '1':
        while True:
            prompt = "\n\nWhich column contains the groups?\n\n"
            print '\n'
            for name in headings:
                print '(', headings.index(name) + 1, ')', name
            groupcol = raw_input(prompt)
    
            # error handling: only digits allowed
            if not groupcol.isdigit():
                print('\nERROR: Only digits are accepted; choose again.')
                continue
            else:
                groupcol = int(groupcol) - 1

            # error handling: only proper integers allowed
            if groupcol > len(headings) - 1 or groupcol < 0:
                print('\nERROR: Number out of range; choose again.')
                continue
            else:
                break
        
    elif wish == '2':
        groupcol = None

    # no stratification if without grouping (should just group otherwise) 
    if groupcol is not None:

        # figure out which columns are which: stratification
        while True:
            prompt = """\n\nShould randomization be stratified (choose a number)?
            \n(1) Yes
            \n(2) No
            \n\n"""
            wish = raw_input(prompt)
            options = ['1','2']   

            # error handling
            if wish not in options:
                print('\nERROR: Number not in options; choose again')
                continue
            else:
                break       

        # stratified groupings
        if wish == '1':
            while True:
                prompt = '\n\nWhich column contains the stratification category?\n\n'
                print '\n'
                for name in headings:
                    print '(', headings.index(name) + 1, ')', name
                stratcol = raw_input(prompt)

                # error handling: only digits allowed
                if not stratcol.isdigit():
                    print('\nERROR: Only digits are accepted; choose again.')
                    continue
                else:
                    stratcol = int(stratcol) - 1

                # error handling: only proper integers allowed
                if stratcol > len(headings) - 1 or stratcol < 0:
                    print('\nERROR: Number out of range; choose a proper number.')
                    continue
                else:
                    break
            
        elif wish == '2':
            stratcol = None
    else:
        stratcol = None

    # return unit, group, and stratification columns
    return df, unitcol, groupcol, stratcol

def numExperGroups():

    # ask for number of treatment conditions
    while True:
        prompt = """\n\nHow many treatment conditions, excluding control?
        \n\nPlease enter an integer (choosing 0 means only control group).
        \n\n"""
        wish = raw_input(prompt)

        # error handling (needs to be an integer)
        if not wish.isdigit() or wish < 0:
            print('\nERROR: Non-digit entered or number out of range; choose a proper number.')
            continue
        else:
            wish = int(wish)
            break
        
    # init number of treatment and control based on input
    if wish == 1:
        conditions = ['C','T']
    else:
        conditions = ['C'] + ['T' + str(i + 1) for i in range(wish)]

    # return conditions
    return conditions

def whichLabels():

    # get label options
    labopts = list(pdflabels.commercial_labels.keys())

    # ask for types of labels to be used
    while True:
        prompt = "\n\nWhich labels will you use?\n\n"
        print '\n'
        for name in labopts:
            print '(', labopts.index(name) + 1, ')', name
        labs = raw_input(prompt)

        # error handling: only digits allowed
        if not labs.isdigit():
            print('\nERROR: Only digits are accepted; choose again.')
            continue
        else:
            labs = int(labs) - 1

        # error handling
        if labs > len(labopts) - 1 or labs < 0:
            print('\nERROR: Number out of range; choose a proper number.')
            continue
        else:
            break

    # return name of labels to be used
    labtype = labopts[labs]; return labtype

def whatLabels(df):

    # get column options
    colopts = list(df.columns.values)

    # ask for what is wanted on labels
    while True:
        prompt = """\n\nWhat do you want on the printed labels?
        \nPlease select desired columns by number, separated by commas.\n\n"""
        print '\n'
        for name in colopts:
            print '(', colopts.index(name) + 1, ')', name
        labitems = list(raw_input(prompt).split(','))      

        # error handling: correct format
        try:
            labitems = [int(i) - 1 for i in labitems]
        except ValueError:
            print('\nERROR: Use integers separated by commas; choose again.')
            continue

        # error handling: make sure columns exist     
        try:
            [df.columns.values[i] for i in labitems]
        except (TypeError, ValueError, IndexError):
            print('\nERROR: Number out of range; choose a proper number.')
            continue

        # error handling: no negative columns (means person chose 0)
        if any(x < 0 for x in labitems):
            print('\nERROR: Number out of range; choose a proper number.')
            continue
        else:
            pass

        # error handling: too many columns selected 
        if len(labitems) > len(colopts) - 1:
            print('\nERROR: Too many columns chosen; choose again.')
            continue
        else:
            pass

        # error handling: too few columns selected 
        if not labitems:
            print('\nERROR: Too few columns chosen; choose again.')
            continue
        else:
            break

    # return columns for labels
    return labitems

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# RANDOMIZATIONS FUNCTION
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def randomizeUnits(df,cond,unit,group,strat):

    # straight-forward randomization (no grouping or stratification)
    if group is None and strat is None:
        # assign random integer for each unit that is length of conditions
        a = [randint(0, len(cond) - 1) for x in range(len(df.index))]
        # map condition value onto assignment value
        a = [cond[i] for i in a]
        # add to dataframe
        df['assign'] = a
        # return the dataframe with assignment
        return df

    # within groups, no stratification
    if group is not None and strat is None:
        # subset date by unique groups; init blank dataframe
        gp = list(df.iloc[:,group].unique()); out = pd.DataFrame()
        for g in gp:
            # subset data
            sub = df[df.iloc[:,group] == g]
            # get relatively even number of each condition within group
            a = cond * int(math.ceil(float(len(sub.index)) / len(cond)))
            # shuffle; reduce to size of dataframe by chopping off end
            shuffle(a); a = a[0:len(sub.index)]
            # add to subdataframe
            sub['assign'] = a
            # append
            out = out.append(sub, ignore_index = True)

        # return the dataframe with assignment
        df = out; return df

    # within groups, with stratification
    if group is not None and strat is not None:
        # subset date by unique groups; init blank dataframe
        gp = list(df.iloc[:,group].unique())
        st = list(df.iloc[:,strat].unique())
        out = pd.DataFrame()
        for g in gp:
            sub = df[df.iloc[:,group] == g]
            for s in st:
                # subset data
                ssub = sub[sub.iloc[:,strat] == s]
                # get relatively even number of each condition within group
                a = cond * int(math.ceil(float(len(ssub.index)) / len(cond)))
                # shuffle; reduce to size of dataframe by chopping off end
                shuffle(a); a = a[0:len(ssub.index)]
                # add to subdataframe
                ssub['assign'] = a
                # append
                out = out.append(ssub, ignore_index = True)

        # return the dataframe with assignment
        df = out; return df

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# OUT/PRINT FUNCTIONS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            
def outTable(df,unit):
    # subset dataframe (don't need everything for this list); output
    cols = [df.columns.values[unit], 'assign']
    df.to_csv('assignment.csv', index = False, columns = cols)

def makeLabels(df,labitems,labtype):
    # get unique experimental groups
    expergroup = list(df['assign'].unique())
    # loop through each experimental group
    for eg in expergroup:
        # subset data
        sub = df[df.assign == eg]
        # move through rows adding labels with items as choosen; init page
        pl = pdflabels.PDFLabel(labtype); pl.add_page()
        for index, row in sub.iterrows():
            labval = []
            for i in range(len(labitems)):
                labval.append(str(row[sub.columns.values[labitems[i]]]))
            labstring = '\n'.join(labval)
            pl.add_label(labstring)
        pl.output('addresslabels_' + str(eg) + '.pdf', 'F')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN COLLECTION FUNCTION
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():
    # get csv file
    csvfile = whichCSV()
    # assign columns from csv file accordingly
    df,u,g,s = whichColumns(csvfile)
    # figure out number of experimental groups
    cond = numExperGroups()
    # randomize
    df = randomizeUnits(df,cond,u,g,s)
    # output assignment table as csv
    outTable(df,u)
    # get label types
    labtype = whichLabels()
    # get label options
    labitems = whatLabels(df)
    # make labels
    makeLabels(df,labitems,labtype)

# //////////////////////////////////////////////////////////////////////////////
# RUN THE SCRIPT
# //////////////////////////////////////////////////////////////////////////////

if __name__== "__main__":
    main()
    print('Success! See local directory for label sheets and assignment table.')
