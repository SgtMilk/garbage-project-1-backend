from matplotlib.pyplot import imread
from ml import predict

if __name__ == "__main__":
    picture = imread('./ml/data/source/biological/biological5.jpg')
    print(predict(picture))
