import numpy as np
import pandas as pd
import time
import gspread
from pprint import pprint
from oauth2client.service_account import ServiceAccountCredentials
scope = ["..."]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("sleepData").sheet1

data = sheet.get_all_records()
pprint(data)

row = sheet.row_values(2)
col = sheet.col_values(1)

print(row)
print(col)

for word in col:
    print(word)
    time.sleep(1)

insertrow = ['Azan', 'Computer Science', 'A']
sheet.insert_row(insertrow, 5)

sheet.insert_row(['', '', '', 'marks'], 1)
sheet.insert_row([2], 6)
# ------------------------------------------------------------------------------
# TODO: inserting array values one by one in the sheet


def insertarr():
    l = [i for i in range(20)]  # inserting 5 values to the google spreadsheet
    for i, letter in enumerate(l):
        sheet.insert_row([l[i]], 6 + i)
        print(i)


insertarr()
# ------------------------------------------------------------------------------
# TODO: inserting array values one by one in the sheet


def autoVal():
    l1 = [i for i in range(20)]  # inserting 5 values to the google spreadsheet
    l1
    l2 = []
    for i in l1:
        l2.append(i)
        time.sleep(0.2)
        print(l2[-1:])


autoVal()
# ---------------------------------------------------------------------------
# TODO: ralph work(realtime values updation)
l1 = [i for i in range(20)]  # inserting 5 values to the google spreadsheet
l1
l2 = []
for i in l1:
    l2.append(i)
    time.sleep(0.2)
    print(l2[-1:])
    sheet.insert_row(l2[-1:])

# ------------------------------------------------------------------------------
# TODO: testing block, inserting row
sheet.insert_row([1, 2, 3, 4], 6)

marks = np.random.randint(1, 10, 5)
for submarks in marks:
    print(submarks)

# -----------------------------------------------------------------------------
# TODO: update multiple cells
cell_list = sheet.range('D2:D5')
print(cell_list)
cell_values = [20, 15, 16, 19]

for i, val in enumerate(cell_values):  # gives us a tuple of an index and value
    cell_list[i].value = val  # use the index on cell_list and the val from cell_values
sheet.update_cells(cell_list)
# ----------------------------------------------------------------------------
# TODO: adding new column of pass/fail status

cell_list = sheet.range('E1:E5')
cell_values = ['Status', 'Pass', 'pass', 'Pass', 'Fail']

for i, val in enumerate(cell_values):  # gives us a tuple of an index and value
    cell_list[i].value = val  # use the index on cell_list and the val from cell_values
sheet.update_cells(cell_list)


# ----------------------------------------------------------------------------
# TODO: ralph work- pandas

date = pd.to_datetime("now")
date.strftime("%T - %A - %D ")
