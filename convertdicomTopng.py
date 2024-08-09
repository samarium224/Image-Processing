import os
import numpy as np
import pydicom
from PIL import Image

# Folder path containing DICOM files
folder_path = r'D:\HCC_DataSet\manifest-1643035385102\HCC-TACE-Seg\HCC_017\10-23-1998-NA-ABDOMEN LIVER PROTOCOL-72380\5.000000-Recon 3 3 PHASE LIVER ABD-68712'

# Get a list of all files in the folder
files = os.listdir(folder_path)

# Filter DICOM files
dicom_files = [file for file in files if file.endswith('.dcm')]

# Function to apply windowing to the pixel array
def apply_windowing(pixel_array, window_center, window_width): #window center = window level
    lower_limit = window_center - (window_width / 2.0)
    upper_limit = window_center + (window_width / 2.0)
    
    # Clip pixel values to the window limits
    windowed_array = np.clip(pixel_array, lower_limit, upper_limit)
    
    # Normalize pixel values to the range 0-255
    windowed_array = ((windowed_array - lower_limit) / (upper_limit - lower_limit)) * 255.0
    
    return windowed_array

# Ensure output directory exists
output_dir = 'output/HCC_17/CT'
os.makedirs(output_dir, exist_ok=True)


######################################################################################
count = 0
# Loop through each DICOM file
for i, file_name in enumerate(dicom_files):
    file_path = os.path.join(folder_path, file_name)
    
    # Read DICOM file
    img = pydicom.dcmread(file_path)
    
    # Ensure we process the correct series
    print(img.AcquisitionNumber)
    if img.AcquisitionNumber != 2: # it turns out 2 !!! not 3==portal vinus phase. (1-4 is wrong need to redo) (5,7,8,9,12,13)
        continue
    
    # Extract pixel data
    pixel_array = img.pixel_array
    count = count + 1
    # Get the window center and window width from the DICOM metadata
    if hasattr(img, 'WindowCenter') and hasattr(img, 'WindowWidth'):
        window_center = img.WindowCenter
        window_width = img.WindowWidth
        
        # WindowCenter and WindowWidth can be stored as lists in some cases
        if isinstance(window_center, pydicom.multival.MultiValue):
            window_center = window_center[0]
        if isinstance(window_width, pydicom.multival.MultiValue):
            window_width = window_width[0]
        
        # Apply windowing
        windowed_array = apply_windowing(pixel_array, 1040, 400)  #1040 , 400
        print(pixel_array.min())
        print(pixel_array.max())
        print(f"{window_center} and {window_width}")
    else:
        # If no windowing information is available, normalize the entire range
        windowed_array = ((pixel_array - pixel_array.min()) / (pixel_array.max() - pixel_array.min())) * 255.0
    
    # Convert to uint8
    final_img = np.uint8(windowed_array)
    
    # Convert to PIL image
    final_img = Image.fromarray(final_img)
    
    # Save as PNG
    output_path = os.path.join(output_dir, f'{count}.png')
    final_img.save(output_path)

    print(f"Saved: {output_path}")
