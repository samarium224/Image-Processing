from PIL import Image
import cv2
import os
import albumentations as A
import numpy as np
from tqdm import tqdm

def ImageAugPerfold():
  images_location = r'D:\HCC_DataSet\manifest-1643035385102\output_PortalVenous\Manifold\Data\Train'
  max_train = 7000
  desired_size = (512, 512)  # Desired size for both original and augmented images

  # Define the same transforms for both image and mask
  transforms = A.Compose([
    A.RandomBrightnessContrast(p=0.4, brightness_limit=0.15, contrast_limit=0.15),
      A.HorizontalFlip(p=0.5),
      A.VerticalFlip(p=0.5),
      A.Rotate(limit=[90, 180], p=0.5),
      A.Resize(*desired_size)  # Resize to the desired size
  ], is_check_shapes=False)  # Disable shape checking

  # Additional enhancement: CLAHE (Contrast Limited Adaptive Histogram Equalization)
  clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

  # Augmentation loop for images and masks
  for fold in range(1, 6):
      fold_path = os.path.join(images_location, f'fold_{fold}')
      # fold_path = images_location
      image_list = os.listdir(os.path.join(fold_path, "images"))

      image_list = np.random.choice(image_list, int(len(image_list)), replace=False)
      remain_image = max_train - int(len(image_list))

      for i in tqdm(range(remain_image)):
          image_name = image_list[i % len(image_list)]
          image_path = os.path.join(fold_path, "images", image_name)
          mask_name = image_name
          mask_path = os.path.join(fold_path, "masks", mask_name)

          # Read and resize image to the desired size
          original_image = Image.open(image_path)
          original_image = original_image.resize(desired_size, Image.LANCZOS)  # Using Lanczos resampling filter
          original_image = original_image  # Convert to grayscale

          # Read mask
          mask = Image.open(mask_path).convert('L')

          # Convert PIL Image to numpy array for CLAHE
          image_np = np.array(original_image)

          # Apply CLAHE to enhance image contrast
          # image_np = clahe.apply(image_np)

          # Convert back to PIL Image
          image = Image.fromarray(image_np)

          # Apply augmentation to both image and mask
          augmented = transforms(image=np.array(image), mask=np.array(mask))
          augmented_image = augmented['image']
          augmented_mask = augmented['mask']

          # Save augmented image
          image_output_path = os.path.join(fold_path, "images", image_name[:-4] + f'_aug{i}.png')
          cv2.imwrite(image_output_path, augmented_image)

          # Save augmented mask
          mask_output_path = os.path.join(fold_path, "masks", mask_name[:-4] + f'_aug{i}.png')
          Image.fromarray(augmented_mask).save(mask_output_path)



def ImageAugSingleFolder(file_location, target_img_dir = "images", target_mask_dir = "masks", aug_output_path="Augmented"):
  
  desired_size = (512, 512)  # Desired size for both original and augmented images

  # Define the same transforms for both image and mask
  transforms = A.Compose([
    A.RandomBrightnessContrast(p=0.4, brightness_limit=0.15, contrast_limit=0.15),
      A.HorizontalFlip(p=0.5),
      A.VerticalFlip(p=0.5),
      A.Rotate(limit=[90, 180], p=0.5),
      A.Resize(*desired_size)  # Resize to the desired size
  ], is_check_shapes=False)  # Disable shape checking

  # Additional enhancement: CLAHE (Contrast Limited Adaptive Histogram Equalization)
  clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

  # Augmentation loop for images and masks

  image_list = os.listdir(os.path.join(file_location, target_img_dir))

  for i in tqdm(image_list):
      image_name = i
      image_path = os.path.join(file_location, target_img_dir, image_name)
      mask_name = image_name
      mask_path = os.path.join(file_location, target_mask_dir, mask_name)

      # Read and resize image to the desired size
      original_image = Image.open(image_path)
      original_image = original_image.resize(desired_size, Image.LANCZOS)  # Using Lanczos resampling filter
      original_image = original_image  # Convert to grayscale

      # Read mask
      mask = Image.open(mask_path).convert('L')

      # Convert PIL Image to numpy array for CLAHE
      image_np = np.array(original_image)
      mask = np.array(mask)
      # Apply CLAHE to enhance image contrast
      image_np = clahe.apply(image_np)

      # Convert back to PIL Image
      # image = Image.fromarray(image_np)

      # Apply augmentation to both image and mask
      # augmented = transforms(image=np.array(image), mask=np.array(mask))
      # augmented_image = augmented['image']
      # augmented_mask = augmented['mask']

      # no transformation only CLAHE
      augmented_image = image_np
      augmented_mask = mask

      # Save augmented image
      os.makedirs(aug_output_path, exist_ok=True)
      image_output_path = os.path.join(aug_output_path, "images", f'{i}')
      cv2.imwrite(image_output_path, augmented_image)

      # Save augmented mask
      mask_output_path = os.path.join(aug_output_path, "masks", f'{i}')
      Image.fromarray(augmented_mask).save(mask_output_path)


ImageAugSingleFolder(file_location="D:\HCC_DataSet\manifest-1643035385102\Tumor_DATA\[1] full dataset\main", aug_output_path="D:\HCC_DataSet\manifest-1643035385102\Tumor_DATA\Aug_all")