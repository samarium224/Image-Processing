import numpy as np
import pydicom
from PIL import Image

path = r'D:\HCC_DataSet\manifest-1643035385102\HCC-TACE-Seg\HCC_017\10-23-1998-NA-ABDOMEN LIVER PROTOCOL-72380\300.000000-Segmentation-18229\1-1.dcm'
ds = pydicom.dcmread(path)
num_slices = len(ds.PerFrameFunctionalGroupsSequence)
list = ['1_liver', '2_tumor', '3_PV', '4_Aorta']
GroupSequence = int(num_slices/4)
count = GroupSequence
segmentIndex = 0
print(GroupSequence)

for i in range(0,num_slices):
    
    img = pydicom.dcmread(path)
    img = img.pixel_array[i].astype(float)
    
    # Handle the case where img.max() is zero to avoid division by zero
    if img.max() > 0:
        rescaled_image = (np.maximum(img, 0) / img.max()) * 255
    else:
        rescaled_image = img * 255

    final_img = np.uint8(rescaled_image)

    final_img = Image.fromarray(final_img)
    # final_img.show()
    final_img.save(f'output/HCC_17/Seg/{list[segmentIndex]}{count}.png')
    print(f"image {count} complete for segment {list[segmentIndex]}\n")

    if (count == 1):
        count = GroupSequence
        segmentIndex = segmentIndex + 1
    else:
        count = count - 1
