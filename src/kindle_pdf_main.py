#-*- coding: utf-8 -*-

'''

@author: Administrator
'''
import os
from pdf_to_image import  pdf_to_image 
from image_split import split_image
from image_to_pdf import  create_pdf

def main(pdfpath,workpath,max_process_page_num):
    
    pdfname=os.path.splitext(os.path.basename(pdfpath))[0]
    print 'pdf',pdfname    

    pdfbasepath=os.path.join(workpath,pdfname)
    pdf_image_save_path=os.path.join(pdfbasepath,'image')
    pdf_sub_image_save_path=os.path.join(pdfbasepath,'subimage')
    
    if not os.path.exists(os.path.join(workpath,pdfname)):      
        print   pdfbasepath
        os.mkdir(pdfbasepath)
        os.mkdir(pdf_image_save_path)
        os.mkdir(pdf_sub_image_save_path)

    pdf_to_image(pdfpath,pdf_image_save_path,max_process_page_num)

    for i in range(max_process_page_num):
        print 'page',i
        split_image(r'{0}\{1}.png'.format(pdf_image_save_path,i),i,pdf_sub_image_save_path)
        
    create_pdf(pdfbasepath,'kindle_{0}'.format(os.path.basename(pdfpath)),pdf_sub_image_save_path,max_process_page_num)

if __name__ == '__main__':
    pdfpath='./tmp/pdf/ComputerComponent.pdf'
    workpath='./tmp/pdf'
    max_process_page_num=4
    main(pdfpath,workpath,max_process_page_num)
    
    