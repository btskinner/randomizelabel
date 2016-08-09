#!/usr/bin/env python3

################################################################################
#
# FILE: randomizelabel.py
# AUTH: Benjamin Skinner
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
# ------------------------------------------------------------------------------

# //////////////////////////////////////////////////////////////////////////////
# LIBRARIES
# //////////////////////////////////////////////////////////////////////////////

import pandas as pd      # for working with csv
import numpy  as np      # for checking column data types
import random as rd      # for randomizing
import math              # for ceiling function
import fpdf              # for printing labels
import os                # for checking for local file
import urllib.request    # for downloading file

# //////////////////////////////////////////////////////////////////////////////
# DOWNLOAD TEMPLATE
# //////////////////////////////////////////////////////////////////////////////

if not os.path.exists('./pdflabels.py'):
    print('Required file nonexistent...downloading...')
    url = 'https://raw.githubusercontent.com/reingart/pyfpdf/master/tools/'
    f = 'pdflabels.py'
    urllib.request.urlretrieve(url + f, f)

import pdflabels

# //////////////////////////////////////////////////////////////////////////////
# FUNCTIONS
# //////////////////////////////////////////////////////////////////////////////

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# UTILITY
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def printOpts(optlist):
    for l in optlist:
        print('(', optlist.index(l) + 1, ')', l)

def promptMessage(text):
    print('\n')
    print('-' * len(text))
    print(text)
    print('-' * len(text), end = '\n\n')

def errorMessage(text):
    o = len(text) + 7
    print('\n')
    print('*' * o)
    print('ERROR: ', end = '')
    print(text)
    print('*' * o, end = '\n\n')

def matchMessage(optlist, rc = None, bg = None):
    if rc is not None:
        rc = optlist[rc]
    else:
        rc = ''
    if bg is not None:
        bg = ', '.join([optlist[i] for i in sc])
    else:
        bg = ''
    print('')
    print('Randomization unit: ' + rc)
    print('Blocking group(s):  ' + bg, end = '\n\n')
     
def pickOpt(prompt, optlist, multopts = False):
    
    em1 = 'Only digits are accepted. Please choose again.'
    em2 = 'Please choose again from among options.'
    
    if multopts:
        while True:
            flag = 0
            promptMessage(prompt)
            printOpts(optlist)
            try:
                choice = [int(x) for x in input('\nCHOICE: ').split()]
                
            except ValueError:
                errorMessage(em1)
                continue
            
            if len(choice) == 0 | len(choice) > len(optlist):
                errorMessage(em2)
                continue
            
            for i in choice:
                if i > len(optlist) or i < 1:
                    errorMessage(em2)
                    flag = 1
                    continue
            if flag == 0:
                break

        return [x - 1 for x in choice]
                
    while True:
        promptMessage(prompt)
        printOpts(optlist)
        try:
            choice = int(input('\nCHOICE: '))

        except ValueError:
            errorMessage(em1)
            continue
        
        if choice > len(optlist) or choice < 1:
            errorMessage(em2)
            continue
        return choice - 1

# h/t http://stackoverflow.com/a/35415963
def flatten(irrlist):
    if isinstance(irrlist, int):
        return [irrlist]
    flist = []
    for i in irrlist:
        if not isinstance(i, list):
            flist.append(i)
        else:
            flist.extend(flatten(i))
    return flist

def inList(new, old):
    new = flatten(new)
    old = flatten(old)
    reps = []
    for n in new:
        if n in old:
            reps.append(n)
    return reps

def badOpt(choice, header, rc = None, gc = None):
    prior = flatten([rc, gc])
    prior = [i for i in prior if i is not None]
    check = inList(choice, prior)
    if len(check) > 0:
        return True
    return False

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DATA CHECK FUNCTION
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def dataCheck(df, header, ru, block):
     
    # get summary stats for each non-None column
    cols = flatten([ru, block])
    cols = [x for x in cols if x is not None]
    
    # print for review
    for c in cols:
        name = header[c]
        uniq = sorted(list(df.iloc[:,c].unique()))
        if name == header[ru]:
            rand_param = 'randomization unit'
        else:
            rand_param = 'blocking category'
        print('\n' + '=' * 80, end = '\n\n')
        print('For the ' + rand_param + ': {0}'.format(name))
        print('\n' + '.' * 80, end = '\n\n')
        print('Number of unique values = {0}'.format(len(uniq)))
        if name != header[ru]:
            print('Unique values: ', end = '\n\n')
            for i in uniq:
                print(i)
        print('\n' + '=' * 80, end = '\n\n')

    # confirm that user wishes to continue
    prompt = 'Does all look as it should?'
    choice = pickOpt(prompt, ['Yes, continue', 'No, please exit']) 
    
    if choice == 1:       
        prompt = 'Randomization program exited by user request.'
        promptMessage(prompt)
        exit()
          
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# USER PROMPTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def whichCSV(prompt):
    
    fopts = []
    for f in os.listdir('./'):
        if f.endswith('.csv'):
            fopts.append(os.path.basename(f))
    fopts.append('File not in this directory')
               
    choice = pickOpt(prompt, fopts)
    
    while True:
        if choice == len(fopts) - 1:
            csvfile = input('Please give path to CSV file: ').strip()
        else:
            csvfile = os.path.abspath(fopts[choice])
            
        try:
            df = pd.read_csv(os.path.expanduser(csvfile))

        except OSError:
            errorMessage('Unable to read CSV. Please choose another file.')
            continue
        else:
            return df
       
def whichColumn(df, header, prompt, multopts = False, unique = False):
     
    while True:
        choice = pickOpt(prompt, header, multopts)
        if unique and len(df.iloc[:,choice]) > len(df.iloc[:,choice].unique()):
            errorMessage('Values not unique. Please choose another column.')
            continue
        return choice

def randSettings(df, header):

    # randomization unit
    prompt = 'Which column contains the primary randomization unit?'
    ru = whichColumn(df, header, prompt, unique = True)
     
    # blocking
    prompt = 'Should random assignment be blocked?'
    choice = pickOpt(prompt, ['Yes', 'No'])
     
    if choice == 1:
        block = None
        return ru, block

    while True:
        prompt = 'On which column(s) do you wish to block?'
        choice = whichColumn(df, header, prompt, multopts = True)
        if badOpt(choice, header, rc = ru):
            errorMessage('Column already chosen. Please choose again.')
            matchMessage(header, rc = ru)
            continue
        block = choice
        break
     
    return ru, block
    
def numExperGroups():  

    while True:
        prompt = 'How many treatment conditions, excluding control?'
        choice = pickOpt(prompt, [1,2,3,4,5])
        break

    if choice == 0:
        conditions = ['C','T']
    else:
        conditions = ['C'] + ['T' + str(i + 1) for i in range(choice)]

    return conditions

def whichLabelType():
    
    labopts = list(sorted(pdflabels.commercial_labels.keys()))

    while True:
        prompt = 'Which labels will you use?'
        choice = pickOpt(prompt, labopts)
        break

    return labopts[choice]

def whichLabelOpts(df, header):

    prompt = 'What do you want on the printed labels?'
    labitems = whichColumn(df, header, prompt, multopts = True)
    return labitems
               
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# RANDOMIZATION FUNCTIONS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def setSeed():
    while True:
        seed = input('Give integer seed of at least 6 digits: ').strip()
        try:
            int(seed)
        except ValueError:
            errorMessage('Seed not an integer (no letters or decimals)!')
            continue
        if len(seed) < 6:
            errorMessage('Seed not long enough!')
            continue  
        break

    with open('seed.txt', 'w') as f:
        f.write(seed)
    return int(seed)
    
def randomizeUnits(seed, df, header, cond, ru, block = None):

    # set seed
    rd.seed(seed)

    # group_by categories, dropping None
    gbc = [x for x in flatten([block]) if x is not None]
    
    # simple random (no blocking)
    if len(gbc) == 0:
        a = cond * int(math.ceil(float(len(df.index)) / len(cond)))
        df['assign'] = rd.sample(a, len(df.index))
        return df

    # within blocks/groups
    gbc = [header[x] for x in gbc]

    assignment = []
    for index, value in df.groupby(gbc).size().iteritems():
        a = cond * int(math.ceil(value / len(cond)))
        a = rd.sample(a, value)
        assignment.append(a)
    
    df['assign'] = flatten(assignment)
    
    return df

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# OUT/PRINT FUNCTIONS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            
def outTable(df, header, ru):
    cols = [header[ru], 'assign']
    df.to_csv('assignment.csv', index = False, columns = cols)

def adjustLabels():

    while True:
        prompt = 'Please enter horizontal adjustment (negative number for left): '
        h = input(prompt).strip()
        try:
            float(h)

        except ValueError:
            errorMessage('Please give real number.')
            continue

        h = float(h)
        break

    while True:
        prompt = 'Please enter vertical adjustment (negative number for up): '
        v = input(prompt).strip()
        try:
            float(v)

        except ValueError:
            errorMessage('Please give real number.')
            continue

        v = float(v)
        break

    while True:
        prompt = 'Please enter font size from 7 to 15 (default is 11): '
        f = input(prompt).strip()
        try:
            float(f)

        except ValueError:
            errorMessage('Please give real number.')
            continue

        f = int(round(float(f)))

        if f < 7 or f > 15:
            errorMessage('Please choose number between 7 and 15, inclusive.')
            continue
        
        break
    
    return h, v, f

def makeLabels(df, labitems, labtype, h_shift = 3, v_shift = 4, font_size = 11):
    # get unique experimental groups
    expergroup = list(df['assign'].unique())
    # loop through each experimental group
    for eg in expergroup:
        sub = df[df['assign'] == eg]

        pl = pdflabels.PDFLabel(labtype)
        pl.margin_left = pl.margin_left + h_shift
        pl.margin_top = pl.margin_top + v_shift
        pl.set_font_size(font_size)
        pl.line_height = pl.get_height_chars(font_size)
        pl.add_page()

        for index, row in sub.iterrows():
            labval = []
            for i in range(len(labitems)):
                labval.append(str(row[sub.columns.values[labitems[i]]]))
            labstring = '\n'.join(labval)
            pl.add_label(labstring)
        pl.output('assignmentlabels_' + str(eg) + '.pdf', 'F')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN COLLECTION FUNCTION
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():

    # randomize vs print labels from prior randomization
    prompt = 'What do you want to do?'
    opts = ['Randomize and make labels',
            'Generate labels from prior randomization']
    choice = pickOpt(prompt, opts)

    # get roster file
    df = whichCSV('Which CSV file contains the roster?')
    header = list(df.columns.values)

    if choice == 0:
        # set seed
        seed = setSeed()
        # randomization settings
        ru, block = randSettings(df, header)
        # data check
        dataCheck(df, header, ru, block)
        # conditions
        cond = numExperGroups()
        # randomize
        df = randomizeUnits(seed, df, header, cond, ru, block)
        # output assignment table as csv
        outTable(df, header, ru)
    else:
        # get assignment file
        dfa = whichCSV('Which CSV file contains the assignment?')
        ## merge
        df = pd.merge(dfa, df, how = 'left')

    # label type
    labtype = whichLabelType()
    # new header
    header = list(df.columns.values)
    # label items
    labitems = whichLabelOpts(df, header)

    if choice == 1:
        prompt = 'Do you want to adjust label margins and/or font size?'
        choice = pickOpt(prompt, ['Yes', 'No'])
        if choice == 0:
            h, v, f = adjustLabels()
            makeLabels(df, labitems, labtype, h_shift = h, v_shift = v,
                       font_size = f)
        else:
            pass
    else:
        makeLabels(df, labitems, labtype)
    
# //////////////////////////////////////////////////////////////////////////////
# RUN THE SCRIPT
# //////////////////////////////////////////////////////////////////////////////

if __name__ == '__main__':
    main()
    text = 'Success! See local directory for label sheets and assignment table.'
    promptMessage(text)
