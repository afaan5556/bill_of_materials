### PART OF EXCEL FUNCTIONLITY NOT NEEDED IN PYTHON
# Calc Count Previous and Count Actual columns as lists
level_list = ebom['level'].tolist()
level_list_previous = [level_list[0:index].count(i-1) for index, i in enumerate(level_list)]
level_list_actual = [level_list[0:index].count(i) + 1 for index, i in enumerate(level_list)]

# Add Count Previous and Count Actual to df
ebom['Count_Previous'] = level_list_previous
ebom['Count_Actual'] = level_list_actual

# Add Concatenate column to df
ebom['Conc'] = [int(str(i) + str(j)) for i, j in zip(ebom['Count_Actual'].tolist(), ebom['level'])]
