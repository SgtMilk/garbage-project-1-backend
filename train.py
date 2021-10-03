from ml.data import get_images
from ml import Net

if __name__ == "__main__":
    dataset = get_images()
    print("beep")
    net = Net()
    net.train(100, dataset, 0.1)
