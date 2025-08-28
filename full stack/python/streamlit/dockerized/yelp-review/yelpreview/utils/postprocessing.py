"""Class to save the trained model with timestamp to configured location"""
import datetime
import os
import pickle


class ModelSaving(object):
    
    @staticmethod
    def get_current_timestamp():
        now = datetime.datetime.now()
        return now.strftime("%Y%m%d_%H%M%S")

    @staticmethod
    def save_model_with_timestamp(vectorizer, model, output_config):
        filename = ModelSaving.get_current_timestamp() + '_LogReg' + '.pickle'
        filepath = os.path.join(output_config, filename)
        with open(filepath, 'wb') as outputfile:
            pickle.dump((vectorizer, model), outputfile)
        return print('Saved vectorizer and model to pickle file: ', filepath)

if __name__ == '__main__':
    print(ModelSaving.get_current_timestamp())