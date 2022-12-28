import os
import cv2
import pydicom as pdc
import SimpleITK as sitk

def slice_with_overlay(img_name, stride_x, stride_y, out, path_to_save='./', path_to_read='./'):
    """
        stride_x kadar enine stride_y kadar boyuna bindirme yapar. 
    """

    stride_x = out - stride_x
    stride_y = out - stride_y
    os.chdir(path_to_read)
    print(os.getcwd())
    print(f'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>{img_name} görüntüsü parçalanıyor<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')

    k = img_name
    is_mask = True
    if img_name.endswith('.dcm'):
        is_mask = False
    else:
        is_mask = True

    if is_mask:
        img = cv2.imread(k)  # etiket dosyaları için
    else:
        img = pdc.dcmread(k).pixel_array
        # img=pdc.read_file(dicoms[0],force=True)
        # img.file_meta.TransferSyntaxUID = pdc.uid.ImplicitVRLittleEndian  # or whatever is the correct transfer syntax for the file
        # img.SamplesPerPixel = 1
        # img = img.pixel_array

        # img = pd.dcmread(k).pixel_array #dicom dosyaları için
  
    os.chdir(path_to_save)
    if os.path.exists(k[:-4]):
        os.chdir(k[:-4])
    else:
        os.mkdir(k[:-4])
        os.chdir(k[:-4])


    row = img.shape[0]
    col = img.shape[1]

    outer = (row // out) * out
    inner = (col // out) * out

    for r in range(0, outer, stride_y):
        for c in range(0, inner + 1, stride_x):
            #satır boyutundan büyük çıkarsa satır boyutunu sınır alarak geriye out kadar geriden alır
            if r + out > row:

                #sütun boyutundan büyük çıkarsa sütun boyutunu sınır alarak geriye out kadar geriden alır
                if c + out > col:

                    # print(row - out, row, col - out, col)

                    if is_mask:
                        # #etiketleri kayıtederken
                        cv2.imwrite(str(row-out) + '_' + str(row) + '_' + str(col-out) +'_' + str(col) + '_' + k, img[row-out:row, col - out:col, :])

                    else:
                        # dicom dosyalarını kayıt ederken
                        temp_dcm = img[row-out:row, col - out:col]
                        temp_dcm = sitk.GetImageFromArray(temp_dcm)
                        sitk.WriteImage(temp_dcm, str(row-out) + '_' + str(row) + '_' + str(col-out) + '_' + str(col) + '_' + k)

                    break
                    
                else:
                    #print(row - out, row, c, c + out)

                    if is_mask:
                        # #etiketleri kayıtederken
                        cv2.imwrite(str(row-out) + '_' + str(row) + '_' + str(c) + '_' + str(c + out) + '_' + k, img[row - out : row, c : c + out, :])

                    else:
                        # dicom dosyalarını kayıt ederken
                        temp_dcm = img[row - out:row, c : c + out]
                        temp_dcm = sitk.GetImageFromArray(temp_dcm)
                        sitk.WriteImage(temp_dcm, str(row-out) + '_' + str(row) + '_' + str(col-out) + '_' + str(col) + '_' + k)

            elif c + out > col:

                #print(r, r + out, col - out, col)
                if is_mask:
                        # #etiketleri kayıtederken
                        cv2.imwrite(str(r) + '_' + str(r + out) + '_' + str(col - out) + '_' + str(col) + '_' + k, img[r : r + out, col - out : col, :])

                else:
                    # dicom dosyalarını kayıt ederken
                    temp_dcm = img[r : r + out, col - out : col]
                    temp_dcm = sitk.GetImageFromArray(temp_dcm)
                    sitk.WriteImage(temp_dcm, str(r) + '_' + str(r + out) + '_' + str(col-out) + '_' + str(col) + '_' + k)

                break
            else:
                #print(r , r + out, c, c + out)

                if is_mask:
                        # #etiketleri kayıtederken
                        cv2.imwrite(str(r) + '_' + str(r + out) + '_' + str(c) + '_' + str(c + out) + '_' + k, img[r : r + out, c : c + out, :])

                else:
                    # dicom dosyalarını kayıt ederken
                    temp_dcm = img[r : r + out, c : c + out]
                    temp_dcm = sitk.GetImageFromArray(temp_dcm)
                    sitk.WriteImage(temp_dcm, str(r) + '_' + str(r + out) + '_' + str(c) + '_' + str(c + out) + '_' + k)

               
    os.chdir(path_to_read)



# Örnek Kullanım
# stride_x enine bindirme. 256x256 bölme işlemi yapacaksanız. 256 - stride_x kadar geriden alarak bölme işlemi yapar.
# stride_y boyune bindirme. 256x256 bölme işlemi yapacaksanız. 256 - stride_y kadar geriden alarak bölme işlemi yapar.


read_path = r"D:\github_test\patch-unpatch-concat\images" #full path ile çalıştırınız
save_path = r"D:\github_test\patch-unpatch-concat\patched_images" #full path ile çalıştırınız


for root, _, files in os.walk(read_path):
    for file in files:
        if file.endswith('.png'):
            slice_with_overlay(file, 64, 64, 256, save_path, read_path)
        