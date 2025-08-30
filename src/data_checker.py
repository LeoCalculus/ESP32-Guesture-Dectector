# data integrity checker

import pandas as pd

try:    
    for i in range(1, 150):
        data = pd.read_csv('src/others.csv', nrows=1, skiprows=(i * 51 - 1), skip_blank_lines=False)
        if data.shape != (1,0):
            print(f"Data integrity failed at row {i*51-1}")
        else:
            print(f"line {i*51} is valid with shape {data.shape}")
    # with open('src/circle.csv', 'rb') as file:
    #     file.seek(0)
    #     lines = file.readlines()
    #     print(repr(lines[1070:1100]))
    
            
except FileNotFoundError:
    print("Error: src/arc.csv not found")
except Exception as e:
    print(f"Error reading file: {e}")