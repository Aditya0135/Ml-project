# here we will perform actual model training using various algorithms
# Basic Import
import numpy as np
import pandas as pd
import os
import sys
from dataclasses import dataclass

# Modelling
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor,AdaBoostRegressor
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression, Ridge,Lasso
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.model_selection import RandomizedSearchCV
from xgboost import XGBRegressor
import warnings
from sklearn.metrics import r2_score

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object,evaluate_models

@dataclass
class modelTrainerConfig:
    model_trainer_config = os.path.join('artifacts','model.pkl')
    
class modelTrainer:
    def __init__(self):
        self.model_trainer_config = modelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("Splitting training and test data")
            X_train,y_train,X_test,y_test=(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1],
            )
            models={
                "Linear Regression": LinearRegression(),
                "Lasso": Lasso(),
                "Ridge": Ridge(),
                "K-Neighbors Regressor": KNeighborsRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Random Forest Regressor": RandomForestRegressor(),
                "XGBRegressor": XGBRegressor(), 
                "AdaBoost Regressor": AdaBoostRegressor()
            }
            # Hyperparameter tuning
            params={
                "Decision Tree":{
                    'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                },
                "Random Forest Regressor":{
                    'n_estimators':[8,16,32,64,128,256]
                },
                "K-Neighbors Regressor":{
                    'n_neighbors':[5,7,9,11],
                    'weights':['uniform','distance'],
                    'algorithm':['auto','ball_tree','kd_tree']
                },
                "Linear Regression":{},
                "Lasso":{},
                "Ridge":{},
                "XGBRegressor":{
                    'learning_rate':[0.1,0.01,0.05,0.15],
                    'max_depth':[3,4,5,6],
                    'n_estimators':[50,100,200,300]
                },
                "AdaBoost Regressor":{
                    'n_estimators':[50,100,200,300],
                    'learning_rate':[0.1,0.01,0.05,0.5]
                }

            }
            model_report:dict = evaluate_models(X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,
                                               models=models,params=params)
            
            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]

            if best_model_score < 0.6:
                raise CustomException("No best model found")
            logging.info("Best model found on training and test dataset")

            save_object(file_path=self.model_trainer_config.model_trainer_config,
                        obj=best_model)

            predicted = best_model.predict(X_test)
            r2_square= r2_score(y_test,predicted)
            return r2_square 




        except Exception as e:
            raise CustomException(e,sys)
