# PDF文件切割 #
## 功能 ##
  * 切割PDF书籍，使其适合Kindle横向阅读
  * 将每页PDF切成三段
  * 切割大致均等的三段，每段以空白行为分割依据

## 基本步骤
  * 将所有的PDF文件页面转换成图片
  * 将图片中所有像素值做垂直投影，找出所有空白行
  * 根据空白行的像素位置分割每个图片为大致的垂直三段
  *将所有的分割后的图片再装成PDF在Kindle上阅读
  
## 提醒 ##
 * 如果带切割的PDF文件能做白切边更佳
 * .\tmp\pdf\ComputerComponent\kindle_ComputerComponent.pdf.pdf 为切割以后的效果，这样的PDF文件可以在kindle上横屏阅读
 
 2017 alex All Rights Reserved.
  




