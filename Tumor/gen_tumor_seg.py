import os
import numpy as np
import pydicom
from PIL import Image
import shutil  # Import shutil for copying files
import utility.ImageProcessingHelpers.hcc_image_pro_helper_func as hcc_function

folder_path = r"D:\HCC_DataSet\manifest-1643035385102\experimental_output"
output_base_dir = r"D:\HCC_DataSet\manifest-1643035385102\output-tumor-multiclass"
root_directory_path = r'D:\HCC_DataSet\manifest-1643035385102\HCC-TACE-Seg'  # dataset directory
hcc_folders_to_skip = ["HCC_3", "HCC_10", "HCC_17", "HCC_65", "HCC_89"]
hcc_folders_to_keep = ["HCC_3"]

seg_files = hcc_function.find_segmentation_directories(root_directory_path)

# List all the directories
hcc_folders = hcc_function.sort_subfolders(folder_path)  # Need numbers also

for i, hcc_folder in enumerate(hcc_folders):

    if hcc_folder not in hcc_folders_to_keep:
        print("Skipping...")
    else:
        hcc_folder_full_path = os.path.join(folder_path, hcc_folder)

        masks = os.listdir(os.path.join(hcc_folder_full_path, 'Mask'))
        CT_images = os.listdir(os.path.join(hcc_folder_full_path, 'CT'))
        numbers = [int(name.replace('.png', '')) for name in masks]
        numbers_sorted = sorted(numbers, reverse=True)
        sorted_file_names = [f"{number}.png" for number in numbers_sorted]
        
        segmentation_file = os.path.join(seg_files[i], '1-1.dcm')

        ds = pydicom.dcmread(segmentation_file)
        num_slices = len(ds.PerFrameFunctionalGroupsSequence)
        GroupSequence = int(num_slices / 4)
        count = GroupSequence + 1
        black_mask = []
        good_mask = []
        
        for j in range(0, GroupSequence):
            
            if(count == 1):
                pass
            count = count - 1
            
            liver = ds.pixel_array[j].astype(float)
            tumor = ds.pixel_array[GroupSequence + j].astype(float)
            pv = ds.pixel_array[GroupSequence + GroupSequence + j].astype(float)
            
            rescaled_image_liver = (liver + pv) * 255
            rescaled_image_tumor = tumor * 255

            mask_array_liver = np.array(rescaled_image_liver)
            mask_array_tumor = np.array(rescaled_image_tumor)

            # Create an RGB image with the same dimensions as the mask images
            combined_image = np.zeros((mask_array_liver.shape[0], mask_array_liver.shape[1], 3), dtype=np.uint8)

            # Define the new mask colors (R, G, B)
            mask_color_liver = (71, 39, 119)
            mask_color_tumor = (62, 73, 137)

            # Apply the liver mask color where the mask is white (255 in grayscale)
            combined_image[mask_array_liver == 255] = mask_color_liver
            
            for i in range(3):
                combined_image[mask_array_tumor == 255, i] = np.maximum(combined_image[mask_array_tumor == 255, i], mask_color_tumor[i])

            # Main image
            final_img = combined_image

            if final_img.max() == 0:
                black_mask.append(j)
            else:
                # rescaled_image = img * 255
                good_mask.append(j)
            
                # final_img = np.uint8(rescaled_image)
                final_img = Image.fromarray(final_img)
                final_img = final_img.transpose(Image.FLIP_LEFT_RIGHT) #exection for HCC03
                final_img = final_img.transpose(Image.FLIP_TOP_BOTTOM) #exection for HCC03
                
                output_mask_dir = os.path.join(output_base_dir, f"{hcc_folder}/Mask")
                os.makedirs(output_mask_dir, exist_ok=True)
                
                output_mask_path = os.path.join(output_mask_dir, f'{count}.png')
                final_img.save(output_mask_path)

                # Copy the corresponding CT image if it's not a black mask
                ct_image_name = f'{count}.png'
                if ct_image_name in CT_images:
                    output_ct_dir = os.path.join(output_base_dir, f"{hcc_folder}/CT")
                    os.makedirs(output_ct_dir, exist_ok=True)
                    
                    src_ct_image_path = os.path.join(hcc_folder_full_path, 'CT', ct_image_name)
                    dst_ct_image_path = os.path.join(output_ct_dir, ct_image_name)
                    shutil.copy(src_ct_image_path, dst_ct_image_path)

        print(f"Processing {hcc_folder} good masks: {len(good_mask)} and black masks {len(black_mask)}")
