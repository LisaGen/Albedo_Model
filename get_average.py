import csv
#Provides the average value of a column in a csv file
#Used to estimate correction terms for the update of the Albedo model

# Read data from CSV file
csv_file_path = '/localdata/lgeneros/data_new_albedo_3eb.csv' #change with your file path
data = []

with open(csv_file_path, mode='r') as file:
    reader = csv.reader(file)
    next(reader) #skip the frist row of coments
    for row in reader:
        data.append(float(row[3]))  # Assuming the value is in the second column

# Calculate the average
average = sum(data) / len(data)
print("Average:", average)
