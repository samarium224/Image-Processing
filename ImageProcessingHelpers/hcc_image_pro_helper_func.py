import os
import numpy as np
import pydicom
from PIL import Image
import re

def find_segmentation_directories(root_dir):
    segmentation_dirs = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for dirname in dirnames:
            if "Segmentation" in dirname:
                segmentation_dirs.append(os.path.join(dirpath, dirname))
    return segmentation_dirs

def find_non_segmentation_directories(root_dir):
    segmentation_dirs = find_segmentation_directories(root_dir)
    parent_directories = [os.path.dirname(seg_dir) for seg_dir in segmentation_dirs]
    non_segmentation_dirs = []
    temp_dir = []
    date_pattern = r'\d{2}-\d{2}-\d{4}'
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for dirname in dirnames:
            match = re.search(date_pattern, dirname)
            if match:
                temp_dir.append(os.path.join(dirpath, dirname))
    
    for i in temp_dir:
        if i not in parent_directories:
            non_segmentation_dirs.append(i)
            
    return non_segmentation_dirs

def sort_subfolders(root_dir):
    directories = os.listdir(root_dir)
    numbers = [int(name.replace('HCC_', '')) for name in directories]
    numbers_sorted = sorted(numbers)
    sorted_file_names = [f"HCC_{number}" for number in numbers_sorted]
    
    return sorted_file_names

def count_dicom_files(directory):
    dicom_count = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.dcm'):
                dicom_count += 1
    return dicom_count

def apply_windowing(pixel_array, window_center, window_width, RI, RS):
    pixel_array_ = Convert_HU_unit(pixel_array, RI, RS)
    lower_limit = window_center - (window_width / 2.0)
    upper_limit = window_center + (window_width / 2.0)
    
    windowed_array = np.clip(pixel_array_, lower_limit, upper_limit)
    windowed_array = ((windowed_array - lower_limit) / (upper_limit - lower_limit)) * 255.0
    
    return windowed_array

def Convert_HU_unit(pixel_array, rescale_intercept, rescale_slope):
    hu_array = (pixel_array * rescale_slope) + rescale_intercept
    return hu_array

def normalization(volume):
    ### *** Normalize the image *** ###
    min = -1000
    max = 1000
    volume[volume < min] = min
    volume[volume > max] = max
    volume = (volume - min) / (max - min)
    volume = volume.astype("float32")

    return volume

def process_dicom_files_in_directory(directory, ValidMasks, output_base_dir, patient_count, CT_phase_number):
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
        
        if not hasattr(img, 'AcquisitionNumber') or img.AcquisitionNumber != CT_phase_number:
            continue
        
        # if count in ValidMasks:
        if True:
            pixel_array = img.pixel_array
            
            if hasattr(img, 'WindowCenter') and hasattr(img, 'WindowWidth'):
                window_center = img.WindowCenter
                window_width = img.WindowWidth
                rescale_intercept = img.RescaleIntercept
                rescale_slope = img.RescaleSlope
                
                if isinstance(window_center, pydicom.multival.MultiValue):
                    window_center = window_center[0]
                if isinstance(window_width, pydicom.multival.MultiValue):
                    window_width = window_width[0]
                
                windowed_array = apply_windowing(pixel_array, window_center, window_width, rescale_intercept, rescale_slope)
            else:
                windowed_array = ((pixel_array - pixel_array.min()) / (pixel_array.max() - pixel_array.min())) * 255.0
            
            final_img = np.uint8(windowed_array)
            final_img = Image.fromarray(final_img)
            
            output_dir = os.path.join(output_base_dir, f"HCC_{patient_count}/CT")
            os.makedirs(output_dir, exist_ok=True)
            
            output_path = os.path.join(output_dir, f'{count}.png')
            final_img.save(output_path)
            print(f"Saved: {output_path}")
        else:
            print(f"Skiping black mask's corrosponding CT {count}")

        count += 1


def process_segmentation_files(segmentation_dir, output_base_dir, patient_count):
    segmentation_files = [os.path.join(segmentation_dir, f) for f in os.listdir(segmentation_dir) if f.endswith('.dcm')]
    Valid_Masks = []  # Masks that are not black

    if not segmentation_files:
        return
    
    for file_path in segmentation_files:
        ds = pydicom.dcmread(file_path)
        num_slices = len(ds.PerFrameFunctionalGroupsSequence)
        segment_names = ['1_liver', '2_tumor', '3_PV', '4_Aorta']
        GroupSequence = int(num_slices / 4)
        count = GroupSequence
        segmentIndex = 0

        for i in range(0, GroupSequence):

            liver = ds.pixel_array[i].astype(float)
            tumor = ds.pixel_array[GroupSequence + i].astype(float)
            portal_vain = ds.pixel_array[GroupSequence + GroupSequence + i].astype(float)
            # main image
            img = liver + tumor + portal_vain

            if img.max() == 0:
                print(f'skipping black mask {count}')

            # if img.max() > 0:
            #     rescaled_image = (np.maximum(img, 0) / img.max()) * 255
            else:
                img = tumor
                Valid_Masks.append(count)
                rescaled_image = img * 255

                final_img = np.uint8(rescaled_image)
                final_img = Image.fromarray(final_img, mode= "L")
            
                output_dir = os.path.join(output_base_dir, f"HCC_{patient_count}/Mask")
                os.makedirs(output_dir, exist_ok=True)
            
                output_path = os.path.join(output_dir, f'{count}.png')
                final_img.save(output_path)
                # print(f"image {count} complete \n")

            if count == 1:
                pass
            else:
                count = count - 1
            
    return Valid_Masks

def process_segmentation_directories(root_directory_path, 
                                     starting_patient = 0, 
                                     ending_patient = 105, 
                                     output_dir = 'experimental_output',
                                     CT_Phase = 2):
    
    segmentation_dirs = find_segmentation_directories(root_directory_path)
    parent_directories = [os.path.dirname(seg_dir) for seg_dir in segmentation_dirs]

    output_base_dir = output_dir
    patient_count = 0

    for index, parent_dir in enumerate(parent_directories):
        patient_count += 1

        if patient_count < starting_patient:
            continue
        if patient_count > ending_patient:
            return
        
        # First Process the segmentation files
        segmentation_subdirs = [d for d in os.listdir(parent_dir) if "Segmentation" in d]
        for seg_dir in segmentation_subdirs:
            valid_masks = process_segmentation_files(os.path.join(parent_dir, seg_dir), output_base_dir, patient_count)

        # Then Process the CT files
        # valid_masks = []
        # process_dicom_files_in_directory(parent_dir, valid_masks, output_base_dir, patient_count, CT_Phase)