"""Trainer class"""


class LogisticRegressionTrainer():
    def __init__(self, model, X_train, Y_train):
        self.model = model
        self.X_train = X_train
        self.Y_train = Y_train
    def train(self):
        self.model.fit(self.X_train, self.Y_train)