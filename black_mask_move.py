import os
import shutil
from PIL import Image
import numpy as np
import json

def remove_black_masks(mask_image_path, tumor_image_path, output_black_masks, output_black_tumor_images):
    """
    Function to find black mask images and move them, along with their corresponding tumor images, to a new folder.
    
    Parameters:
        mask_image_path (str): Path to the folder containing mask images.
        tumor_image_path (str): Path to the folder containing tumor images.
        output_black_masks (str): Path to the folder to store black mask images.
        output_black_tumor_images (str): Path to the folder to store corresponding tumor images.
    """
    # Create output directories if they do not exist
    os.makedirs(output_black_masks, exist_ok=True)
    os.makedirs(output_black_tumor_images, exist_ok=True)

    # List all mask images
    mask_images = os.listdir(mask_image_path)

    # Loop through mask images to find black masks
    for mask_image_name in mask_images:
        mask_image_full_path = os.path.join(mask_image_path, mask_image_name)

        # Open the mask image using PIL
        with Image.open(mask_image_full_path) as mask_image:
            # Convert the image to a NumPy array
            mask_array = np.array(mask_image)

            # Check if the mask is completely black
            if np.max(mask_array) == 0:
                # The mask is completely black, move the mask and corresponding tumor image
                tumor_image_full_path = os.path.join(tumor_image_path, mask_image_name)

                # Move the black mask image
                shutil.move(mask_image_full_path, os.path.join(output_black_masks, mask_image_name))

                # Move the corresponding tumor image if it exists
                if os.path.exists(tumor_image_full_path):
                    shutil.move(tumor_image_full_path, os.path.join(output_black_tumor_images, mask_image_name))

                print(f"Moved black mask and corresponding tumor image: {mask_image_name}")

    print("Completed moving black masks and their corresponding tumor images.")


def remove_specific_images(image_path, output_path, image_names):
    """
    Function to remove specific named images to a new folder.
    
    Parameters:
        image_path (str): Path to the folder containing images.
        output_path (str): Path to the folder to store removed images.
        image_names (list): List of image names (without extensions) to remove.
    """
    # Create output directory if it does not exist
    os.makedirs(output_path, exist_ok=True)

    # Loop through the specified image names
    for image_name in image_names:
        image_file = f"{image_name}.png"
        image_full_path = os.path.join(image_path, image_file)

        if os.path.exists(image_full_path):
            shutil.move(image_full_path, os.path.join(output_path, image_file))
            print(f"Moved specific image: {image_file}")
        else:
            print(f"Image not found: {image_file}")

    print("Completed moving specified images.")


def remove_images_and_masks_below_dice_score(image_path, mask_path, output_image_path, output_mask_path, dice_score_file, threshold=0.8):
    """
    Function to remove images and corresponding masks with dice scores below a specified threshold.
    
    Parameters:
        image_path (str): Path to the folder containing images.
        mask_path (str): Path to the folder containing masks.
        output_image_path (str): Path to the folder to store removed images.
        output_mask_path (str): Path to the folder to store removed masks.
        dice_score_file (str): Path to the file containing dice scores in JSON format.
        threshold (float): The dice score threshold; images with scores below this will be moved.
    """
    # Create output directories if they do not exist
    os.makedirs(output_image_path, exist_ok=True)
    os.makedirs(output_mask_path, exist_ok=True)

    # Load the dice scores from the JSON file
    with open(dice_score_file, 'r') as file:
        dice_scores = json.load(file)

    # Filter images with dice scores below the threshold
    for image_name, dice_score in dice_scores.items():
        if dice_score < threshold:
            image_full_path = os.path.join(image_path, image_name)
            mask_full_path = os.path.join(mask_path, image_name)

            if os.path.exists(image_full_path):
                shutil.copy(image_full_path, os.path.join(output_image_path, image_name))
                print(f"copied image with dice score below {threshold}: {image_name} (score: {dice_score})")
            else:
                print(f"Image not found: {image_name}")
            
            # Check and move the corresponding mask
            if os.path.exists(mask_full_path):
                shutil.copy(mask_full_path, os.path.join(output_mask_path, image_name))
                print(f"copied corresponding mask for image: {image_name}")
            else:
                print(f"Mask not found for image: {image_name}")

    print("Completed moving images and corresponding masks with dice scores below the threshold.")


# Example usage:
mask_path = r"D:\HCC_DataSet\manifest-1643035385102\Tumor_DATA\[4] Fulldataset Plus CLAHE\masks"
image_path = r"D:\HCC_DataSet\manifest-1643035385102\Tumor_DATA\[4] Fulldataset Plus CLAHE\images"
output_mask = r"D:\HCC_DataSet\manifest-1643035385102\Tumor_DATA\[4] Fulldataset Plus CLAHE\black_masks"
output_tumor = r"D:\HCC_DataSet\manifest-1643035385102\Tumor_DATA\[4] Fulldataset Plus CLAHE\black_images"

remove_black_masks(mask_path, image_path, output_mask, output_tumor)


# Paths
# image_path = r"D:\HCC_DataSet\manifest-1643035385102\results\fold_2\images"  # Path to the folder containing images
# mask_path = r"D:\HCC_DataSet\manifest-1643035385102\results\fold_2\masks"  # Path to the folder containing masks
# output_image_path = r"D:\HCC_DataSet\manifest-1643035385102\results\tumor\low_dice_images"  # Path to store removed images
# output_mask_path = r"D:\HCC_DataSet\manifest-1643035385102\results\tumor\low_dice_masks"  # Path to store removed masks
# dice_score_file = r"D:\HCC_DataSet\manifest-1643035385102\results\dice score\dice_scores_fold_2.json"  # Path to the dice score file

# # Call the function to remove images and masks below a dice score of 0.8
# remove_images_and_masks_below_dice_score(image_path, mask_path, output_image_path, output_mask_path, dice_score_file, threshold=0.6)


# # Call the function to remove black masks
# remove_black_masks(mask_image_path, tumor_image_path, output_black_masks, output_black_tumor_images)

# # Call the function to remove specific images
# remove_specific_images(tumor_image_path, output_specific_images, specific_image_names)
