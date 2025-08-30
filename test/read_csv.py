import pandas as pd
import numpy as np

np.set_printoptions(suppress=True, precision=3)

arc_path = 'src/arc.csv'
circle_path = 'src/circle.csv'
line_path = 'src/line.csv'
others_path = 'src/others.csv'

# each batch will have 16 example: 1 arc, 1 circle, 1 line, 1 others in order and repeat for 4 times 
# I will have 25 batches in total
# use 400 to load all examples so the batch size is flexible 
result = np.empty((400, 50, 6))  # 25 batches of (16 examples, each example has 50 samples points and each point has 6 features)
label_result = np.empty((400, 4))  

for i in range(100):  # each time we load 4 examples (1 arc, 1 circle, 1 line, 1 others) so we can create mixed batches in a factor of 4
    skip_rows = i * 51 + 1 if i > 0 else 0  # Skip header + previous chunks + empty lines
    arc_data = pd.read_csv(arc_path, nrows=50, skiprows=skip_rows, header=None).to_numpy()
    circle_data = pd.read_csv(circle_path, nrows=50, skiprows=skip_rows, header=None).to_numpy()
    line_data = pd.read_csv(line_path, nrows=50, skiprows=skip_rows, header=None).to_numpy()
    others_data = pd.read_csv(others_path, nrows=50, skiprows=skip_rows, header=None).to_numpy()
    result[i*4] = arc_data
    label_result[i*4] = [1, 0, 0, 0]  # one-hot encoding for arc
    result[i*4+1] = circle_data
    label_result[i*4+1] = [0, 1, 0, 0]  # one-hot encoding for circle
    result[i*4+2] = line_data
    label_result[i*4+2] = [0, 0, 1, 0]  # one-hot encoding for line 
    result[i*4+3] = others_data
    label_result[i*4+3] = [0, 0, 0, 1]  # one-hot encoding for others
    
# one-hot label for them: [1, 0, 0, 0] first column is arc, second is circle, third is line, fourth is others
# sample check 
print(result[8]) # it will be 0-3, 4-7, 8-11, so 8 is arc
print(label_result[8] == [1, 0, 0, 0]) # if True ok

