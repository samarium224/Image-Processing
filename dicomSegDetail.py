import numpy as np
import pydicom
import os
from PIL import Image
import matplotlib.pyplot as plt

path = r'D:\HCC_DataSet\manifest-1643035385102\HCC-TACE-Seg\HCC_055\02-01-2002-NA-CT CAP LIVER-87181\5.000000-Recon 2 LIVER 2PHASE CAP-17939'

dicom_files = os.listdir(path)

for dicom_file in dicom_files:

    path_ = os.path.join(path, dicom_file)
    ds = pydicom.dcmread(path_)
    print(ds)

    break

    # ct_image = ds.pixel_array
    # ct_image = np.array(ct_image)

    # print(ct_image.shape)
    # max = np.max(ct_image)
    # min = np.min(ct_image)

    # print(f"min: {min} and max: {max}")


# # Function to display a specific slice
# def display_slice(slice_index):
#     plt.imshow(liver_mask[slice_index, :, :], cmap='gray')
#     plt.title(f'Slice {slice_index}')
#     plt.axis('off')
#     plt.show()

# # Initialize the segment number for Liver
# liver_segment_number = None

# # Iterate through Segment Sequence to find the segment number for 'Liver'
# for segment in ds.SegmentSequence:
#     if segment.SegmentLabel == 'Liver':
#         liver_segment_number = segment.SegmentNumber
#         break

# if liver_segment_number is None:
#     raise ValueError('Liver segment not found')

# # Get the dimensions of the segmentation image
# rows = ds.Rows
# cols = ds.Columns
# num_slices = len(ds.PerFrameFunctionalGroupsSequence) #436 !each segment has #109 img for hcc2

# # Initialize an empty array to hold the binary mask for the liver segment
# liver_mask = np.zeros((num_slices, rows, cols), dtype=np.uint8)

# # Iterate through each frame to extract the binary mask for the liver segment
# for i, frame in enumerate(ds.PerFrameFunctionalGroupsSequence):
#     # Get the segment number for this frame
#     segment_number = frame.SegmentIdentificationSequence[0].ReferencedSegmentNumber
    
#     if segment_number == liver_segment_number:
#         # Extract the pixel data for this frame
#         frame_data = ds.pixel_array[i]

#         # Add to the liver mask
#         liver_mask[i, :, :] = frame_data

# display_slice(7)