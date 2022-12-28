import os
import cv2
import numpy as np
import pydicom as pdc
import SimpleITK as sitk

def concat(path):
    os.chdir(path)
    row = 0
    column = 0

    img_list = [i for i in os.listdir(path) if i.endswith('.dcm')]
    if len(img_list) == 0:
        img_list = [i for i in os.listdir(path) if i.endswith('.png')]


    for i in img_list:

        i_ = i.split('_')

        if row < int(i_[1]):
            row = int(i_[1])
        
        if column < int(i_[3]):
            column = int(i_[3])

    

    if img_list[0].endswith('.dcm'):
        concat_img = np.zeros((row, column), dtype='uint16')
    elif img_list[0].endswith('.png'):
        concat_img = np.zeros((row, column,3), dtype='uint8')

    for i in img_list:
        if i.endswith('.png'):
            img = cv2.imread(i)

            img = cv2.resize(img, (img.shape[0], img.shape[1]), cv2.INTER_AREA)
            name = i.split('_')
            concat_img[int(name[0]):int(name[1]), int(name[2]):int(name[3]), :] = img
        elif i.endswith('.dcm'):
            img = pdc.dcmread(i).pixel_array
            img = cv2.resize(img, (img.shape[0], img.shape[1]), cv2.INTER_AREA)
            name = i.split('_')
            concat_img[int(name[0]):int(name[1]), int(name[2]):int(name[3])] = img

        
        save_path = path + '/../../'
        name = img_list[0].split('_')
        name = '_'.join(name[4:])
        if img_list[0].endswith('.dcm'):
            temp_dcm = sitk.GetImageFromArray(concat_img)
            sitk.WriteImage(temp_dcm, name)
        else:
            cv2.imwrite(save_path + name, concat_img)
        print(name)
                
    #return concat_img


# Örnek kullanım

path = r"D:\github_test\patch-unpatch-concat\patched_images"

for root, _, files in os.walk(path):
    for file in files:
        concat(root)
