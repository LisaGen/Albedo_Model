import csv

# Read data from CSV file
csv_file_path = '/localdata/lgeneros/data_new_albedo_3eb.csv'
data = []

with open(csv_file_path, mode='r') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        data.append(float(row[3]))  # Assuming the value is in the second column

# Calculate the average
average = sum(data) / len(data)
print("Average:", average)