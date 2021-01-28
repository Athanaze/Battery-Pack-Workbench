import csv

with open("price_performance.csv", newline='') as csvfile:
     reader = csv.DictReader(csvfile)
     for row in reader:
         print(row['Brand'], row['max. Weight in g (Datasheet)'])