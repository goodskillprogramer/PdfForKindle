#-*- coding: utf-8 -*-
import os
import time

def pdf_to_image(file_path,outdir,imageformat,max_process_page_num=None): 
    from wand.image import Image 
    print file_path,os.path.exists(file_path)
    stime=time.time()
    with(Image(filename=file_path,resolution=200)) as source:
        
        images=source.sequence
        pages=len(images)
        print 'read time ',time.time()-stime,pages
        process=0
        for i in range(pages):
            if max_process_page_num and i >= max_process_page_num:
                break           
            subtime=time.time()
            Image(images[i]).save(filename=os.path.join(outdir,str(i)+"."+imageformat))
            process+=1
            print i,'pdf_to_image','save time ',time.time()-subtime
            
        print 'total time',time.time()-stime
        return process

def pdf_num_page(file_path):
    import PyPDF2
    
    pdf_im = PyPDF2.PdfFileReader(file(file_path, "rb"))
    npage = pdf_im.getNumPages()
    return npage
            
def pdf2png(file_path, outdir,imageformat, max_page=None):

    import PythonMagick

    npage = pdf_num_page(file_path)
    if max_page and npage > max_page:
        npage = max_page
    print npage,'page'
    stime=time.time()
    for p in range(npage):
        im = PythonMagick.Image()
        im.density('200')
        im.read(file_path + '[{page}]'.format(page=p))
        im.write(os.path.join(outdir,'{page}.png'.format(page=p)))

    return npage
    print time.time()-stime
                
if __name__ == '__main__':
    pdf_to_image(r'E:\github\PdfForKindle\src\tmp\pdf\484d8037a509648a8e09fc0466b06f38\tongjixuexifangfa.pdf',r'.\tmp\pdf\484d8037a509648a8e09fc0466b06f38')