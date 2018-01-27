import os
import cv2
import numpy as np


class ClipType(object):    
    
    ALL=0 # clip the margin and split the image
    MARGIN_ONLY = 1
    
class ClipImageFormat(object):
    JPG='jpg'
    PNG='png'
    
    
def extract_peek_ranges_from_array(array_vals, minimun_val=10, minimun_range=2):
    start_i = None
    end_i = None
    peek_ranges = []
    for i, val in enumerate(array_vals):
        if val > minimun_val and start_i is None:
            start_i = i
        elif val > minimun_val and start_i is not None:
            pass
        elif val < minimun_val and start_i is not None:
            end_i = i
            if end_i - start_i >= minimun_range:
                peek_ranges.append((start_i, end_i))
            start_i = None
            end_i = None
        elif val < minimun_val and start_i is None:
            pass
        else:
            raise ValueError("cannot parse this case...")
    return peek_ranges
        
def write_image(savepath,image_color,margin_length=70):
    range=get_start_end(image_color,0)
    h = image_color.shape[0]
    w = image_color.shape[1]
    cropImg=image_color
    if range:
        start=range[0]
        end=range[1]
        print 'range',range
        if start>margin_length:
            start=start-margin_length
        if w-end>margin_length:
            end=end+margin_length
        cropImg = image_color[0:h, start:end]
        
    cv2.imwrite(savepath,cropImg)#,[int( cv2.IMWRITE_JPEG_QUALITY), 80]
        
def get_clip_points(image_color,peek_ranges,savepath,page,imageformat='jpg',partnumber=3):
    h = image_color.shape[0]
    w = image_color.shape[1]
    print 'heigth',h
    prepart=0
    preline=0
    part=1
    print 'peek len',len(peek_ranges)
    len_peek_ranges=len(peek_ranges)
    
    if len_peek_ranges == 0:
        write_image(os.path.join(savepath,'{0}.{1}.{2}'.format(page,part,imageformat)),image_color)
        return
    elif len_peek_ranges==1:
        cropImg = image_color[0:peek_ranges[0][1], 0:w]
        write_image(os.path.join(savepath,'{0}.{1}.{2}'.format(page,part,imageformat)),cropImg)
        cropImg = image_color[peek_ranges[0][1]:h, 0:w]
        part+=1
        write_image(os.path.join(savepath,'{0}.{1}.jpg'.format(page,part,imageformat)),cropImg)
        return

    for i ,peek_range in enumerate(peek_ranges):
        print 'peek_range i {0} peekrange {1} part {2} partnum {3}'.format(i,peek_range,part, 1.0*h*part/partnumber)
        if  i== len_peek_ranges-1:
            cropImg = image_color[prepart:peek_range[1], 0:w]
            print 'clip 1',prepart,peek_range[1]
            write_image(os.path.join(savepath,'{0}.{1}.{2}'.format(page,part,imageformat)),cropImg)
            break
        elif  peek_range[1] > 1.0*h*part/partnumber :
            clip= preline+int((peek_range[0]-preline)/2)
            print 'clip 2 prepart {} clip {} preline {}'.format(prepart,clip,preline)
            cropImg = image_color[prepart:peek_range[1], 0:w]
            write_image(os.path.join(savepath,'{0}.{1}.{2}'.format(page,part,imageformat)),cropImg)  
            
            if part == partnumber-1:
                cropImg = image_color[peek_range[1]:h, 0:w]
                print 'clip 3',clip,h
                write_image(os.path.join(savepath,'{0}.{1}.{2}'.format(page,part+1,imageformat)),cropImg)
                break 
            prepart=peek_range[1]
            part+=1            
        preline=peek_range[1]

def get_peek_ranges_from_image(image,minimun_val,minimun_range,direction=1):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    adaptive_threshold = cv2.adaptiveThreshold(
    image,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
    cv2.THRESH_BINARY_INV, 11, 2)

    horizontal_sum = np.sum(adaptive_threshold, axis=direction)
    peek_ranges = extract_peek_ranges_from_array(horizontal_sum,minimun_val,minimun_range)
    return peek_ranges

def get_start_end(image,direction):
    peek_ranges=get_peek_ranges_from_image(image,minimun_val=2000,minimun_range=2,direction=0)
    print peek_ranges
    if len(peek_ranges)==1:
        return peek_ranges[0][0],peek_ranges[0][1]
    elif len(peek_ranges)>=2:
        return peek_ranges[0][0],peek_ranges[-1][1]        
    return None
    
def split_image(imagepath,page,savepath,margin_length,imageformat,cliptype=ClipType.MARGIN_ONLY):

    if not os.path.exists(imagepath):
        print imagepath ,'not exists'
        return 
    image_color = cv2.imread(imagepath)
    if cliptype == ClipType.MARGIN_ONLY:
        write_image(os.path.join(savepath,'{0}.{1}.{2}'.format(page,1,imageformat)),image_color,margin_length)
        return

    new_shape = (image_color.shape[1] * 2, image_color.shape[0] * 2)
    image_color = cv2.resize(image_color, new_shape)
    image = cv2.cvtColor(image_color, cv2.COLOR_BGR2GRAY)
    
    adaptive_threshold = cv2.adaptiveThreshold(
        image,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
        cv2.THRESH_BINARY_INV, 11, 2)
    
    horizontal_sum = np.sum(adaptive_threshold, axis=1)
    peek_ranges = extract_peek_ranges_from_array(horizontal_sum)
    get_clip_points(image_color,peek_ranges,savepath,page,imageformat)
    
if __name__ == '__main__':
    for i in range(20):
        print i
        split_image(r'.\tmp\pdf\484d8037a509648a8e09fc0466b06f38\image\{0}.png'.format(i),i,'./tmp/pdf/484d8037a509648a8e09fc0466b06f38/subimage',
                    1,'jpg',ClipType.ALL)
# cv2.imshow('binary image', adaptive_threshold)
# cv2.waitKey(0)



# cv2.imshow('line image', line_seg_adaptive_threshold)
# cv2.imwrite('./tmp/messigray.png',line_seg_adaptive_threshold)
# cv2.waitKey(0)