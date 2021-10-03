import torch
from torch.autograd import Variable
from torchvision.transforms import Compose, Resize, ToTensor, Normalize

transforms = Compose(
    [ToTensor(),
     Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
     Resize((256, 256))])

classes = ("battery", "biological", "brown-glass", "cardboard", "clothes", "green-glass", "metal", "paper", "plastic",
           "shoes", "trash", "white-glass")


def predict(image):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = torch.load('./ml/models/model.hdf5')
    model.eval()

    image_tensor = transforms(image).float()
    image_tensor = image_tensor.unsqueeze_(0)
    input_var = Variable(image_tensor)
    input_var = input_var.to(device)
    output = model(input_var)
    index = output.data.cpu().numpy().argmax()
    return classes[index]
