from __future__ import print_function

import argparse
import logging
import os
import pickle
import warnings
import dask.dataframe as dd
import lightgbm as lgb
# import matplotlib.pyplot as plt
# import numpy as np
import pandas as pd
# import plotly.express as px
# import seaborn as sns
from colorama import Fore, Style, init
# from sklearn import metrics, tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import cross_val_score, train_test_split
# from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

warnings.filterwarnings('ignore')

init(autoreset=True)

# Custom formatter class to add colors


class CustomFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: Fore.BLUE,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.MAGENTA
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelno, Fore.WHITE)
        log_message = super().format(record)
        return f"{log_color}{log_message}{Style.RESET_ALL}"


# Set up logging
logger = logging.getLogger("colored_logger")
handler = logging.StreamHandler()
handler.setFormatter(CustomFormatter("- %(levelname)s - %(message)s"))

logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

path = 'dataset/super_crops_synth.csv'

models_folder = "models"
logger.info(f"Dataset: \033[1;94m{path}\033[0m")
df = pd.read_csv(path)

# Dask DataFrame
df = pd.read_csv(path)
# Converting Dask DataFrame to pandas for further operations
# df = df.compute()

# INSPECT
print(df.head())  # csv head
print(df.shape)  # Number of columns
print(df.columns)  # Column names
print(df['crop'].unique())  # get a column
print(df.dtypes)  # Column datatype
print(df['crop'].value_counts())  # Number of crop occurences
