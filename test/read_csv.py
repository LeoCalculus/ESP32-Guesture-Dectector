import pandas as pd

# file_path = 'src/arc.csv'
# lines_to_read = 50
# data_read = pd.read_csv(file_path, nrows=lines_to_read)
# print(data_read)
arc_path = 'src/arc.csv'
circle_path = 'src/circle.csv'
line_path = 'src/line.csv'
others_path = 'src/others.csv'

for i in range(16):
    arc_data = pd.read_csv(arc_path, nrows=50, skiprows=range(1, i * 50 + 1))
    circle_data = pd.read_csv(circle_path, nrows=50, skiprows=range(1, i * 50 + 1))
    line_data = pd.read_csv(line_path, nrows=50, skiprows=range(1, i * 50 + 1))
    others_data = pd.read_csv(others_path, nrows=50, skiprows=range(1, i * 50 + 1))
    print(f"Arc Data Chunk {i+1}:\n", arc_data)
    print(f"Circle Data Chunk {i+1}:\n", circle_data)
    print(f"Line Data Chunk {i+1}:\n", line_data)
    print(f"Others Data Chunk {i+1}:\n", others_data)