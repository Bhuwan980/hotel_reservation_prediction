import os
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.preprocessing import OrdinalEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from .logger import get_logger
from config.path_conf import TRAIN_DATA_FILE, TEST_DATA_FILE, PROCESSED_TRAIN_FILE, PROCESSED_TEST_FILE

logger = get_logger(__name__)

class CustomException(Exception):
    def __init__(self, message):
        super().__init__(message)

class DataPreprocessor:
    def __init__(self, train_file, test_file=None, test_size=0.2, random_state=42, n_neighbors=5):
        self.train_file = train_file
        self.test_file = test_file
        self.test_size = test_size
        self.random_state = random_state
        self.n_neighbors = n_neighbors

        self.df = None
        self.df_test = None
        self.target_col = "booking_status"
        self.cat_cols = []
        self.num_cols = []

        self.scaler = StandardScaler()
        self.knn_imputer = KNNImputer(n_neighbors=self.n_neighbors)
        self.ordinal_encoder = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)

    def load_data(self):
        try:
            self.df = pd.read_csv(self.train_file).drop(columns=["Unnamed: 0"], errors="ignore")
            if self.test_file:
                self.df_test = pd.read_csv(self.test_file).drop(columns=["Unnamed: 0"], errors="ignore")
            logger.info("Data loaded successfully.")
        except Exception as e:
            raise CustomException(f"Error loading data: {e}")

    def identify_columns(self):
        self.cat_cols = self.df.select_dtypes(include=["object"]).columns.tolist()
        self.num_cols = self.df.select_dtypes(include=["int64", "float64"]).columns.tolist()

        if self.target_col in self.cat_cols:
            self.cat_cols.remove(self.target_col)
        if self.target_col in self.num_cols:
            self.num_cols.remove(self.target_col)

        logger.info(f"Categorical columns: {self.cat_cols}")
        logger.info(f"Numerical columns: {self.num_cols}")

    def handle_missing_values(self):
        try:
            for col in self.cat_cols:
                mode_value = self.df[col].mode()[0]
                self.df[col] = self.df[col].fillna(mode_value)
                if self.df_test is not None:
                    self.df_test[col] = self.df_test[col].fillna(mode_value)

            self.df[self.num_cols] = self.knn_imputer.fit_transform(self.df[self.num_cols])
            if self.df_test is not None:
                self.df_test[self.num_cols] = self.knn_imputer.transform(self.df_test[self.num_cols])

            logger.info("Missing values handled successfully.")
        except Exception as e:
            raise CustomException(f"Error handling missing values: {e}")

    def encode_categorical_variables(self):
        try:
            self.df[self.cat_cols] = self.ordinal_encoder.fit_transform(self.df[self.cat_cols])
            if self.df_test is not None:
                self.df_test[self.cat_cols] = self.ordinal_encoder.transform(self.df_test[self.cat_cols])

            logger.info("Categorical variables encoded with OrdinalEncoder successfully.")
        except Exception as e:
            raise CustomException(f"Error encoding categorical variables: {e}")

    def scale_features(self):
        try:
            self.df[self.num_cols] = self.scaler.fit_transform(self.df[self.num_cols])
            if self.df_test is not None:
                self.df_test[self.num_cols] = self.scaler.transform(self.df_test[self.num_cols])

            logger.info("Features scaled successfully.")
        except Exception as e:
            raise CustomException(f"Error scaling features: {e}")

    def save_preprocessed_data(self):
        try:
            os.makedirs(os.path.dirname(PROCESSED_TRAIN_FILE), exist_ok=True)
            self.df.to_csv(PROCESSED_TRAIN_FILE, index=False)

            if self.df_test is not None:
                os.makedirs(os.path.dirname(PROCESSED_TEST_FILE), exist_ok=True)
                self.df_test.to_csv(PROCESSED_TEST_FILE, index=False)

            logger.info("Preprocessed data saved successfully.")
        except Exception as e:
            raise CustomException(f"Error saving preprocessed data: {e}")

    def preprocess(self):
        self.load_data()
        self.identify_columns()
        self.handle_missing_values()
        self.encode_categorical_variables()
        self.scale_features()
        self.save_preprocessed_data()
        logger.info("Preprocessing pipeline completed successfully.")

if __name__ == "__main__":
    try:
        preprocessor = DataPreprocessor(TRAIN_DATA_FILE, TEST_DATA_FILE)
        preprocessor.preprocess()
    except CustomException as e:
        logger.error(f"Unexpected Error: {e}")