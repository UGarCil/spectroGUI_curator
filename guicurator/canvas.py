"""
An object to handle a canvas made from pygame
"""

import pygame 
import json
# CD. AnnotationRenderer
class AnnotationRenderer():
    def __init__(self, json_path, screen_res):
        '''
        Initialize the AnnotationRenderer with the json file path and screen resolution
        '''
        self.boxes = self.get_annotation_boxes(json_path, screen_res)
        self.rects = self.get_rects_from_boxes(self.boxes)

    def draw(self, display):
        '''
        Draw the rectangles on the display
        '''
        for box in self.rects:
            pygame.draw.rect(display, box["color"], box["rect"], 2)
            # Draw the text of the annotation on the canvas
            font = pygame.font.Font(None, 36)
            text = font.render(str(box["idx"]), True, (0, 0, 0))
            display.blit(text, box["rect"].topleft)
            
    def get_rects_from_boxes(self, boxes):
        '''
        Get the rectangles from the boxes
        '''
        rects = []
        for box in boxes:
            rect = pygame.Rect(box["x"], box["y"], box["w"], box["h"])
            rects.append({"rect": rect, "color": box["color"], "idx": box["idx"]})
        return rects


    def remap(self,value, from1, to1, from2, to2):
        return (value - from1) / (to1 - from1) * (to2 - from2) + from2


    def get_color(self, idx, true_label_vector):
        '''
        Get the color based on the trueLabelVector
        '''
        return "green" if true_label_vector[idx] == 1 else "red"
    
    def get_annotation_boxes(self, json_path, screen_res):
        '''
        Get the annotation boxes from the json file
        '''
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        boxes = []
        for box in data["boxes"]:
            x = int(self.remap(box["x"], 0, 1, 0, screen_res[0]))
            y = int(self.remap(box["y"], 0, 1, 0, screen_res[1]))
            w = int(self.remap(box["w"], 0, 1, 0, screen_res[0]))
            h = int(self.remap(box["h"], 0, 1, 0, screen_res[1]))
            color = self.get_color(box["idx"], data["trueLabelVector"])
            boxes.append({"idx": box["idx"], "x": x, "y": y, "w": w, "h": h, "color": color})
        
        return boxes
        


# CD. Canvas
class Canvas():
    def __init__(self,screen_dims, fps=60):
        pygame.init()
        self.screen_dims = screen_dims 
        self.fps = fps
        self.display = pygame.display.set_mode(self.screen_dims)
        pygame.display.set_caption("Canvas")
        self.clock = pygame.time.Clock()
        self.image = None # Current spectrogram image to render
        self.annotations = None # List of annotations (dict)
        
    def draw(self):
        '''
        Draw the current image and annotations on the canvas
        '''
        self.display.fill((255, 255, 255))
        if self.image is not None:
            self.display.blit(self.image, self.rect)
        # iterate through the annotations and draw them on the canvas
        if self.annotations is not None:
            self.annotations.draw(self.display)
        pygame.display.flip()
        
    def update(self):
        '''
        Update the canvas with the current image and annotations
        '''
        self.draw()
        self.clock.tick(self.fps)
        
    def update_canvas(self, _image_path:str, _json_path_ann:str):
        '''
        Update the canvas with a new image and annotations
        '''
        self.update_image(_image_path)
        self.update_annotations(_json_path_ann)

    def update_image(self, _image_path):
        '''
        Update the current image to be displayed
        '''
        self.image = pygame.image.load(_image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        
    def update_annotations(self, _json_path_ann):
        '''
        Update the current annotations to be displayed
        '''
        self.annotations = AnnotationRenderer(_json_path_ann, self.screen_dims)
        
if __name__ == "__main__":
    RES = (800, 600) # Resolution of the canvas
    FPS = 60 # Frames per second
    pygame.init() # Initialize pygame
    test_json_path = r"D:\Garcilazo\Python\00Exercises\CHEMAI_projects\00_Rudra\Spectro_images\data_retrieving_from_server\Annotations_received\WABAR825_00002563.json"
    test_image_path = r"D:\Garcilazo\Python\00Exercises\CHEMAI_projects\00_Rudra\Spectro_images\spectro_GUI_flutter\server_side_scripts\dataset\images\00002563.png"
    canvas = Canvas(RES, FPS)
    canvas.update_canvas(test_image_path, test_json_path)
    # Main loop to keep the canvas open and update it
    while True:
        canvas.update()
    
    