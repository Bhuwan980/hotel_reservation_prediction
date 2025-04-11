import pandas as pd
import joblib
import logging
import os
import json
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

from config.path_conf import PROCESSED_TRAIN_FILE, PROCESSED_TEST_FILE,MODEL_FILE, SCALER_FILE, MODEL_DIR


METRICS_FILE = "artifacts/models/metrics.json"
FEATURE_IMPORTANCE_PLOT = "artifacts/models/feature_importance.png"

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class ModelTrainer:
    def __init__(self, train_file, test_file, test_size=0.2, random_state=45):
        self.train_file = train_file
        self.test_file = test_file
        self.test_size = test_size
        self.random_state = random_state
        self.df_train = None
        self.df_test = None
        self.y_train = None
        self.y_test = None
        self.X_train = None
        self.X_test = None
        self.model = None
        self.scaler = None
        self.features = None

    def load_data(self):
        logger.info("Loading processed training and testing data.")
        try:
            self.df_train = pd.read_csv(self.train_file)
            self.df_test = pd.read_csv(self.test_file)

            assert not self.df_train.isnull().any().any(), "Training data contains NaNs"
            assert not self.df_test.isnull().any().any(), "Test data contains NaNs"

            self.y_train = self.df_train.pop('booking_status')
            self.y_test = self.df_test.pop('booking_status')

            self.df_train.drop(columns=['Booking_ID'], inplace=True)
            self.df_test.drop(columns=['Booking_ID'], inplace=True)

            self.X_train = self.df_train
            self.X_test = self.df_test
            self.features = self.df_train.columns.tolist()

            logger.info("Data loaded and validated successfully.")
        except Exception as e:
            logger.error("Error loading data: %s", e)
            raise Exception(f"Failed to load data: {e}")

    def preprocess_data(self):
        logger.info("Preprocessing data: scaling features.")
        try:
            self.scaler = StandardScaler()
            self.X_train = self.scaler.fit_transform(self.X_train)
            self.X_test = self.scaler.transform(self.X_test)
            os.makedirs(MODEL_DIR, exist_ok=True)
            joblib.dump(self.scaler, SCALER_FILE)
            logger.info("Scaler saved to disk.")
        except Exception as e:
            logger.error("Error preprocessing data: %s", e)
            raise Exception(f"Failed to preprocess data: {e}")

    def train_model(self):
        logger.info("Training the model.")
        try:
            model = RandomForestClassifier(random_state=self.random_state)
            model.fit(self.X_train, self.y_train)
            self.model = model
            logger.info("Model training complete.")
        except Exception as e:
            logger.error("Error training model: %s", e)
            raise Exception(f"Failed to train model: {e}")

    def save_model(self):
        try:
            os.makedirs(os.path.dirname(MODEL_FILE), exist_ok=True)
            joblib.dump(self.model, MODEL_FILE)
            logger.info(f"Model saved to {MODEL_FILE}.")
        except Exception as e:
            logger.error("Error saving model: %s", e)
            raise Exception(f"Failed to save model: {e}")

    def run(self):
        try:
            self.load_data()
            self.preprocess_data()
            self.train_model()
            self.save_model()
        except Exception as e:
            logger.error(f"Error in model training process: {e}")
            raise Exception(f"Failed to complete the model training process: {e}")


if __name__ == '__main__':
    trainer = ModelTrainer(PROCESSED_TRAIN_FILE, PROCESSED_TEST_FILE)
    trainer.run()