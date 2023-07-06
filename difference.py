import csv


def compare_csv(csv1_path, csv2_path, output_path):
    # Read the first CSV file
    with open(csv1_path, 'r') as csv1_file:
        csv1_reader = csv.reader(csv1_file)
        csv1_rows = list(csv1_reader)

    # Read the second CSV file
    with open(csv2_path, 'r') as csv2_file:
        csv2_reader = csv.reader(csv2_file)
        csv2_rows = list(csv2_reader)

    # Find the missing rows in csv2
    missing_rows = []
    for row1 in csv2_rows:
        if row1[0] not in [row2[0] for row2 in csv1_rows]:
            missing_rows.append(row1)

    # Write the missing rows to the output CSV file
    with open(output_path, 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerows(missing_rows)


# Usage example
csv1_path = 'org.csv'
csv2_path = '0607_org.csv'
output_path = 'new_leads0607.csv'

compare_csv(csv1_path, csv2_path, output_path)
