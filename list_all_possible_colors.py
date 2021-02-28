import csv

with open("identification_ref.csv", newline='') as csvfile:
     reader = csv.DictReader(csvfile)
     for row in reader:
         print(row['Color (Ring)'])