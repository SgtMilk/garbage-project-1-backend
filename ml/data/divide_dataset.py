import os
from shutil import copyfile


def divide_dataset():
    source_folder = os.path.abspath("./source")
    base_folder = os.path.abspath("./sorted")
    train_folder = os.path.join(base_folder, "train")
    validation_folder = os.path.join(base_folder, "validation")
    test_folder = os.path.join(base_folder, "test")

    if not os.path.exists(base_folder):
        os.mkdir(base_folder)
    if not os.path.exists(train_folder):
        os.mkdir(train_folder)
    if not os.path.exists(validation_folder):
        os.mkdir(validation_folder)
    if not os.path.exists(test_folder):
        os.mkdir(test_folder)

    validation_split = 0.1
    test_split = 0.1

    for folder in os.listdir(source_folder):
        folder_path = os.path.join(source_folder, folder)
        pictures = os.listdir(folder_path)

        split_train = int(len(pictures) * (1 - validation_split - test_split))
        split_validation = int(len(pictures) * (1 - test_split))

        path = os.path.join(train_folder, folder)
        if not os.path.exists(path):
            os.mkdir(path)
        copy_pictures = pictures[:split_train]
        for picture in copy_pictures:
            copyfile(os.path.join(folder_path, picture), os.path.join(path, picture))

        path = os.path.join(validation_folder, folder)
        if not os.path.exists(path):
            os.mkdir(path)
        copy_pictures = pictures[split_train:split_validation]
        for picture in copy_pictures:
            copyfile(os.path.join(folder_path, picture), os.path.join(path, picture))

        path = os.path.join(test_folder, folder)
        if not os.path.exists(path):
            os.mkdir(path)
        copy_pictures = pictures[split_validation:]
        for picture in copy_pictures:
            copyfile(os.path.join(folder_path, picture), os.path.join(path, picture))


if __name__ == "__main__":
    divide_dataset()
