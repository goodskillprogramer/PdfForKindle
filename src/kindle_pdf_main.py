# -*- coding: utf-8 -*-

'''

@author: Administrator
'''
import os
import hashlib
import shutil
from pdf_to_image import  pdf_to_image , pdf2png
from image_split import split_image, ClipType, ClipImageFormat
from image_to_pdf import  create_pdf

def main(srcpdfpath, workpath, max_process_page_num,
         cliptype, marginlength, imageformat):
    
    if not os.path.exists(srcpdfpath):
        print 'PDF {0} not exists'.format(srcpdfpath)
        return
    if not os.path.exists(workpath):
        print 'workspace {0} not exists'.format(srcpdfpath)
        return
            
    pdfname = os.path.splitext(os.path.basename(srcpdfpath))[0]    
        
    md5 = md5sum(srcpdfpath)

    print 'pdf', pdfname ,'md5', md5

    pdfbasepath = os.path.join(workpath, md5)
    pdf_image_save_path = os.path.join(pdfbasepath, 'image')
    pdf_sub_image_save_path = os.path.join(pdfbasepath, 'subimage' + str(cliptype))
    is_create_image = True
    
    if os.path.exists(pdf_image_save_path) and \
       len(os.listdir(pdf_image_save_path)) > 0:
        is_create_image = False
        
    if not os.path.exists(os.path.join(workpath, md5)):      
        print   pdfbasepath
        os.mkdir(pdfbasepath)
        os.mkdir(pdf_image_save_path)
        
    pdfpath = os.path.join(pdfbasepath, 'src.pdf')   
    
    if not os.path.exists(pdfpath):
        shutil.copy(srcpdfpath, pdfpath)
        
    if not os.path.exists(pdf_sub_image_save_path):
        os.mkdir(pdf_sub_image_save_path)

    if is_create_image:
        process_page_num = pdf_to_image(pdfpath, pdf_image_save_path, imageformat, max_process_page_num)
    else:
        process_page_num = len(os.listdir(pdf_image_save_path))

    for i in range(process_page_num):
        print 'page', i
        split_image(r'{0}\{1}.{2}'.format(pdf_image_save_path, i, imageformat),
                    i,
                    pdf_sub_image_save_path,
                    marginlength,
                    imageformat,
                    cliptype)
        
    clip_pdf_path = 'kindle_{0}.pdf'.format(cliptype)
    savepdfname = os.path.join(pdfbasepath, clip_pdf_path)      
    create_pdf(savepdfname, pdf_sub_image_save_path, process_page_num, cliptype, imageformat)
    renamepath = os.path.join(pdfbasepath, pdfname + str(cliptype)+'.pdf')  
        
    shutil.move(savepdfname, renamepath)
    print 'saved pdf to ',renamepath

def md5sum(filename):
    """
    用于获取文件的md5值
    :param filename: 文件名
    :return: MD5码
    """
    if not os.path.isfile(filename):  # 如果校验md5的文件不是文件，返回空
        print 'not file', filename
        return
    myhash = hashlib.md5()
    f = open(filename, 'rb')
    while True:
        b = f.read(8096)
        if not b:
            break
        myhash.update(b)   
    f.close()
    return myhash.hexdigest()
    
if __name__ == '__main__': 
      
    pdfpath = r'E:\book\Python核心编程.pdf'
    pdfpath = r'D:\BaiduNetdiskDownload\jiqixuexi.pdf'
    pdfpath = r'D:\BaiduNetdiskDownload\tongjixuexifangfa.pdf' 
    pdfpath = unicode(pdfpath, 'utf-8')
    
    workpath = r'D:\Users\Administrator\PdfForKindle\tmp\pdf'
    max_process_page_num = None
    marginlength = 5
    print 'start'
    
    main(pdfpath,
         workpath,
         max_process_page_num,
         ClipType.ALL,
         marginlength,
         ClipImageFormat.JPG)

    
    
