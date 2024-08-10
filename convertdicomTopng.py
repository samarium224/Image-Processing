import os
import numpy as np
import pydicom
from PIL import Image
from ImageProcessingHelpers import hcc_image_pro_helper_func as helper

def Convert_Dicom_to_PNG(parent_dir, output_dir, patient_count):
    # """"
    # convert dicom to png for a specific folder
    # """"
    output_base_dir = output_dir
    os.makedirs(output_dir, exist_ok=True)

    dicom_files = os.listdir(parent_dir)
    i = 0
    for index, file_name in enumerate(dicom_files):
        file_path = os.path.join(parent_dir, file_name)
        # read dicom file
        img = pydicom.dcmread(file_path)

        pixel_array = img.pixel_array
            
        if hasattr(img, 'WindowCenter') and hasattr(img, 'WindowWidth'):
            window_center = img.WindowCenter
            window_width = img.WindowWidth
            rescale_intercept = img.RescaleIntercept
            rescale_slope = img.RescaleSlope
            
            windowed_array = helper.apply_windowing(pixel_array, window_center, window_width, rescale_intercept, rescale_slope)
        else:
            return False
        
        final_img = np.uint8(windowed_array)
        final_img = Image.fromarray(final_img)
        
        output_dir = os.path.join(output_base_dir, f"HCC_{patient_count}/CT")
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, f'{i}.png')
        final_img.save(output_path)
        print(f"Saved: {output_path}")
        i = i + 1


# __MAIN__

######################################################################################
# Folder path containing DICOM files
folder_path = r'D:\HCC_DataSet\manifest-1643035385102\HCC-TACE-Seg\HCC_001\04-21-2000-NA-CT ABDPEL WC-49771\3.000000-Recon 2 PRE LIVER-07012'
output_path = "100_custom_dicom_to_png"
Convert_Dicom_to_PNG(folder_path, output_path, 1)
