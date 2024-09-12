from ImageProcessingHelpers import hcc_image_pro_helper_func as hcc_function

# Change 'root_directory_path' to the path of the directory you want to search
root_directory_path = r'D:\HCC_DataSet\manifest-1643035385102\HCC-TACE-Seg'  # dataset directory

hcc_function.process_segmentation_directories(root_directory_path,
                                              starting_patient=5, 
                                              ending_patient= 5, 
                                              output_dir= "output_PortalVenous", 
                                              CT_Phase=3)