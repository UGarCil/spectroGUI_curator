''''
An integration of pygame and json to visualize data annotations in a simplified GUI.
'''

import pygame
import os
import json
from os.path import join as jn
# from utils import *
from .canvas import Canvas

# CD. GUICurator()
class GUICurator():
    '''
    Control module to handle GUI image and data loading
    '''
    def __init__(self,path_images, path_anns, res, fps=60):
        # self.path_images = [jn(path_images,_img) for _img in os.listdir(path_images) ]
        self.path_images = path_images 
        self.path_anns = path_anns
        self.list_of_path_anns = [_json for _json in os.listdir(path_anns)]
        self.canvas = Canvas(res, fps)
        self.idx = 0
    
    def changeImage(self, is_next=True):
        '''
        Extract the images at a respective index in the annotation files
        '''
        if is_next:
            self.idx += 1
        else:
            self.idx -= 1
        # split by underscore and keep the second element. Trim .png
        img_no = self.list_of_path_anns[self.idx].split("_")[1].replace(".json","")
        # form the image name and pass it to the canvas
        img_path_at_idx = jn(self.path_images,img_no+".png")
        json_file_at_idx = jn(self.path_anns,self.list_of_path_anns[self.idx])
        self.canvas.update_canvas(img_path_at_idx,json_file_at_idx)
        
    def exec(self):
        while True:
            self.canvas.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_q:
                        self.changeImage(is_next=True)
                    if event.key == pygame.K_e:
                        self.changeImage(is_next=False)
# Example usage
if __name__ == "__main__":
    RES = (800, 600) # Resolution of the canvas
    json_files_path = r"D:\Garcilazo\Python\00Exercises\CHEMAI_projects\00_Rudra\Spectro_images\data_retrieving_from_server\Annotations_received"
    image_files_path = r"D:\Garcilazo\Python\00Exercises\CHEMAI_projects\00_Rudra\Spectro_images\spectro_GUI_flutter\server_side_scripts\dataset\images"
    curator = GUICurator(image_files_path,json_files_path,RES)
    curator.exec()
        
    
    
    