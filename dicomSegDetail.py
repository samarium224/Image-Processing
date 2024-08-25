import numpy as np
import pydicom
import pydicom_seg
import SimpleITK as sitk
import os
from PIL import Image
import matplotlib.pyplot as plt

def display_slice(slice):
    plt.imshow(slice, cmap='gray')
    plt.axis('off')
    plt.show()

path = r'D:\HCC_DataSet\manifest-1643035385102\HCC-TACE-Seg\HCC_003\09-12-1997-NA-AP LIVER-64595\4.000000-Recon 2 LIVER 3 PHASE AP-18688\1-001.dcm'

dcm = pydicom.dcmread(path)
print(dcm.Phase)
# reader = pydicom_seg.SegmentReader()
# result = reader.read(dcm)

# for segment_number in result.available_segments:
#     image_data = result.segment_data(segment_number)  # directly available
#     image = result.segment_image(segment_number)  # lazy construction
#     print(image_data[0].shape)

#     display_slice(image_data[30])
    # sitk.WriteImage(image, f'/tmp/seg-{segment_number}.nrrd', True)
    # ct_image = ds.pixel_array
    # ct_image = np.array(ct_image)

    # print(ct_image.shape)
    # max = np.max(ct_image)
    # min = np.min(ct_image)

    # print(f"min: {min} and max: {max}")


# # Function to display a specific slice


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