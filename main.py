import os
import random
import sys
import pandas as pd
import numpy as np
import glob
from tkinter import messagebox
# from gui import *
"""""""""""""""""""""""""""
This section read the files.
"""""""""""""""""""""""""""
def readFiles():
    path = r'D:\Personal Project\Datacsv'                                                                                                      #CHANGE THIS TO WHATEVER LOCATION THE FOLDER IS                                     
    files = glob.glob(os.path.join(path,"*.csv"))
    dfs = list()
    name_list = list()
    for i, f in enumerate(files):
        data = pd.read_csv(f, index_col=0).replace(np.nan,'O')
        name = os.path.splitext(os.path.basename(f))[0]
        name_list.append(name)
        data['Name'] = name
        dfs.append(data)
    df = pd.concat(dfs, ignore_index=True)
    name_list_lowercase = [x.lower() for x in name_list]
    return dfs,name_list_lowercase

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Gets the list from GUI (through main) and shuffles each list (high, med, low).
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def getPriority(workers_list):
    [random.shuffle(lst) for lst in workers_list]  # randomize order in each priority
    return workers_list[0],workers_list[1],workers_list[2]

"""""""""""""""""""""""""""""""""""""""""
Checks if the specific shift is available.
"""""""""""""""""""""""""""""""""""""""""
def is_it_available(output,day,time,morning_shift,afternoon_shift,evening_shift,num_workers):
    if time == 1:       #afternoon - needs to be maximum 3 workers!
        if (len(output.iloc[time,day]) < afternoon_shift and num_workers > afternoon_shift):
            return True
        else:
            return False

    if time == 0:    #morning and evening - needs to be maximum 3 workers!
        if len(output.iloc[time,day]) < morning_shift and num_workers > morning_shift:
            return True
        else:
            return False

    if time == 2:    #morning and evening - needs to be maximum 3 workers!
        if len(output.iloc[time,day]) < evening_shift and num_workers > evening_shift:
            return True
        else:
            return False

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Place function place the shifts of the people that did V by prio, high->med->low .
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def placePrio(data,output,person_list,morning,afternoon,evening,num_workers):
    for person in person_list:
        for name in range(len(data)):
            if data[name].loc['Morning', 'Name'].lower() == person.lower():
                for day in range(len(data[name].columns)):
                    for time in range(len(data[name].index)):
                        var = data[name].iloc[time, day]
                        if var == 'V' and is_it_available(output,day,time,morning,afternoon,evening,num_workers):
                            if output.iloc[time,day] != '':
                                output.iloc[time,day].append(data[name].loc['Morning', 'Name'])
                            else:
                                output.iloc[time, day]= [data[name].loc['Morning', 'Name']]

                        else:
                            pass
    return output

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Takes all the places which are not full yet and randomly assign someone who can (who doesn't have X).
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def placeTheRest(data,output,morning_shift,afternoon_shift,evening_shift,index_name,num_workers):
    for day in range(len(output.columns)):
        for time in range(len(output.index)):
            while is_it_available(output,day,time,morning_shift,afternoon_shift,evening_shift,num_workers):
                x = random.choice(index_name)
                if data[x].loc['Morning', 'Name'] not in output.iloc[time,day] and data[x].iloc[time,day] != 'X':
                    if output.iloc[time, day] != '':
                        output.iloc[time, day].append(data[x].loc['Morning', 'Name'])
                    else:
                        output.iloc[time, day] = [data[x].loc['Morning', 'Name']]
    return output

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Checks if the shifts are fair by the fairness value we assigned.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def checkFairness(output,fairness_level):
    fairness_dict = dict()
    for day in output.columns[1:]:
        for time in output.index:
            for item in output.loc[time, day]:
                fairness_dict[item] = fairness_dict.get(item , 0) + 1

    max_val = max(fairness_dict.values())
    min_val = min(fairness_dict.values())
    if max_val - min_val > fairness_level:
        return True , fairness_dict
    else:
        return False , fairness_dict

"""""""""""""""""""""""""""""""""""""""""""""""""""
Makes sure no one gets 3 shifts in a row in one day.
"""""""""""""""""""""""""""""""""""""""""""""""""""
def check_3_shifts(output):
    for day in output.columns[1:]:
        cur_list = list(np.concatenate(output[day].to_list()))
        dict = {i: cur_list.count(i) for i in cur_list}
        if 3 in dict.values():
            return True
    return False

"""""""""""""""""""""""""""""""""""""""""""""""""""
Write into the output with a string and not a list.
"""""""""""""""""""""""""""""""""""""""""""""""""""
def makeIntoString(output):
    for day in range(0,len(output.columns)):
        for time in range(len(output.index)):
            output.iloc[time, day] = ', '.join(output.iloc[time,day])
    return output

"""""""""""""""""""""""""""""""""""""""""""""""""""
Gets the indexes of the workers from the data files.
"""""""""""""""""""""""""""""""""""""""""""""""""""
def get_index(data,high,med,low):
    lst = []
    for i in range(len(data)):
        if data[i].loc['Morning', 'Name'].lower() in high or data[i].loc['Morning', 'Name'].lower()\
                in med or data[i].loc['Morning', 'Name'].lower() in low:
            lst.append(i)
    return lst, len(lst)

"""""""""""""""
The function that runs priority placement (placePrio)
"""""""""""""""
def def_prio(data,output,high,med,low,morning,afternoon,evening,num_workers):
    placePrio(data,output,high,morning,afternoon,evening,num_workers)
    placePrio(data,output,med,morning,afternoon,evening,num_workers)
    placePrio(data,output,low,morning,afternoon,evening,num_workers)
    return output

"""""""""""""""""
THE MAIN FUNCTION!
"""""""""""""""""
def main(workers_list,fairness_level_gui,morning_combobox,afternoon_combobox,evening_combobox):
    try:
        data,name_list = readFiles()
    except Exception as e:
        print(f"\n{e}\nTo fix, add the employees shifts\ncsv files into 'Datacsv' folder.\n")
        sys.exit()

    try:
        output = pd.read_csv(r'D:\Personal Project\output.csv',index_col=0,converters={'COLUMN_NAME': pd.eval}).fillna('')                     #CHANGE THIS TO WHATEVER LOCATION THE FOLDER IS

    except Exception as e:
        print(f"\n{e}\nTo fix, add the 'output.csv' template\nback "
              f"to the main directory.\n")
        sys.exit()


    fairness_level = fairness_level_gui
    morning_shift, afternoon_shift, evening_shift = morning_combobox,afternoon_combobox,evening_combobox
    high, med, low = getPriority(workers_list)

    index_name, num_workers = get_index(data, high, med, low)
    capital_name_list = [word.capitalize() for word in name_list]

    condition = True
    iteration = 0
    while condition:
        output = pd.read_csv(r'D:\Personal Project\output.csv', index_col=0,converters={'COLUMN_NAME': pd.eval}).fillna('')                    #CHANGE THIS TO WHATEVER LOCATION THE FOLDER IS
        def_prio(data, output, high, med, low, morning_shift, afternoon_shift, evening_shift, num_workers)
        placeTheRest(data,output,morning_shift,afternoon_shift,evening_shift,index_name,num_workers)

        condition, dict_s = checkFairness(output,fairness_level)
        if not condition:
            condition = check_3_shifts(output)

        iteration += 1
        if iteration>1000:
            fairness_level +=1
            iteration=0
        if fairness_level - fairness_level_gui > 5:
            messagebox.showinfo(f"Error", f"Fairness level is now {fairness_level}.\nI don't think we can help you today.")
            sys.exit()

    makeIntoString(output)
    date = str(pd.to_datetime('today')).split()[0]
    output.to_csv(f"{date} shifts.csv")



##### ALGORITHM #####
# 1) ASSUME all the data by: name.csv.  X - Cannot work
#                                       V - Want to work
#                                       O - Open to work
# 2) Loop read all data: name = pd.read_csv('....')
# 3) Once we have all the data loaded. Go over all of the data and make a dictionary
#    that have ('high': ['name1','name2',...], ....., 'low': 'name3').
# 4) Make an exact TEMP dictionary as in 3.
# 5) Load the empty csv template named 'output.csv'
# 6) (make 3 functions that check whether the selected shift is available [full or not])
# 7) Go over all prio 'high' V's and place them, same for prio 'med' then for prio 'low'.
#                                                               MORNING - 3 person, AFTERNOON - 1 person, Evening - 3 person.
#                                                               prio 1 can put 6 V, prio 2 can put 5 V prio 3 can put 4 V
#                                                               each person can have 3 X
#
# 8) After all V's placed. Loop around the entire output from Sunday morning. If a shift is available (7) randomly
#    choose a person from the database. If a person have an X or is already
#    in this shift - randomly choose a different person.
# 9) Do a triple loop (2 for loops and then a while loop [run until a the shift is not still available(FALSE)])
#10) Export the final output csv.
#11) In the GUI have a "RANDOM" button that will run the code from scratch.
#12)
#13)
#14)

