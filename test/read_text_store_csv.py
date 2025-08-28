import re
import csv

file = 'test/sample.txt'
try:
    with open(file, 'r') as f:
        for line in f:
            extract_result = re.findall(r'\d.\d+', line)
            print(extract_result)
            with open('test/output.csv', 'a', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(extract_result)
                
except FileNotFoundError:
    print(f"File {file} not found.")
except Exception as e:
    print(f"An error occurred: {e}")
    
    