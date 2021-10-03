from torch.optim import SGD
import torch
from torch import save
from torch.nn import CrossEntropyLoss
from ml.model import Model
import numpy as np
import matplotlib.pyplot as plt
import time
import os


class Net:
    def __init__(self):
        self.model = Model()
        self.optimizer = SGD(self.model.parameters(), lr=0.001, momentum=0.9)
        self.loss_func = CrossEntropyLoss()

        gpu = torch.cuda.is_available()
        if gpu:
            self.model = self.model.to(device='cuda')

        self.weights_train = None
        self.loss_train = None
        self.loss_validation = None
        self.hist = None

        # getting the right file name
        destination_folder = os.path.abspath('./ml/model/models')
        self.save_file = os.path.join(destination_folder, "model.hdf5")

    def train(self, epochs: int, dataset, validation_split: float):
        x, y = dataset.get_train()
        n = int(x.shape[0] * (1 - validation_split))
        x_train, y_train = x[:n], y[:n]
        x_validation, y_validation = x[n:], y[n:]

        self.hist = np.zeros((epochs, 2))
        start_time = time.time()

        for epoch in range(1, epochs + 1):

            # training
            y_predicted_train = self.model(x_train)
            self.loss_train = self.loss_func(y_predicted_train, y_train)

            # validation
            y_predicted_validation = self.model(x_validation)
            self.loss_validation = self.loss_func(
                y_predicted_validation, y_validation)

            self.hist[epoch - 1] = np.array([self.loss_train, self.loss_validation])

            # optimizer
            self.optimizer.zero_grad()
            self.loss_train.backward()
            self.optimizer.step()

            # logging losses
            print(f"Epoch {epoch}, Training Loss: {self.loss_train.item()}, " +
                  f"Validation Loss: {self.loss_validation}")

        save(self.model.state_dict(), self.save_file)
        training_time = time.time() - start_time
        print("Training time: {}".format(training_time))

    def evaluate_training(self):
        plt.gcf().set_size_inches(22, 15, forward=True)

        plt.plot([value[0] for value in self.hist], label='training loss')
        plt.plot([value[1] for value in self.hist], label='validation loss')

        plt.legend(['Training Loss', 'Validation Loss'])

        plt.show()

    def evaluate(self, dataset):
        x, y, y_unscaled = dataset.get_test()
        predicted_y_test = self.model(x)

        # re-transforming to numpy
        predicted_y_test = predicted_y_test.detach().cpu().numpy()
        y = y.detach().cpu().numpy()
        y_unscaled = y_unscaled.detach().cpu().numpy()

        unscaled_predicted = dataset.normalizer.inverse_transform(
            predicted_y_test)

        assert predicted_y_test.shape == unscaled_predicted.shape
        assert predicted_y_test.shape == y_unscaled.shape

        real_mse = np.mean(np.square(y - predicted_y_test))
        scaled_mse = real_mse / (np.max(y) -
                                 np.min(y)) * 100
        print(f"scaled_mse_y: {scaled_mse}")

        real_mse = np.mean(np.square(y_unscaled - unscaled_predicted))
        scaled_mse = real_mse / (np.max(y_unscaled) -
                                 np.min(y_unscaled)) * 100
        print(f"scaled_mse_u_unscaled: {scaled_mse}")

        plt.gcf().set_size_inches(22, 15, forward=True)

        plt.plot(y[-1], label='real', marker='o')
        plt.plot(predicted_y_test[-1], label='predicted', marker='o')

        plt.legend(['Real', 'Predicted'])

        plt.show()

    def save(self):
        torch.save(self.model.state_dict(), self.save_file)

    def load(self):
        self.model = torch.load(self.save_file)
