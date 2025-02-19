"""This file contains a class to store asc data from the photon
    correlation spectroscopy setup at the ALS.

    Authors: Dayne Sasaki
"""
import pandas as pd
from io import StringIO

# Some useful static variable(s)
MARKER = '\n\n'  # This string occurs between the different data sections

class ASCCorrelator:
    def __init__(self,
                 file_path: str):
        """Creates an ASCCorrelator class using data from an asc file generated
            by the ALV-7004 correlator. Stores the data as three pandas
            dataframes or None, depending on which section of data may be missing

            Parameters
            ----------
            file_path: str
                Path of the asc file of interest
        """
        # Initialize the variables which will hold the various sections of data
        self.correlation = None
        self.count_rate = None
        self.instrument = None

        # Start reading the asc file (apparently encoded in latin-1)
        with open(file_path, mode='r', encoding='latin-1') as data_file:
            # Break up text file into sections which different data
            separated_data = (data_file.read()).split(MARKER)

            # Read each individual section of data in the asc file
            for data_string in separated_data:
                if 'Correlation' in data_string:
                    # Remove the Correlation header from data_string
                    temp_string = data_string.replace('"Correlation"\n', '') \
                        .replace('"Correlation (Multi, Averaged)"\n', '')

                    # Read temp_string as a csv by using StringIO
                    self.correlation = pd.read_csv(StringIO(temp_string),
                                                   sep='\t',
                                                   lineterminator='\n')

                elif 'Count Rate' in data_string:
                    # Remove the string '"Count Rate"\n' from data_string
                    temp_string = data_string.replace('"Count Rate"\n', '')

                    # Read temp_string as a csv by using StringIO
                    self.count_rate = pd.read_csv(StringIO(temp_string),
                                                  sep='\t',
                                                  lineterminator='\n',
                                                  usecols=[0, 1],
                                                  names=['Time [s]',
                                                         'Count rate [kHz]'])

                elif 'ALV-7004/USB-FAST' in data_string:
                    # Remove the header string and any spaces
                    temp_string = data_string.replace('ALV-7004/USB-FAST\n',
                                                      '')
                    temp_string = temp_string.replace(' ', '')

                    # Read temp_string as a csv by using StringIO
                    self.instrument = pd.read_csv(StringIO(temp_string),
                                                  sep=':\t',
                                                  lineterminator='\n',
                                                  names=['Parameter', 'Value'])
