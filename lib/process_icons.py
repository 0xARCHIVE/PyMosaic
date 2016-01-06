# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 18:36:14 2016

@author: Steven
"""

import colorsys
import os
import math
from PIL import Image,ImageStat,ImageFilter

def process_icons(subdir_name):
    print('Analysing icons')
    subdir_loc = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', subdir_name))
    
    icons = os.listdir(subdir_loc)
    icons_unsorted = []
    
    for icon_name in icons:
        impath = os.path.join(subdir_loc,icon_name)
        file_extension = os.path.splitext(impath)[1]
        if (file_extension != '.png'):
            icons.remove(icon_name)
            continue
        
        print('Loading ' + icon_name)
        #load icon
        im = Image.open(impath)
        if (im.mode != "RGB"):  #todo: fix P->RGB icons
            continue
        
        cols = list(ImageStat.Stat(im).median)
        
        data = []
        data.append(im)
        data.append(cols)
        
        icons_unsorted.append(data)
    return icons_unsorted

def dota_process_icons(subdir_name):
    icons_unsorted = process_icons(subdir_name)
    dota_sortRGB(icons_unsorted)

def resizeImage(im,target_size):
    #resize and crop large images down to size
    resizedIm = Image.new("RGB",target_size)
    
    size_x,size_y = im.size
    target_x,target_y = target_size
    
    if (target_x != size_x):
        im = im.resize((target_x,int(target_x*size_y/size_x)))
    
    size_x,size_y = im.size
    
    if (target_y != size_y):
        left = 0
        right = left + target_x
        upper = int((1/2)*(size_y - target_y))
        lower = upper + target_y
        
        im = im.crop((left,upper,right,lower))
    
    size_x,size_y = im.size
    xoffset = yoffset = 0    
#    xoffset = int((target_x - size_x)/2)
#    yoffset = int((target_y - size_y)/2)
    resizedIm.paste(im,(xoffset,yoffset))
    return resizedIm

def scoreRGB(x,RGB):
    score_red = math.e**(-4*(x**2))/(4/(math.pi**(1/2)))
    score_green = math.e**(-16*((x-0.5)**2))/(4/(math.pi**(1/2)))
    score_blue = math.e**(-4*((x-1)**2))/(4/(math.pi**(1/2)))
    
    red,green,blue = RGB
    h,s,v = colorsys.rgb_to_hsv(RGB[0],RGB[1],RGB[2])
    
    score = h*score_red
    
#    score = (1/3)*(h*score_red + s*score_green + v*score_blue)
    return score

def dota_sortRGB(data):
    #target size for individual icons
    target_x = 85
    target_y = 64
    
    num_cols = 30
    num_rows = int(len(data)/num_cols)
    
    x_max = num_cols*target_x
    y_max = num_rows*target_y
    
    border_x = 1
    border_y = 1
    
    testim = Image.new("RGB",((x_max)+(border_x*(num_cols+1)),(y_max)+(border_y*(num_rows+1))))
    
    y_coord = 0
    for x in range(0,num_cols):
        x_rel = x/num_cols
        y_direction = (-1)**(x)
        
        for y in range(0,num_rows):
            y_rel = y/num_rows
            
            if (y_direction < 0):
                y_coord = num_rows + (y+1)*y_direction
            else:
                y_coord = y
            
            data = sorted(data, key=lambda row: scoreRGB(x_rel,[row[1][0]/255,row[1][1]/255,row[1][2]/255]))
    
            if (len(data) == 0):
                break
            
            row = data.pop()
            im = row[0]
            r,g,b = row[1]
            
            #resize and crop large icons down to size
            im = resizeImage(im,(target_x,target_y))
            
            testim.paste(im,((border_x*(x+1)) + (target_x)*x,(border_y*(y_coord+1) + (target_y)*y_coord)))
    
    testim.save("output1.png")
    
    outputim = Image.new("RGB",(4096,2160))
    outputim.paste(testim,(int((1/2)*(outputim.size[0] - testim.size[0])),int((1/2)*(outputim.size[1] - testim.size[1]))))
    outputim.save("output2.png")
    
    testim.close()
    outputim.close()

#needs work
def dist_RGB(RGB1,RGB2):
    r1,g1,b1 = RGB1
    r2,g2,b2 = RGB2
    
    return ((r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2)

def find_closest_RGB(target_RGB,pallete):
    candidate_color = None
    candidate_score = 0
    
    rt,gb,bt = target_RGB
    
    for color in pallete:
        r,g,b = color[1]
        dist = dist_RGB((r,g,b),(rt,gb,bt))
        if (candidate_color == None or dist < candidate_score):
            candidate_color = color
            candidate_score = dist
    return candidate_color
            

def image_replicate(subdir_name):
    icons = process_icons(subdir_name)
    
    target_im_original = Image.open("collage_target.png")
    
    target_im = target_im_original
    target_im = target_im.resize((int(target_im.size[0]/4),int(target_im.size[1]/4)))
    
    icon_size_x = 32
    icon_size_y = 32
    
    x_size = target_im.size[0]*icon_size_x
    y_size = target_im.size[1]*icon_size_y
    
    output_im = Image.new("RGB",(x_size,y_size))
    
    #resize icons
    for icon in icons:
        icon[0] = resizeImage(icon[0],(icon_size_x,icon_size_y))
    
    #place icons in the output image
    for x in range(0,target_im.size[0]):
        for y in range(0,target_im.size[1]):
            target_RGB = target_im.getpixel((x,y))
            output_RGB = find_closest_RGB(target_RGB,icons)
            
            r,g,b = output_RGB[1]
            
            output_im.paste(output_RGB[0],(x*icon_size_x,y*icon_size_y))
    
    output_im.save("collage_output.png")
    
    output_im_small = output_im.resize((int(output_im.size[0]/4),int(output_im.size[1]/4)))
    output_im_small.save("collage_output_small.png")
    
    output_im.thumbnail(target_im_original.size)
    output_im.save("collage_output_thumb.png")
    
    output_im.close()
    output_im_small.close()