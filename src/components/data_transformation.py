# Do feature engineering, data cleaning,covert categorical features to numerical etc...
import sys
import os
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer #used to create pipeline fro all data transformation things
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', "preprocessor.pkl")
    #A pickle file is a file that stores a Python object in binary form so you can load it back later.
    # Pickle file = stored / preserved object
    # Fresh object → usable in memory
    # Pickle it → sealed in a jar (file)
    # Unpickle → same object comes back, ready to use

class DataTransformation:
    # 1. Initialise data config object
    def __init__(self):
        self.data_transform_config =DataTransformationConfig()
    
    #2. make you data transformer
    def get_data_transformer_object(self):
        """
        This function is responsible for data transformation
        1. separate num and cat columns
        2. make objects for the pipeline by defining task and method chosen
        3. define your preprocessor by respectively joining column types with their dedicated pipeline
        """
        try:
            numerical_columns =["writing_score", "reading_score"]
            categorical_columns =[
                'gender',
                'race_ethnicity',
                'parental_level_of_education', 
                'lunch',
                'test_preparation_course',
                ]
            
            num_pipeline = Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler())
                ]
            )

            cat_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder",OneHotEncoder()),
                    ("scaler", StandardScaler(with_mean=False))
                ]
            )
            logging.info(f"Numerical columns {numerical_columns}")
            logging.info(f"Categorical columns {categorical_columns}")

            preprocessor = ColumnTransformer(
                [
                    ("numerical_pipeline", num_pipeline, numerical_columns),
                    ("categorical_pipeline", cat_pipeline, categorical_columns)
                ]
            )
            return preprocessor
        except Exception as e:
            raise CustomException(e, sys)
        
    def initialize_data_transformation(self, train_path, test_path):
        try:
            # 1. Read csv 
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)
            # 2. log
            logging.info("Read train and test data completed")

            logging.info("Obtaining pre processing object")

            # 3 initialize preprocessor obj + X(features), y(o/p)
            preprocessing_obj = self.get_data_transformer_object()
            target_column_name="math_score"
            numerical_columns =["writing_score", "reading_score"]

            # 4. X and y for train and test data
            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            # 5. apply preprocessor obj and fit train_i/p and transform i/p_test
            logging.info(f"Applying preprocessing object on training dataframe and test data")

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info(f"Saved preprocessing object")

            save_object(
                file_path=self.data_transform_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )
            return(
                train_arr,
                test_arr,
                self.data_transform_config.preprocessor_obj_file_path,
            )
        except Exception as e:
            raise CustomException(e, sys)