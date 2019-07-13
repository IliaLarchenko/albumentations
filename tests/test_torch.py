import numpy as np
import torch

import albumentations as A
from albumentations.pytorch.transforms import ToTensor


def test_torch_to_tensor_augmentations(image, mask):
    aug = ToTensor(image_dtype=torch.float32, mask_dtype=torch.float32)
    data = aug(image=image, mask=mask, force_apply=True)
    assert data['image'].dtype == torch.float32
    assert data['mask'].dtype == torch.float32


def test_torch_to_tensor_one_hot():
    image = np.zeros((512,512,3))
    mask = np.randint(0,10, (512,512))

    aug = ToTensor(image_dtype=torch.float32, mask_dtype=torch.float32, mask_one_hot_channels=10)
    data = aug(image=image, mask=mask)
    assert data['image'].dtype == torch.float32
    assert data['mask'].shape == [10,512,512]


def test_additional_targets_for_totensor():
    aug = A.Compose(
        [ToTensor(mask_one_hot_channels=4)], additional_targets={'image2': 'image', 'mask2': 'mask'})

    for i in range(10):
        image1 = np.random.randint(low=0, high=256, size=(100, 100, 3), dtype=np.uint8)
        image2 = image1.copy()
        mask1 = np.random.randint(low=0, high=256, size=(100, 100, 4), dtype=np.uint8)
        mask2 = mask1.copy()
        res = aug(image=image1, image2=image2, mask=mask1, mask2=mask2)
        assert np.array_equal(res['image'], res['image2'])
        assert np.array_equal(res['mask'], res['mask2'])
