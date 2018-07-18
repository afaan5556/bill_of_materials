# -*- coding: utf-8 -*-

import pandas as pd
from pandas import merge, DataFrame

# Read the ebom
ebom = pd.read_csv('../BOM_Array_v3.3.csv', skiprows=11)

# Calc Count Previous and Count Actual columns as lists
level_list = ebom['level'].tolist()
level_list_previous = [level_list[0:index].count(i-1) for index, i in enumerate(level_list)]
level_list_actual = [level_list[0:index].count(i) + 1 for index, i in enumerate(level_list)]

# Add Count Previous and Count Actual to df
ebom['Count_Previous'] = level_list_previous
ebom['Count_Actual'] = level_list_actual

# Add Conc column to df
ebom['Conc'] = [int(str(i) + str(j)) for i, j in zip(ebom['Count_Actual'].tolist(), ebom['level'])]

# Function to find parents
def list_parents(level_list, item_list):
    # List to hold lists of parent items for each item
    parents = []
    for index, level in enumerate(level_list):
        # Number of times the level will need to be reset before hitting 0
        reset_qty = level
        # List to hold parent items for this item in loop
        parents_temp = []
        # Chassis level
        if level == 0:
            parents_temp.append("N/A")
        # Non-chassis levels
        else:
            loop_level = level
            loop_index = index
            step = 1
            while reset_qty > 0:
                # Check if level of item [step] rows above current item is < current item
                if level_list[loop_index - step] < loop_level:
                    # Append corresponding item to parent items list
                    parents_temp.append(item_list[loop_index - step])
                    # Reset the loop level to the newly found parent
                    loop_level = level_list[loop_index - step]
                    # Reduce the parent reset quanity
                    reset_qty -= 1
                else:
                    # Increase step to check a row higher than current row
                    step += 1
        # Loop complete. Append the parents list for the current item to the master parents list
        parents.append(parents_temp)
    return parents

# Add the parents list to the df as a new Series
ebom['Parents'] = list_parents(ebom['level'].tolist(), ebom['item_number'].tolist())
# Reverse each list in the ebom['Parents'] Series so that the Chassis kpn is the first element in the list
ebom['Parents'] = ebom['Parents'].apply(lambda x: x[::-1])

# Read network mapping
network = pd.read_csv('../network.csv')

# Drop duplicates in the item-Number column of the network d
network = network.drop_duplicates(subset='item_number', keep='first')

# Bring in the "Netwok Text Final" data from the network df to the ebom df. Kind of like an excel vlookup but using pandas merge 
ebom = pd.merge(ebom, network[['item_number', 'Network Text Final']], on='item_number', how='left')

