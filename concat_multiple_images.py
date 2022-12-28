import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

def concat(title = '',**images):
    """PLot images in one row."""
    n = len(images)
    image_list = [*images.values()]
    space_count = 0
    concat_img = np.ones((image_list[0].shape[0], (image_list[0].shape[1] * n) + (n - 1) * 50, 3), dtype='uint8') * 255

    for i, (name, image) in enumerate(images.items()):
        concat_img[:, i * image.shape[1] + (space_count * 50): (i+1) * image.shape[1] + (space_count * 50), :] = image
        space_count += 1

    return concat_img

img = cv2.imread('c200amg.png')

img_c = concat(
    resim_1 = img,
    resim_2 = img,
    resim_3 = img,
    resim_4 = img,
)

plt.imshow(img_c)
plt.show()
print("a")