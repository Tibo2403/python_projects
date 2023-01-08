import glob
import panda as pd
list_csv = glob('*.csv')
list_csv:['source1.csv','source2.csv','source3.csv']
list_json = glob('*.json')

def extract_from_csv(file_to_process):
    dataframe = pd.read_csv(file_to_process)
    return dataframe

def extract_from_json(file_to_process):
    dataframe = pd.read_json(file_to_process, lines=True)
    return dataframe

df = extract_from_csv('source1.csv')
df = extract_from_json('source1.csv')

def extract():
    # create an empty data frame to hold extracted data
    extracted_data = pd.DataFrame(columns=['name','height','weight'])

    #process all csv files
    for csvfile in glob.glob("*.csv"):
        extracted_data = extracted_data.append(extract_from_csv(csvfile), ignore_index=True)

    #process all json files
    for jsonfile in glob.glob("*.json"):
        extracted_data = extracted_data.append(extract_from_json(jsonfile),ignore_index=True)

    return extracted_data

extracted_data = pd.DataFrame(columns=['name','height','weight'])

def transform(data):
    #convert height is in inches to millimeter
    #Convert inches to meters and round off to two decimals(one inch is 0.0254 meters)
    data['height'] = round(data.height * 0.0254,2)

    #Convert pounds to kilograms and round off to two decimals (one pound is 0.45359237 kilograms)
    data['weight'] = round(data.weight * 0.45359237,2)

def load(targetfile, data_to_load):
    data_to_load.to_csv(targetfile)

    targetfile = "transformed_data.csv"
    load(targetfile, transformed_data)

from datetime import datetime

def log(message):
    timestamp_format = '%Y-%h-%d-%H:%M:%S'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    with open("logfile.txt", "a") as f:
        f.write(timestamp + ',' + message + '\n')

log("ETL Job Started")
log("Transform Job Started")
transformed_data = transform(extracted_data)
log("Transform Job Ended")
log("Load Job Started")
load(targetfile, transformed_data)
log("Load Job Ended")
log("ETL Job Ended")