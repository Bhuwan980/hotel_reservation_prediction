

import os
import pandas as pd
from sklearn.model_selection import train_test_split
from config.path_conf import RAW_DIR, RAW_FILE, TRAIN_DATA_FILE, TEST_DATA_FILE, CONFIG_PATH
from .custom_exception import CustomException
from google.cloud import storage
from utils.common_functions import get_config
from .logger import get_logger


class DataIngestion:

    def __init__(self, config_file):
        try:
            self.logger = get_logger(__name__)
            self.data = config_file["data_ingestion"]
            self.bucket_name = self.data["bucket_name"]
            self.bucke_file_name = self.data["bucket_file_name"]
            self.train_ratio = self.data["train_ratio"]
        except CustomException as e:
            raise f"Config file could not found: {e}"

    def download_data_from_gcp(self):
        try:
            os.makedirs(RAW_DIR, exist_ok=True)
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.bucke_file_name)
            blob.download_to_filename(RAW_FILE)
            self.logger.info(f"CSV file is successfully downloaded to {RAW_FILE}")
            
        except CustomException as e:
            raise f"Could not able to download the file: {e}"
        
    def extract_data(self):
        try:
            if os.path.exists(RAW_FILE):
                df = pd.read_csv(RAW_FILE)
                train_data, test_data = train_test_split(df, test_size= 1 - self.train_ratio, random_state=42)
                train_data.to_csv(TRAIN_DATA_FILE)
                test_data.to_csv(TEST_DATA_FILE)

        except CustomException as e:
            raise f"Could not able to extract the data: {e}"
        

    def run(self):
        self.download_data_from_gcp()
        self.extract_data()

if __name__ == "__main__":
    di = DataIngestion(get_config(CONFIG_PATH))
    di.run()
