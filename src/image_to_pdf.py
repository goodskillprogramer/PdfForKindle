import os  

from image_split import ClipType
from reportlab.lib.pagesizes import A4, landscape ,portrait 
# from PIL import Image
from reportlab.platypus import SimpleDocTemplate,   Image,PageBreak  
from reportlab.platypus import PageTemplate, Frame  

#----------------------------------------------------------------------  
def create_pdf(filename, path,page,cliptype,imageformat):  
    """
    """      
    
    if cliptype == ClipType.ALL:
        width,height = portrait(A4)  
    else:
        width,height = landscape(A4)  
    
    print("width = %d, height = %d\n" % (width, height))  
      
    doc = SimpleDocTemplate(filename, pagesize=(height, width))  
    frame1 = Frame(0, 0, height, width, 0, 0, 0, 0, id="normal1")  
    doc.addPageTemplates([PageTemplate(id="Later", frames=frame1)])  
    Story=[]  

    for page in range(page):
        print 'create_pdf',page
        image1 = os.path.join(path,'{0}.{1}.{2}'.format(page,'1',imageformat))
        image2 = os.path.join(path,'{0}.{1}.{2}'.format(page,'2',imageformat))
        image3 = os.path.join(path,'{0}.{1}.{2}'.format(page,'3',imageformat))
        if os.path.exists(image1) and os.stat(image1).st_size:
            Story.append(Image(image1, height, width))
            Story.append(PageBreak())  
        if os.path.exists(image2) and os.stat(image2).st_size:
            Story.append(Image(image2, height, width))
            Story.append(PageBreak())  
        if os.path.exists(image3) and os.stat(image3).st_size:
            Story.append(Image(image3, height, width))
            Story.append(PageBreak())  

    doc.build(Story)  
    print "%s created" % filename  
#----------------------------------------------------------------------  
if __name__ == "__main__":  
    cliptype=ClipType.MARGIN_ONLY
    pdfsavepath = r".\tmp\pdf\484d8037a509648a8e09fc0466b06f38\tongjixuexifangfa{0}.pdf".format(cliptype)  
    subimagepath = r".\tmp\pdf\484d8037a509648a8e09fc0466b06f38\subimage{0}".format(cliptype)  
    
    create_pdf(pdfsavepath, subimagepath, 20, cliptype, 'jpg')

