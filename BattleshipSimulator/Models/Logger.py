import csv
import os

class CSVLogger:
    def __init__(self, filename):
        self.filename = filename
        self.file = open(self.filename, 'w', newline='')
        self.writer = csv.writer(self.file)
        # If the file is new, we'll write the headers later, when we get the first dictionary.

    def log(self, data):
        # If the file is new (or empty), write the headers (dictionary keys)
        if os.path.getsize(self.filename) == 0:
            self.writer.writerow(data.keys())
            self.flush()
        
        # Write the dictionary values
        self.writer.writerow(data.values())

    def flush(self):
        """Ensures that data is written to the file."""
        self.file.flush()

    def close(self):
        self.flush()
        """Closes the file. Make sure to call this when you're done logging."""
        self.file.close()
