from src.data_ingestion import DataIngestion
from src.data_preprocessing import DataPreprocessor
from src.model_traning import ModelTrainer
from config.path_conf import CONFIG_PATH, PROCESSED_TEST_FILE, PROCESSED_TRAIN_FILE, TEST_DATA_FILE, TRAIN_DATA_FILE
from utils.common_functions import get_config


if __name__ == "__main__":
    # data ingestion 
    di = DataIngestion(get_config(CONFIG_PATH))
    di.run()


    # data preprocessing
    preprocessor = DataPreprocessor(TRAIN_DATA_FILE, TEST_DATA_FILE)
    preprocessor.preprocess()

    # model training
    model_trainer = ModelTrainer(PROCESSED_TRAIN_FILE, PROCESSED_TEST_FILE)
    model_trainer.run()
    
