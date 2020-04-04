import imageManipulation as img
from pixelPlant import PixelPlant

imRGBs = []
for i in range(5):
  plant = PixelPlant()
  im = plant.genRandom()
  imRGBs.append(img.toRGBImage(im))

img.showTrees(imRGBs)

