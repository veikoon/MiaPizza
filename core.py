from setting import datafile
import json

#### Functions ####

# Load database function
def load():
    file = open(datafile,'r')
    data = json.load(file)
    file.close()
    return data
    
# Save database function
def save(data):
    file = open(datafile,'w')
    json.dump(data, file, indent=4)
    file.close()
