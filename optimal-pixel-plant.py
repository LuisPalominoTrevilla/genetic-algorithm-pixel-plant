import imageManipulation as img
from pixelPlant import PixelPlant

# imRGBs = []
# for i in range(5):
#     plant = PixelPlant()
#     im = plant.genRandom()
#     imRGBs.append(img.toRGBImage(im))
wrong = 0
for i in range(1000):
    plant = PixelPlant()
    im = plant.genRandom()
    score = plant.getScore()
    if score == 0:
        wrong += 1

print(1-wrong/1000)

# img.showTree(img.toRGBImage(im))
