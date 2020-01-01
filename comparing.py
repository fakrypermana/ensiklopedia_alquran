import csv
inputs = ["result-tc.csv","result-tf.csv","result-nf.csv"]

fieldnames = []
for filename in inputs:
  with open(filename, "r") as f_in:
    reader = csv.reader(f_in)
    headers = next(reader)
    for h in headers:
      if h not in fieldnames:
        fieldnames.append(h)

print('fieldnames',fieldnames)
# Then copy the data
with open("result.csv", "w") as f_out:   # Comment 2 below
  writer = csv.DictWriter(f_out, fieldnames=fieldnames)
  for filename in inputs:
    with open(filename, "r", newline="") as f_in:
      reader = csv.DictReader(f_in)  # Uses the field names in this file
      for line in reader:
        # Comment 3 below
        writer.writerow(line)