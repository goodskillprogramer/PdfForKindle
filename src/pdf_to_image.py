#-*- coding: utf-8 -*-
import os
import time

def pdf_to_image(file_path,outdir,max_process_page_num=None): 
    from wand.image import Image 
    stime=time.time()
    with(Image(filename=file_path,resolution=300)) as source:
        print 'read time ',time.time()-stime
        images=source.sequence
        pages=len(images)
        for i in range(pages):
            if max_process_page_num and i >= max_process_page_num:
                break           
            subtime=time.time()
            Image(images[i]).save(filename=os.path.join(outdir,str(i)+'.png'))
            print i,'pdf_to_image','save time ',time.time()-subtime
        print 'total time',time.time()-stime
            
def pdf2png(file_path, outdir, max_page=None):
    import PyPDF2
    import PythonMagick
    pdf_im = PyPDF2.PdfFileReader(file(file_path, "rb"))
    npage = pdf_im.getNumPages()
    if max_page and npage > max_page:
        npage = max_page
    stime=time.time()
    for p in range(npage):
        im = PythonMagick.Image()
        im.density('300')
        im.read(file_path + '[{page}]'.format(page=p))
        im.write(os.path.join(outdir,'{page}.png'.format(page=p)))
    print time.time()-stime
                
if __name__ == '__main__':
    pdf_to_image('./tmp/clip/深入探索C++对象模型.pdf','./tmp/clip/bookimage')