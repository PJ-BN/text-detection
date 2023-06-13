import scipy.io
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import pathlib

class convert:
    
    def __init__(self,mat, img, save) -> None:
        print(mat)
        mat_p = self.get_path(mat)
        img_p = self.get_path(img)
        save_p = self.get_path(save)
        self.create_label(mat_p, img_p, save_p)    
    
    
    def get_path(self,path):
        current_path = pathlib.Path.cwd()
        pa = pathlib.Path(current_path)
        print(path)
        p = pathlib.Path(path)
        a = pa/p
        return a

    def get_axis(self,file):
        values = []
        mat = scipy.io.loadmat(file)
        a = mat['gt']
        b = [ i for i in a]
        for i in b:
            c = {
                'x': i[1],
                'y': i[3],
                'val' :i[4]
            }
            
            values.append(c)
                    
        return values
        
        
    def load_image( self , path):
        
        img = Image.open(path)
        plt.imshow(img)
        color = (255,0,0)
        thickness = 2
        draw = ImageDraw.Draw(img)
        return img, color, thickness, draw

    def draw_line(self, file, path):
        a= self.get_axis(file)
        img , color , thickness, draw = self.load_image(path)
        for i in range(len(a)):
            for j in range(1, len(a[i]['x'][0])):
            
                x_start = a[i]['x'][0][j-1]
                y_start = a[i]['y'][0][j-1]
                x_end = a[i]['x'][0][j]
                y_end = a[i]['y'][0][j]
                
                start = (x_start, y_start)
                end = (x_end, y_end)
                draw.line([start, end], fill= color, width=thickness)
            
            sta = (a[i]['x'][0][0], a[i]['y'][0][0])
            end = (a[i]['x'][0][-1], a[i]['y'][0][-1])
            draw.line([end, sta], fill= color, width=thickness)         
            
        return img
        

    def save_image(self, img, dir, name):
        image = pathlib.Path(name.name)
        save = dir/image
        img.save(save)
        
        
    def create_label(self, mat_dir, img_dir, save_dir):
        mat_path = [i for i in mat_dir.iterdir()]
        img_path = [i for i in img_dir.iterdir()]
        for i in range(len(mat_path)):
            img = self.draw_line(mat_path[i], img_path[i])
            self.save_image(img, save_dir, img_path[i])
        

mat_dir = "text-reco/TT_new_train_GT/Train"
img_dir = "text-reco/totaltext/Images/Train"
save_dir = "text-reco/totaltext/Images/train_label"

convert(mat_dir, img_dir, save_dir)