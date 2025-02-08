"""Dataloader class"""

import pandas as pd
from sklearn import model_selection
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np


class DataLoader:
    """Data Loader class"""

    @staticmethod
    def load_data(data_config):
        """Loads dataset from path"""
        df = pd.read_csv(data_config.path) # data_config will have .path attribute
        return df

    @staticmethod
    def preprocess_data(data_config, dataset = None): #dataset -> df
        """ Preprocess and splits into training and test"""
        x = dataset[data_config.x]
        y = dataset[data_config.y]
        test_size = data_config.test_size
        random_state = data_config.random_state
        # splitting
        x_train, x_test, y_train, y_test = \
            model_selection.train_test_split(x, y, 
                                             test_size=test_size, 
                                             random_state=random_state)
        # vectorizing
        vectorizer = CountVectorizer(ngram_range = data_config.ngram_range, 
                                     min_df = data_config.min_df)
        # fit_transform on training texts: from text to sparse frequency fector embeddings
        # transform on test texts: using vector dimension from training set
        # Extract token counts out of raw text documents using the vocabulary
        # fitted with fit or the one provided to the constructor.
        # vectorizer.vocabulary_: A mapping of terms to feature indices.
        X_train = vectorizer.fit_transform(x_train)
        X_test = vectorizer.transform(x_test)
        Y_train = np.array(y_train)
        Y_test = np.array(y_test)

        return x, y, x_train, x_test, y_train, y_test, X_train, X_test, Y_train, Y_test, vectorizer
