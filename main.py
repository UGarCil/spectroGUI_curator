'''
Main control module to extract the images and annotations, and visualize them in a simple GUI.
'''
from PIL import Image
from guicurator.curator import GUICurator

def retrieve_resolution(image_path):
        """
        Retrieve the resolution of an image as (width, height).
        """
        with Image.open(image_path) as img:
            return img.size
        



# an image is required to retrieve the resolution
image_calibration_path = r"D:\Garcilazo\Python\00Exercises\CHEMAI_projects\00_Rudra\Spectro_images\spectro_GUI_flutter\server_side_scripts\dataset\images\00002563.png"
RES = retrieve_resolution(image_calibration_path) # Resolution of the canvas


json_files_path = r"D:\Garcilazo\Python\00Exercises\CHEMAI_projects\00_Rudra\Spectro_images\data_retrieving_from_server\Annotations_received"
image_files_path = r"D:\Garcilazo\Python\00Exercises\CHEMAI_projects\00_Rudra\Spectro_images\spectro_GUI_flutter\server_side_scripts\dataset\images"
curator = GUICurator(image_files_path,json_files_path,RES)
curator.exec()