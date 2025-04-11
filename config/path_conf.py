import os

RAW_DIR = 'artifacts/raw'
RAW_FILE = os.path.join(RAW_DIR, 'raw.csv')
TRAIN_DATA_FILE = os.path.join(RAW_DIR, 'train.csv')
TEST_DATA_FILE = os.path.join(RAW_DIR, 'test.csv')

CONFIG_PATH = 'config/conf.yaml'

PROCESSED_DIR = 'artifacts/processed'
PROCESSED_TRAIN_FILE = os.path.join(PROCESSED_DIR, 'processed_train.csv')
PROCESSED_TEST_FILE = os.path.join(PROCESSED_DIR, 'processed_test.csv')
PROCESSED_TRAIN_TARGET_FILE = os.path.join(PROCESSED_DIR, 'processed_train_target.csv')
PROCESSED_TEST_TARGET_FILE = os.path.join(PROCESSED_DIR, 'processed_test_target.csv')

MODEL_DIR = 'artifacts/model'
MODEL_FILE = os.path.join(MODEL_DIR, 'model.joblib')
SCALER_FILE = os.path.join(MODEL_DIR, 'scalar.joblib')