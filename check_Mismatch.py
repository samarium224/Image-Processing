import os

def count_files_in_directory(directory):
    """
    Count the number of files in the given directory.
    """
    return len([file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))])

def check_ct_mask_image_counts(root_path):
    """
    Check if the number of images in the CT folder matches the number of images in the Mask folder for each HCC folder.
    """
    for dir_name in os.listdir(root_path):
        if dir_name.startswith("HCC_"):
            hcc_dir = os.path.join(root_path, dir_name)
            ct_dir = os.path.join(hcc_dir, "CT")
            mask_dir = os.path.join(hcc_dir, "Mask")

            if os.path.isdir(ct_dir) and os.path.isdir(mask_dir):
                ct_count = count_files_in_directory(ct_dir)
                mask_count = count_files_in_directory(mask_dir)

                if ct_count != mask_count:
                    print(f"Mismatch in {dir_name}: CT has {ct_count} images, Mask has {mask_count} images")
            else:
                print(f"CT or Mask folder missing in {dir_name}")

# Define the root path containing the folders like HCC_1, HCC_2, etc.
root_path = r"D:\HCC_DataSet\manifest-1643035385102\output_Arterial"

# Run the check
check_ct_mask_image_counts(root_path)
