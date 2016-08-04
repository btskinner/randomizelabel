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

def matchMessage(optlist, rc = None, gc = None, sc = None):
     if rc is not None:
          rc = optlist[rc]
     else:
          rc = ''
     if gc is not None:
          gc = optlist[gc]
     else:
          gc = ''
     if sc is not None:
          sc = ', '.join([optlist[i] for i in sc])
     else:
          sc = ''
     print('')
     print('Randomization unit: ' + rc)
     print('Blocking group:     ' + gc)
     print('Stratify on:        ' + sc, end = '\n\n')
     
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

def dataCheck(df, header, ru, group, strat):
     
     # get summary stats for each non-None column
     cols = flatten([ru, group, strat])
     cols = [x for x in cols if x is not None]

     # print for review
     for c in cols:
          name = header[c]
          uniq = sorted(list(df.iloc[:,c].unique()))
          if name == header[ru]:
               t = 'randomization unit'
          elif name == header[group]:
               t = 'grouping category'
          else:
               t = 'stratification category'
          print('\n' + '=' * 80, end = '\n\n')
          print('For the ' + t + ': {0}'.format(name))
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
            csvfile = input('Please give full path to CSV file: ')
        else:
            csvfile = os.path.abspath(fopts[choice])
            
        try:
            df = pd.read_csv(csvfile)

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
    prompt = 'Which column contains the randomization unit?'
    ru = whichColumn(df, header, prompt, unique = True)
     
    # blocking
    prompt = 'Are you randomizing within groups?'
    choice = pickOpt(prompt, ['Yes', 'No'])
     
    if choice == 1:
        group = None
        strat = None
        return ru, group, strat

    while True:
        prompt = 'Which column contains the groups?'
        choice = whichColumn(df, header, prompt)
        if badOpt(choice, header, rc = ru):
            errorMessage('Column already chosen. Please choose again.')
            matchMessage(header, rc = ru)
            continue
        group = choice
        break

    # stratification
    prompt = 'Should randomization be stratified?'
    choice = pickOpt(prompt, ['Yes', 'No'])

    if choice == 1:
        strat = None
        return ru, group, strat

    while True:
        prompt = 'Which column(s) contains the stratification category?'
        choice = whichColumn(df, header, prompt, multopts = True)
        if badOpt(choice, header, rc = ru, gc = group):
            errorMessage('Column already chosen. Please choose again.')
            matchMessage(header, rc = ru, gc = group)
            continue
        strat = choice
        break
     
    return ru, group, strat
    
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
# RANDOMIZATION FUNCTION
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def randomizeUnits(df, header, cond, ru, group = None, strat = None):

    # group_by categories, dropping None
    gbc = [x for x in flatten([group, strat]) if x is not None]
    
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
        
    assignment = flatten(assignment)
    
    df['assign'] = assignment
    
    return df

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# OUT/PRINT FUNCTIONS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            
def outTable(df, header, ru):
    cols = [header[ru], 'assign']
    df.to_csv('assignment.csv', index = False, columns = cols)

def makeLabels(df, labitems, labtype):
    # get unique experimental groups
    expergroup = list(df['assign'].unique())
    # loop through each experimental group
    for eg in expergroup:
        sub = df[df['assign'] == eg]

        pl = pdflabels.PDFLabel(labtype)
        pl.padding = 7
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
        # randomization settings
        ru, group, strat = randSettings(df, header)
        # data check
        dataCheck(df, header, ru, group, strat)
        # conditions
        cond = numExperGroups()
        # randomize
        df = randomizeUnits(df, header, cond, ru, group, strat)
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
    # make labels
    makeLabels(df, labitems, labtype)
    
# //////////////////////////////////////////////////////////////////////////////
# RUN THE SCRIPT
# //////////////////////////////////////////////////////////////////////////////

if __name__ == '__main__':
    main()
    text = 'Success! See local directory for label sheets and assignment table.'
    promptMessage(text)
