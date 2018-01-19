import os
import cv2
import numpy as np
 
base_dir = "./tmp"
filename="image1.jpeg"

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

    
def get_clip_point(image_color,peek_ranges,savepath,index):
    h = image_color.shape[0]
    w = image_color.shape[1]
    print h
    preend=0
    for i ,peek_range in enumerate(peek_ranges):

        if peek_range[0]>h/2:
            clip= preend+int((peek_range[0]-preend)/2)
            print clip
            cropImg = image_color[0:clip, 0:w]
            s,e=get_start_end(cropImg)
            print s,e
            cropImg=cropImg[s:e,0:w]
            cv2.imwrite(os.path.join(savepath,'{0}.0.jpg'.format(index)),cropImg)
            cropImg = image_color[clip:h, 0:w]
            s,e=get_start_end(cropImg)
            cropImg=cropImg[s:e,0:w]
            cv2.imwrite(os.path.join(savepath,'{0}.1.jpg'.format(index)),cropImg)
            break
        preend=peek_range[1]
        
def get_clip_points(image_color,peek_ranges,savepath,page,partnumber=3):
    h = image_color.shape[0]
    w = image_color.shape[1]
    print 'heigth',h
    prepart=0
    preline=0
    part=1
    print 'peek',len(peek_ranges)
    len_peek_ranges=len(peek_ranges)
    for i ,peek_range in enumerate(peek_ranges):
        print 'peek_range',peek_range
        if i== len_peek_ranges-1:
            cropImg = image_color[prepart:h, 0:w]
            print 'clip',prepart,h
            cv2.imwrite(os.path.join(savepath,'{0}.{1}.jpg'.format(page,part)),cropImg)
            break
        elif peek_range[1] > 1.0*h*part/partnumber :
            clip= preline+int((peek_range[0]-preline)/2)
            print 'clip',prepart,clip
            cropImg = image_color[prepart:clip, 0:w]
            cv2.imwrite(os.path.join(savepath,'{0}.{1}.jpg'.format(page,part)),cropImg)  
            
            if part == partnumber-1:
                cropImg = image_color[clip:h, 0:w]
                print 'clip',clip,h
                cv2.imwrite(os.path.join(savepath,'{0}.{1}.jpg'.format(page,part+1)),cropImg)
                break 
            prepart=peek_range[1]
            part+=1            
        preline=peek_range[1]

def get_peek_ranges_from_image(image,direction=1):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    adaptive_threshold = cv2.adaptiveThreshold(
    image,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
    cv2.THRESH_BINARY_INV, 11, 2)

    horizontal_sum = np.sum(adaptive_threshold, axis=1)
    peek_ranges = extract_peek_ranges_from_array(horizontal_sum)
    return peek_ranges

def get_start_end(image,direction=1):
    peek_ranges=get_peek_ranges_from_image(image)
    return peek_ranges[0][0],peek_ranges[-1][1]
    
def cut_off_white_paddings(image):
    pass        

    
def split_image(imagepath,page,savepath):

    image_color = cv2.imread(imagepath)
   
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
    get_clip_points(image_color,peek_ranges,savepath,page)
    
if __name__ == '__main__':
    for i in range(2):
        print 'page',i+1
        split_image(r'E:\Users\Administrator\workspace\office\src\tmp\pdf\cop\image\{0}.png'.format(i),i,'./tmp/pdf/cop/subimage')
# cv2.imshow('binary image', adaptive_threshold)
# cv2.waitKey(0)



# cv2.imshow('line image', line_seg_adaptive_threshold)
# cv2.imwrite('./tmp/messigray.png',line_seg_adaptive_threshold)
# cv2.waitKey(0)