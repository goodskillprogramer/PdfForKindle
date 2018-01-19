import glob  
import os  
import re  

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, portrait, landscape
from reportlab.lib.pagesizes import A4, landscape  
# from PIL import Image
from reportlab.platypus import SimpleDocTemplate, flowables, Paragraph,  Image,PageBreak  
from reportlab.platypus import PageTemplate, Frame  
  
  
#----------------------------------------------------------------------  

def sorted_nicely( l ):   
    """  
    # http://stackoverflow.com/questions/2669059/how-to-sort-alpha-numeric-set-in-python 
  
    Sort the given iterable in the way that humans expect. 
    """   
    convert = lambda text: int(text) if text.isdigit() else text   
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]   
    return sorted(l, key = alphanum_key)  
  
def convert_image_to_pdf(img_path, pdf_path):
    img = Image.open(img_path)
    (w0, h0) = img.size
    if w0 > h0:
        (w, h) = landscape(A4)
        c = canvas.Canvas(pdf_path, pagesize = landscape(A4))
        c.drawImage(img_path, 0, 0, w, h)
        c.showPage()
        c.save()
    else:
        (w, h) = portrait(A4)
        c = canvas.Canvas(pdf_path, pagesize = portrait(A4))
        c.drawImage(img_path, 0, 0, w, h)
        
        c.showPage()
        c.save()


#----------------------------------------------------------------------  
def create_pdf(savepath,fname, path,page):  
    """"""  
    filename = os.path.join(savepath, fname + ".pdf")  
    width,height = portrait(A4)  
    
    print("width = %d, height = %d\n" % (width, height))  
      
    doc = SimpleDocTemplate(filename, pagesize=(height, width))  
    frame1 = Frame(0, 0, height, width, 0, 0, 0, 0, id="normal1")  
    doc.addPageTemplates([PageTemplate(id="Later", frames=frame1)])  
    Story=[]  

    for page in range(page):
        print 'create_pdf',page
        if os.path.exists(os.path.join(path,'{0}.{1}'.format(page,'1.jpg'))):
            Story.append(Image(os.path.join(path,'{0}.{1}'.format(page,'1.jpg')), height, width))  
            Story.append(PageBreak())  
        if os.path.exists(os.path.join(path,'{0}.{1}'.format(page,'2.jpg'))):
            Story.append(Image(os.path.join(path,'{0}.{1}'.format(page,'2.jpg')), height, width))  
            Story.append(PageBreak())  
        if os.path.exists(os.path.join(path,'{0}.{1}'.format(page,'3.jpg'))):
            Story.append(Image(os.path.join(path,'{0}.{1}'.format(page,'3.jpg')), height, width))  
            Story.append(PageBreak())  

    doc.build(Story)  
    print "%s created" % filename  
#----------------------------------------------------------------------  
if __name__ == "__main__":  
    path = r"./tmp/clip/book_image_half"  
    savepath=r"./tmp/clip"

#     convert_image_to_pdf(front_cover,'./tmp/pdf.pdf')
    create_pdf(savepath,"page30",path)  