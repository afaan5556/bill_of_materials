import pandas as pd

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

def find_floor(level_list, item_list):
    # List to hold index of floor items for each item
    floors = []
    for index, level in enumerate(level_list):
        loop_level = level
        loop_index = index
        # Number of times the level will need to be reset before hitting 1
        if level == 0:
            floors.append('N/A')
        elif level == 1:
            floors.append(item_list[index])
        else:
            while loop_level > 1:
                loop_index -= 1
                loop_level = level_list[loop_index]
            floors.append(item_list[loop_index])
        
    return floors

def main(ebom_csv_path, ebom_csv_skiprows, network_csv_path, network_csv_skiprows):

    # Read the ebom - engine='python' is needed after a google search re: unicode
    ebom = pd.read_csv(ebom_csv_path, skiprows=ebom_csv_skiprows, engine='python')
        
    # Add the parents list to the df as a new Series by calling the list_parents function
    ebom['Parents'] = list_parents(ebom['level'].tolist(), ebom['item_number'].tolist())
    # Reverse each list in the ebom['Parents'] Series so that the Chassis kpn is the first element in the list
    ebom['Parents'] = ebom['Parents'].apply(lambda x: x[::-1])
    
    # Add the floors list to the df as a new Series by calling the find_floor function
    ebom['floor_item_number'] = find_floor(ebom['level'].tolist(), ebom['item_number'].tolist())
    
    # Read network mapping - engine='python' is needed after a google search re: unicode
    network = pd.read_csv(network_csv_path, skiprows=network_csv_skiprows, engine='python')
    
    # Drop duplicates in the item_number column of the network df
    network = network.drop_duplicates(subset='item_number', keep='first')
    
    # Bring in the "Netwok Text Final" data from the network df to the ebom df. Kind of like an excel vlookup using pandas merge 
    ebom = pd.merge(ebom, network[['item_number', 'Network Text Final']], on='item_number', how='left')
    
    # Temporary dataframe of just the 'item_num' and 'item_name' columns
    temp_item_df = ebom[['item_number', 'item_name']]
    
    # Temporary dataframe of just the floor item numbers and drop duplicates
    temp_floor_df = pd.DataFrame(ebom['floor_item_number']).drop_duplicates()
    
    # Merge temp_floor_df with temp_item_df to get the floor to item mapping, and merge the result with ebom
    ebom = ebom.merge(temp_floor_df.merge(temp_item_df, how = 'left', right_on = 'item_number', left_on = 'floor_item_number').drop('item_number', axis =1), on = 'floor_item_number', suffixes=('', '_parent_floor'))
    
    return ebom

ebom_df = main('../BOM_Array_v3.3.csv', 11, '../network_v3.3.csv', 0)

ebom_df.to_csv('../BOM_pivot_ready')
