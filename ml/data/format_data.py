from torchvision.datasets import ImageFolder
from torchvision.transforms import Compose, ToTensor, Normalize, Resize, RandomCrop, RandomHorizontalFlip
from torch.utils.data import DataLoader

classes = ("battery", "biological", "brown-glass", "cardboard", "clothes", "green-glass", "metal", "paper", "plastic",
           "shoes", "trash", "white-glass")


def get_images():
    transforms = Compose([Resize(256),
                          RandomCrop(224),
                          RandomHorizontalFlip(),
                          ToTensor(),
                          Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])
    loader = DataLoader(ImageFolder(root='./ml/data/source', transform=transforms), shuffle=True, batch_size=32)
    for data, target in loader:
        data = data.to('cuda')
        target = target.to('cuda')
    return loader
