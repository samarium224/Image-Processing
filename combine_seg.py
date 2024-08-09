import numpy as np
import pydicom
from PIL import Image
import os

path = r'D:\HCC_DataSet\manifest-1643035385102\HCC-TACE-Seg\HCC_017\10-23-1998-NA-ABDOMEN LIVER PROTOCOL-72380\300.000000-Segmentation-18229\1-1.dcm'
ds = pydicom.dcmread(path)
num_slices = len(ds.PerFrameFunctionalGroupsSequence)
list = ['1_liver', '2_tumor', '3_PV', '4_Aorta']
GroupSequence = int(num_slices/4)
count = GroupSequence
segmentIndex = 0
print(GroupSequence)

# Ensure output directory exists
output_dir = 'output/HCC_17/com-seg/'
os.makedirs(output_dir, exist_ok=True)

for i in range(0,GroupSequence):
    
    img = pydicom.dcmread(path)
    liver = img.pixel_array[i].astype(float)
    tumor = img.pixel_array[GroupSequence + i].astype(float)
    portal_vain = img.pixel_array[GroupSequence + GroupSequence + i].astype(float)
    # main image
    img = liver + tumor + portal_vain
    # Handle the case where img.max() is zero to avoid division by zero
    if img.max() > 0:
        rescaled_image = (np.maximum(img, 0) / img.max()) * 255
    else:
        rescaled_image = img * 255

    final_img = np.uint8(rescaled_image)

    final_img = Image.fromarray(final_img)
    # final_img = final_img.transpose(Image.FLIP_LEFT_RIGHT) #exection for HCC03
    # final_img = final_img.transpose(Image.FLIP_TOP_BOTTOM) #exection for HCC03
    # final_img.show()
    # final_img.save(f'output/HCC_10/com-seg/{count}.png')
    # Save as PNG
    output_path = os.path.join(output_dir, f'{count}.png')
    final_img.save(output_path)
    print(f"image {count} complete \n")

    if (count == 1):
        pass
    else:
        count = count - 1
