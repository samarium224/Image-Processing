import numpy as np
import matplotlib.pyplot as plt
from pydicom import dcmread

path = r'D:\DatasetDownload\manifest-1643035385102\HCC-TACE-Seg\HCC_001\11-30-1999-NA-CT-CAP WWO CON-00377\300.000000-Segmentation-99942\1-1.dcm'

dicom_object = dcmread(path)
num_slices = len(dicom_object.pixel_array)

# Limit the display to a maximum of 20 slices
max_slices = min(20, num_slices)

# Plot the first 20 slices in a 4x5 grid
fig, axs = plt.subplots(4, 5, figsize=(15, 12))  # Adjust figsize as needed
for i in range(4):
    for j in range(5):
        slice_index = i * 5 + j
        if slice_index < max_slices:
            axs[i, j].imshow(dicom_object.pixel_array[slice_index], cmap=plt.cm.gray)
            axs[i, j].axis('off')
            axs[i, j].set_title(f"Slice {slice_index + 1}", fontsize=8)  # Set font size
            axs[i, j].set_title(f"Slice {slice_index + 1}", fontsize=8, pad=2)  # Set font size and padding

plt.tight_layout()
plt.show()
