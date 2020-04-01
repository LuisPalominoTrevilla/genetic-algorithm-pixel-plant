import webcolors as wc
import matplotlib.pyplot as plt

def toRGBImage(im):
  rgbImage = []
  for row in im:
    rgbRow = []
    for pix in row:
      rgbRow.append(wc.hex_to_rgb(pix))
    rgbImage.append(rgbRow)
  return rgbImage

def showTrees(imRGBs):
  fig=plt.figure(figsize=(6, 6))
  columns = 5

  for i in range(1, columns +1):
    fig.add_subplot(1, columns, i)
    plt.imshow(imRGBs[i-1])
    plt.axis('off')
  plt.show()

def showTree(imRGB):
  plt.imshow(imRGB)
  plt.show()