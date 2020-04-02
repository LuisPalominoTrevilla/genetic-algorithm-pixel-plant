from random import randint, choices, random
import imageManipulation as img

TRUNK = '#663d14'
BRANCH = '#855723'
LEAF = '#4e691a'
NULL = '#ffffff'

trunk_limit = 32 - 8

def createEmptyCanvas(m, n):
  return [[NULL for i in range(n)] for i in range(m)]

def genTree():
  im = createEmptyCanvas(32, 16)

  num = randint(4, 10)
  for i in range(31, 2, -1):
    if i >= trunk_limit:
      trunk_girth = 3
    elif i % 2 != trunk_limit % 2:
      num = randint(prev[0]-1, prev[1]-2)
      if num < prev[0]:
        trunk_girth = choices(
          population=[2,3,4],
          weights=[.1, .5, .4],
          k=1)[0]
      elif num == prev[1]-1:
        trunk_girth = choices(
          population=[1,2],
          weights=[.2, .8],
          k=1)[0]
      else:
        trunk_girth = choices(
          population=[1,2,3],
          weights=[.1, .3, .6],
          k=1)[0]
    prev = (num, num+trunk_girth)
    # Paint tree trunk
    for j in range(num, num+trunk_girth):
      if j < 0 or j >= 16:
        continue
      im[i][j] = TRUNK
    # Paint tree branch
    if (trunk_girth > 1 and i < trunk_limit and random() < .38 and i % 2 != trunk_limit % 2):
      left_growth = randint(0, 1) == 0
      branch_start = prev[0] if left_growth else prev[1] - 1
      branch_length = randint(4, 14)
      pixel_pos_i = i
      for j in range(branch_length):
        pixel_pos_j = branch_start-j if left_growth else branch_start+j
        if pixel_pos_j < 0 or pixel_pos_j > 15 or pixel_pos_i <= 0 or pixel_pos_i >= trunk_limit:
          break
        im[pixel_pos_i][pixel_pos_j] = BRANCH
        pixel_pos_i += choices(
            population=[1, 0, -1],
            weights=[.05, .25, .7],
            k=1
          )[0]
        im[pixel_pos_i][pixel_pos_j] = BRANCH
    if (prev[0] < 0 and prev[1] <= 0) or (prev[0] >= 16 and prev[1] >= 15):
      break
  return im

# imRGBs = []
# for i in range(5):
#   im = genTree()
#   imRGBs.append(img.toRGBImage(im))

im = genTree()
imRGB = img.toRGBImage(im)
img.showTree(imRGB)

#img.showTrees(imRGBs)

