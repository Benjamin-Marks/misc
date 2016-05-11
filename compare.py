"""compare.py
Parses strenghts profile spreadsheet, outputs comparisons of traits
"""


import xlrd


__author__ = "Ben Marks"


SPREADSHEET = 'Strengths Profile.xlsx'


#Open File
try:
    sh = xlrd.open_workbook(SPREADSHEET).sheet_by_index(0)
except:
    print("ERROR: Please use an .xlsx file. This filetype is not compatible")
    exit()


#Get number of people, number of columns
found_end = False
num_people = 1
num_rows = 1
while not found_end:
    try:
        sh.cell(0, num_people).value
        num_people += 1
    except IndexError:
        num_people -= 1
        found_end = True

found_end = False
while not found_end:
    try:
        sh.cell(num_rows, 1).value
        num_rows += 1
    except IndexError:
        num_rows -= 1
        found_end = True


#Import data
people = [[0 for x in range(num_rows + 1)] for y in range(num_people)]
for r in range(num_rows + 1):
    for i in range(1, num_people + 1):
        people[i - 1][r] = sh.cell(r, i).value

#Do data validation
for i in range(num_people):
    for j in range(num_rows):
        for k in range(num_rows):
            if j == k:
                continue
            if people[i][j] == people[i][k]:
                print('DATA ERROR: {s}\'s {s} exists twice'.format(people[i][0], people[i][j]))
                exit()

#Start comparisons
differences = [[[0, 'name'] for x in range(num_people)] for y in range(num_people)]
for i in range(num_people):
    for j in range(num_people):
        #don't compare with ourselves
        if i == j:
            continue
        #Add name of other person
        differences[i][j][1] = people[j][0]
        for k in range(num_rows):
            for l in range(num_rows):
                #if this is the same quality, add the change in rows
                if people[i][k] == people[j][l]:
                    differences[i][j][0] += abs(k - l)
                    break

#Sort the data - bubble sort 4 lyfe YOLO
for x in range(len(differences)):
    for y in range(len(differences)-1, 0, -1):
        for i in range(y):
            if differences[x][i][0] > differences[x][i+1][0]:
                temp = differences[x][i]
                differences[x][i] = differences[x][i+1]
                differences[x][i+1] = temp

#Output the data
for i in range(num_people):
    print("\nResults for " + people[i][0] + ":")
    for j in range(num_people):
        if differences[i][j][0] == 0:
            continue
        print('{:20s} {:3d}'.format(differences[i][j][1], differences[i][j][0]))


#For fun: analysis of each trait
traits = [[0, 'name'] for r in range(num_rows)]
for i in range(len(traits)):
    traits[i][1] = people[0][i + 1]
for i in range(len(people)):
    for j in range(len(people[0])):
        for t in range(len(traits)):
            if traits[t][1] == people[i][j]:
                traits[t][0] += j

#Sort the traits data - bubble sort 4 lyfe YOLO
for x in range(len(traits)):
    for y in range(len(traits)-1, 0, -1):
        for i in range(y):
            if traits[i][0] > traits[i+1][0]:
                temp = traits[i]
                traits[i] = traits[i+1]
                traits[i+1] = temp

for i in range(len(traits)):
    print('{:35s} {:6.2f}'.format(traits[i][1], float(traits[i][0])/num_people))
