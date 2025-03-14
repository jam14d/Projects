import csv  # For reading CSV files
import math  # For distance calculations
from dataclasses import dataclass  # For structured data storage

@dataclass
class Point:
    """Class to represent a 3D point with a type label (GFP or RFP)."""
    x: float
    y: float
    z: float
    type: str  # Either 'GFP' or 'RFP'

def read_csv_data(filename):
    """Reads a CSV file and returns a list of Point objects."""
    points = []
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row

        for row in csv_reader:
            if len(row) < 5:  # Ensure the row has enough columns
                continue  # Skip rows that are too short
            
            try:
                points.append(Point(float(row[1]), float(row[2]), float(row[3]), row[4]))  # x, y, z, type
            except ValueError:
                print(f"Skipping malformed row: {row}")  # Print a warning for bad data

    return points

def find_colocalized_cells(points, threshold=1):
    """Finds GFP and RFP cells that are within a distance threshold."""
    matches = []

    for i in range(len(points)):
        #print(i)
        for j in range(i + 1, len(points)):
            a, b = points[i], points[j]

            if a.type != b.type:  # Only compare GFP vs. RFP
                dist = math.dist((a.x, a.y, a.z), (b.x, b.y, b.z))
                if dist < threshold:
                    matches.append([vars(a), vars(b)])  # Convert to dictionaries for easy output

    return matches

if __name__ == "__main__":
    # Read the CSV file
    csv_data = read_csv_data('yesdata.csv')

    # Find colocalized GFP & RFP cells
    matches = find_colocalized_cells(csv_data)

    # Output the first detected colocalized pair
    if matches:
        print("Colocalized Pair Found:", matches[0])
    else:
        print("No colocalized pairs detected.")
