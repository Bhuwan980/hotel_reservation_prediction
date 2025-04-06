import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import logging
import os
import joblib
from config.path_conf import PROCESSED_TRAIN_FILE, PROCESSED_TEST_FILE, MODEL_FILE

logger = logging.getLogger(__name__)

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

    def load_data(self):
        logger.info("Loading processed training and testing data.")
        try:
            # Load training and testing data
            self.df_train = pd.read_csv(self.train_file)
            self.df_test = pd.read_csv(self.test_file)

            # Extract the target variable 'booking_status'
            self.y_train = self.df_train.pop('booking_status')
            self.y_test = self.df_test.pop('booking_status')

            # The target is removed from the feature set in both train and test data
            self.X_train = self.df_train
            self.X_test = self.df_test

            logger.info("Data loaded successfully.")
        except Exception as e:
            logger.error("Error loading data: %s", e)
            raise Exception(f"Failed to load data: {e}")

    def preprocess_data(self):
        logger.info("Preprocessing data: scaling features.")
        try:
            # Scale the data using StandardScaler
            scaler = StandardScaler()
            self.X_train = scaler.fit_transform(self.X_train)
            self.X_test = scaler.transform(self.X_test)

            logger.info("Data preprocessing complete.")
        except Exception as e:
            logger.error("Error preprocessing data: %s", e)
            raise Exception(f"Failed to preprocess data: {e}")

    def train_model(self):
        logger.info("Training the model.")
        try:
            # Train a RandomForestClassifier
            model = RandomForestClassifier(random_state=self.random_state)
            model.fit(self.X_train, self.y_train)
            self.model = model
            logger.info("Model training complete.")
        except Exception as e:
            logger.error("Error training model: %s", e)
            raise Exception(f"Failed to train model: {e}")

    def evaluate_model(self):
        logger.info("Evaluating model performance.")
        try:
            # Make predictions on the test set
            y_pred = self.model.predict(self.X_test)

            # Calculate accuracy and generate a classification report
            accuracy = accuracy_score(self.y_test, y_pred)
            report = classification_report(self.y_test, y_pred)

            logger.info("Model evaluation complete.")
            logger.info(f"Accuracy: {accuracy}")
            logger.info("Classification Report:")
            logger.info(report)

        except Exception as e:
            logger.error("Error evaluating model: %s", e)
            raise Exception(f"Failed to evaluate model: {e}")

    def save_model(self):
        """ Save the trained model using joblib """
        try:
            # Ensure the directory exists
            model_dir = os.path.dirname(MODEL_FILE)
            if not os.path.exists(model_dir):
                os.makedirs(model_dir)  # Create the directory if it doesn't exist

            # Save the trained model using joblib
            joblib.dump(self.model, MODEL_FILE)
            logger.info(f"Model saved to {MODEL_FILE}.")
        except Exception as e:
            logger.error("Error saving model: %s", e)
            raise Exception(f"Failed to save model: {e}")

    def run(self):
        try:
            # Load and preprocess the data
            self.load_data()
            self.preprocess_data()

            # Train the model
            self.train_model()

            # Evaluate the model
            self.evaluate_model()

            # Save the trained model
            self.save_model()
            
        except Exception as e:
            logger.error(f"Error in model training process: {e}")
            raise Exception(f"Failed to complete the model training process: {e}")


if __name__ == '__main__':

    # Initialize and run the model trainer
    model_trainer = ModelTrainer(PROCESSED_TRAIN_FILE, PROCESSED_TEST_FILE)
    model_trainer.run()