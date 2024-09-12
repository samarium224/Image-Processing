import os
import numpy as np
import pydicom
from PIL import Image

def find_segmentation_directories(root_dir):
    segmentation_dirs = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for dirname in dirnames:
            if "Segmentation" in dirname:
                segmentation_dirs.append(dirpath)
    return segmentation_dirs

def count_dicom_files(directory):
    dicom_count = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.dcm'):
                dicom_count += 1
    return dicom_count

def process_dicom_files_in_directory(directory, output_base_dir, paitant_count_):
    dicom_files = []
    for dirpath, dirnames, filenames in os.walk(directory):
        # Skip the segmentation directories
        dirnames[:] = [d for d in dirnames if "Segmentation" not in d]
        for filename in filenames:
            if filename.endswith('.dcm'):
                dicom_files.append(os.path.join(dirpath, filename))
    
    count = 1
    for file_path in dicom_files:
        img = pydicom.dcmread(file_path)
        
        if not hasattr(img, 'AcquisitionNumber') or img.AcquisitionNumber != 2:
            continue
        
        pixel_array = img.pixel_array
        
        if hasattr(img, 'WindowCenter') and hasattr(img, 'WindowWidth'):
            window_center = img.WindowCenter
            window_width = img.WindowWidth
            
            if isinstance(window_center, pydicom.multival.MultiValue):
                window_center = window_center[0]
            if isinstance(window_width, pydicom.multival.MultiValue):
                window_width = window_width[0]
            
            print(f"{window_center} and width: {window_width} and min: {pixel_array.min()} and max: {pixel_array.max()}")
            # if (pixel_array.max() >= 1800):
            #     windowed_array = apply_windowing(pixel_array, 1040, 400)
            # else:
            windowed_array = apply_windowing(pixel_array, 1040, 400)
        else:
            windowed_array = ((pixel_array - pixel_array.min()) / (pixel_array.max() - pixel_array.min())) * 255.0
        
        final_img = np.uint8(windowed_array)
        final_img = Image.fromarray(final_img)
        
        output_dir = os.path.join(output_base_dir, f"HCC_{paitant_count_}/CT")
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, f'{count}.png')
        final_img.save(output_path)
        print(f"Saved: {output_path}")
        
        count += 1

def apply_windowing(pixel_array, window_center, window_width):
    lower_limit = window_center - (window_width / 2.0)
    upper_limit = window_center + (window_width / 2.0)
    
    windowed_array = np.clip(pixel_array, lower_limit, upper_limit)
    windowed_array = ((windowed_array - lower_limit) / (upper_limit - lower_limit)) * 255.0
    
    return windowed_array

def process_segmentation_directories(root_directory_path):
    segmentation_dirs = find_segmentation_directories(root_directory_path)
    parent_directories = segmentation_dirs

    output_base_dir = 'experimental_output/'
    patiant_count = 0
    for parent_dir in parent_directories:
        patiant_count += 1
        process_dicom_files_in_directory(parent_dir, output_base_dir, patiant_count)

# Change 'root_directory_path' to the path of the directory you want to search
root_directory_path = r'D:\HCC_DataSet\manifest-1643035385102\HCC-TACE-Seg'  # dataset directory

process_segmentation_directories(root_directory_path)
