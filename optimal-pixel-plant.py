from random import randint, choices, random, choice
import imageManipulation as img

TRUNK = '#663d14'
BRANCH = '#855723'
LEAF = '#4e691a'
NULL = '#ffffff'

trunk_limit = 32 - 8

def createEmptyCanvas(m, n):
  return [[NULL for i in range(n)] for i in range(m)]

def getPossibleLocations(i, j, im):
  successors = []
  forbidden = set([BRANCH, TRUNK])
  if j > 0 and im[i][j-1] not in forbidden:
    successors.append((i, j-1))
  if j < 15 and im[i][j+1] not in forbidden:
    successors.append((i, j+1))
  if i > 0 and im[i-1][j] not in forbidden:
    successors.append((i-1, j))
  if i < trunk_limit-1 and im[i+1][j] not in forbidden:
    successors.append((i+1, j))
  return successors

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
    if (trunk_girth > 1 and i < trunk_limit and random() < .34 and i % 2 != trunk_limit % 2):
      left_growth = randint(0, 1) == 0
      branch_start = prev[0] if left_growth else prev[1] - 1
      pixel_pos_i = i
      pixel_pos_j = branch_start
      while pixel_pos_j > 0 and pixel_pos_j < 15 and pixel_pos_i > 0 and pixel_pos_i < trunk_limit:
        pixel_pos_j += -1 if left_growth else 1
        if im[pixel_pos_i][pixel_pos_j] != NULL:
          break
        im[pixel_pos_i][pixel_pos_j] = BRANCH
        pixel_pos_i += choices(
            population=[1, 0, -1],
            weights=[.05, .25, .7],
            k=1
          )[0]
        im[pixel_pos_i][pixel_pos_j] = BRANCH
      # Paint tree leaf
      num_leafs = randint(3,8)
      leaf_positions = getPossibleLocations(pixel_pos_i, pixel_pos_j, im)
      while num_leafs > 0:
        i, j = leaf_positions.pop()
        im[i][j] = LEAF
        if (len(leaf_positions) == 0):
          leaf_positions = getPossibleLocations(i, j, im)
        num_leafs-=1
    if (prev[0] < 0 and prev[1] <= 0) or (prev[0] >= 16 and prev[1] >= 15):
      break
  return im

imRGBs = []
for i in range(5):
  im = genTree()
  imRGBs.append(img.toRGBImage(im))

img.showTrees(imRGBs)

