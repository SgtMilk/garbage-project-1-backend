from torch.nn import Linear, Conv2d, MaxPool2d, Module
from torch.nn.functional import relu
from torch import flatten


class Model(Module):
    def __init__(self):
        super().__init__()
        self.conv1 = Conv2d(3, 6, 5)
        self.conv2 = Conv2d(6, 16, 5)
        self.pool = MaxPool2d(2, 2)
        self.linear1 = Linear(16 * 5 * 5, 120)
        self.linear2 = Linear(120, 84)
        self.linear3 = Linear(84, 12)

    def forward(self, x):
        x = self.pool(relu(self.conv1(x)))
        x = self.pool(relu(self.conv2(x)))
        x = flatten(x, 1)
        x = relu(self.linear1(x))
        x = relu(self.linear2(x))
        x = self.linear3(x)
        return x
    