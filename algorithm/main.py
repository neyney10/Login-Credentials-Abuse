'''
    Description: Program runner.
    Mode: Development [Debug].
    Dependencies:
        Python 3.5+ (3.8 is recommended).
            numpy
            pandas
            re
            logging
            user-agents 2.2.0
'''

from features import OSFamilyMacFeature, OSFamilyWindowsFeature, Top100PasswordFeature, Top3BeginAt100PasswordFeature, Top50PasswordFeature, UserAgentChromeFeature, UserAgentOperaFeature, UserAgentSafariFeature, UserAgentWindows10Chrome80Feature, UserAgentWindows10Firefox57Feature, Top3PasswordFeature
import pandas as pd
import numpy as np
import re
import logging # https://docs.python.org/3/howto/logging-cookbook.html#a-qt-gui-for-logging
from subsetting_method import DefaultSubsettingMethod, OSFamilySubsettingMethod, UsernameSubsettingMethod, BrowserFamilySubsettingMethod
from algorithm import Algorithm


## constants
TIME_INTERVAL = 2 # NOT USED YET
TIME_INTERVAL_UNITS = "hour" # NOT USED YET
NUMBER_OF_SUSBETS = 7
DATA_PATH = r'D:\temp\Akamai\datasets\SCRIPTS\generated2_ua_splitted.csv' #benign
GENERATED_DATA_PATH = r'D:\temp\Akamai\datasets\SCRIPTS\generated2_malicious_ua_splitted.csv' #mal

## program driver
def main():
    set_loggers()
    logger = logging.getLogger('main')
    logger.debug('Starting program')
    logger.debug('Session name: ' + 'DEBUG 2,00,000+100,000 ?-subsets | generated dataset 2')
    logger.debug('Reading data, data filepath: '+DATA_PATH)

    data = read_data(DATA_PATH, 2*1000*1000)
    data["IsMal"] = 0
    generated_data = read_data(GENERATED_DATA_PATH, 100*1000)
    generated_data["IsMal"] = 1
    data = data.append(generated_data)

    logger.debug("Data loaded succesfuly, number of rows loaded: "+str(len(data.index))+", mem usage: "+mem_usage(data))
    print(data.head())

    print(mem_usage(data))

    susbtMethod = BrowserFamilySubsettingMethod(NUMBER_OF_SUSBETS)  #OSFamilySubsettingMethod(NUMBER_OF_SUSBETS) #BrowserFamilySubsettingMethod(NUMBER_OF_SUSBETS) 
    algo = Algorithm(data, susbtMethod, [
        #OSFamilyMacFeature(),
        #OSFamilyWindowsFeature(),
        #UserAgentSafariFeature(),
        #UserAgentChromeFeature(),
        #UserAgentOperaFeature(),
        Top3PasswordFeature(),
        Top3BeginAt100PasswordFeature(),
        Top50PasswordFeature(),
        Top100PasswordFeature()
        ])

    logger.debug("Running the algorithm")

    algo.run()



def read_data(path, amount):
    data = pd.read_csv(path,
                        header=0,
                        names=[
                            "Time", 
                            "Username", 
                            "Password",
                            "Outcome",
                            "Browser Family",
                            "Browser Version",
                            "Device Family",
                            "Device Brand",
                            "Device Model",
                            "OS Family",
                            "OS Version"
                        ],
                        dtype={
                            'Time' : np.uint32,
                            'Username' : 'category',
                            'Password' : 'category',
                            'Outcome' : 'category',
                            "Browser Family" : 'category',
                            "Browser Version" : 'category',
                            "Device Family" : 'category',
                            "Device Brand" : 'category',
                            "Device Model" : 'category',
                            "OS Family" : 'category',
                            "OS Version" : 'category'
                        },
                        nrows=amount)
    return data


def set_loggers() -> None:
    logger =logging.getLogger('main')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    fh = logging.FileHandler('algorithm.log')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(sh)
    
def mem_usage(pandas_obj):
    if isinstance(pandas_obj,pd.DataFrame):
        usage_b = pandas_obj.memory_usage(deep=True).sum()
    else: # we assume if not a df it's a series
        usage_b = pandas_obj.memory_usage(deep=True)
    usage_mb = usage_b / 1024 ** 2 # convert bytes to megabytes
    return "{:03.2f} MB".format(usage_mb)


if __name__ == "__main__":
    main()

