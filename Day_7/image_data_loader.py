import torch

RANDOM_SEED=42
RAND_GEN = torch.Generator().manual_seed(RANDOM_SEED)

from torch.utils.data import Dataset
class ImageDataset(Dataset):
    def __init__(self, path, transform=None, test_transform=None, mode=None):

        from pathlib import Path
        self.path = Path(path)

        import torchvision.transforms as transforms
        if transform is None:
            self.transform = transforms.Compose([
                    transforms.RandomRotation(10),
                    transforms.RandomHorizontalFlip(),
                    transforms.Resize((224, 224)),  # Resize images to a common size
                    transforms.CenterCrop((224, 224)),  # Center crop to ensure consistent size
                    transforms.ToTensor(),          # Convert images to tensors
                    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # Normalize the images
            ])
        else:
            self.transform = transform

        if test_transform is None:
            self.test_transform = transforms.Compose([
                    transforms.ToTensor(),          # Convert images to tensors
                    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # Normalize the images
            ])
        else:
            self.test_transform = test_transform

        from torchvision.datasets import ImageFolder
        self.data = ImageFolder(root=self.path, transform=self.transform)

        #from sklearn.model_selection import train_test_split
        #self.training_data, self.validation_data = train_test_split(self.img_data, test_size=0.1, random_state=42)

        from torch.utils.data import random_split
        self.train_data, self.validation_data, self.test_data = random_split(
                 self.data, lengths=[0.8, 0.1, 0.1], 
                 generator=RAND_GEN
        )

        from copy import deepcopy
        self.test_data = deepcopy(self.test_data)
        self.validate_data = deepcopy(self.validation_data)
        self.test_data.dataset.transform = self.test_transform
        self.validate_data.dataset.transform = self.test_transform

        self.mode = mode

    def __len__(self):
        return len(self._data_pivot)

    def __getitem__(self, idx):
        img, label = self._data_pivot[idx]
        return img, label

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, m):
        if m in ("train", "test", "validate"):
            self._data_pivot = getattr(self, f"{m}_data")
        else:
            self._data_pivot = self.data        

    @property
    def classes(self):
        return self._data_pivot.classes

    @property
    def idx_to_class(self):
        return {v: k for k, v in self._data_pivot.class_to_idx.items()}

    @property
    def class_to_idx(self):
        return self._data_pivot.class_to_idx

    @property
    def num_classes(self):
        return len(self._data_pivot.classes)

    @property
    def target_to_class(self):
        return {i: self.idx_to_class[v] for i, (k, v) in enumerate(self)}
