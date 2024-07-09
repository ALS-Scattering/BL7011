"""
    This file contains a script to read and plot asc data from the photon
    correlation spectroscopy setup at the ALS (i forget which room it's in)

    Authors: Dayne Sasaki
"""

# Import packages
import pandas as pd

def main():
    MARKER = '\n\n' # This string occurs between the different data sections
    dir = '/Users/yoshikisd/Documents/ALS-MIT/Data/Tabletop PCS setup/20240528 - Blackbox testing/'
    file = 'With rubber cap on.ASC'
    path = dir + file

    row_start_correlation = None
    row_end_correlation = None
    row_start_counts = None
    row_end_counts = None
    duration = None
    duration_float = None
    runs = None
    temperature = None
    data_correlation = None

    with open(path,
              mode='r',
              encoding='latin-1') as data_file:
        # Break up text file into sections which different data
        separated_data = (data_file.read()).split(MARKER)
        for idx, data_string in enumerate(separated_data):
            if 'Correlation' in data_string:
                pass


        """
        for row_number, line in enumerate(data_file):
            if row_number <= 28:
                # Save the file header data, which only occurs before line 28
                if 'Temperature' in line:
                    temperature = float(line.split()[3])
                elif 'Duration' in line:
                    duration = float(line.split()[3])
                elif 'FloatDur' in line:
                    duration_float = float(line.split()[3])
                elif 'Runs' in line:
                    runs = int(line.split()[3])
            else:
                # Beyond line 28, look for the correlation/count data sets
                if 'Correlation' in line:
                    row_start_correlation = row_number
                elif 'Count Rate' in line:
                    row_start_counts = row_number

            if 'Temperature' in line:
            print(line)
            #if 'Correlation' in line:
            """



    # Using np.loadtxt
    # It seems like the data is encoded using ISO-8859-1

    ascii_grid = np.loadtxt(path,
                            encoding='ISO-8859-1',
                            unpack=True)
    print(path)
    # Load the file and read the data
    with open(path, mode='r') as f:
        # Look for the
        reader = csv.reader(f, delimiter='\t')
        d = list(reader)

    print(reader.shape)



if __name__ == '__main__':
    main()