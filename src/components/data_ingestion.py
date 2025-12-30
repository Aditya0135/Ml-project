# here we will feed data to our model for training and testing
import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass
"""
this class wil configure the data ingestion component 
It will define things like where to store raw data
where to store test data where to save training path etc
"""
# this will allow to define class variable without using init
@dataclass
class DataIngestionConfig:
    train_data_path: str=os.path.join('artifacts','train.csv')
    test_data_path: str=os.path.join('artifacts','test.csv')
    raw_data_path: str=os.path.join('artifacts','data.csv')

# if you have a calls having fun+car prefer init
class dataIngestion:
    """
    Read dataset -> make train,test,raw csv and folders -> return train test paths
    """
    # initialise the paths by this constructor
    def __init__(self):
        self.ingestion_config= DataIngestionConfig()

    # ingest data from local/remote source and make required directories
    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion component or method")
        try:
            df=pd.read_csv('notebook\data\stud.csv')
            logging.info("Read the dataset as dataframe")

            #now let us make directories(folders) for our train,test,raw data
            # test data directory
            os.makedirs(os.path.dirname(self.ingestion_config.test_data_path),exist_ok=True)# this will prevent delete and remaking new folder every time
            # saving our raw data as csv    
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            logging.info("Train test split initiated")
            train_set,test_set= train_test_split(df, test_size=0.2, random_state=42)
            
            # make and store the csvs' for train and test data
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)
            logging.info("Ingestion of the data is completed")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
            )
        except Exception as e:
            raise CustomException(e,sys)

if __name__=="__main__":
    obj=dataIngestion()
    obj.initiate_data_ingestion()