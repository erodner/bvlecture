import numpy as np
from skimage.draw import disk, rectangle


def generate_example():
    """ Generating an example image to perform binary segmentation """
    #
    # The techniques applied here are not related to the exercise.
    # The following code just generates example images.
    #
    img_shape = np.array((512, 512))
    objects = np.zeros(img_shape, dtype=np.uint8)
    offset = np.random.randint(60,220, (3))

    # draw red circles
    num_circles = int(max(np.random.randn()*3+120, 0))
    for i in range(num_circles):
        center = np.random.randint((0,0), img_shape)
        radius = np.random.randint(10, 20)
        rr, cc = disk(center, radius, shape=img_shape)
        if not np.any(objects[rr, cc]):
            objects[rr, cc] = 1

    # draw blue rectangles
    num_rect = int(max(np.random.randn()*4+100, 0))
    for i in range(num_rect):
        sizes = np.random.randint((20,20),(30,30))
        startpoint = np.random.randint((0,0), img_shape-sizes)
        endpoint = startpoint + sizes
        rr, cc = rectangle(startpoint, endpoint, shape=img_shape)
        if not np.any(objects[rr, cc]):
            objects[rr, cc] = 2

    # add some noiseness
    sd = 30
    bg = objects==0
    fg = np.logical_not(bg)
    noise = np.random.randn(*img_shape)
    img = np.zeros((*img_shape, 3), dtype=np.uint8)
    for c in [0,1,2]:
        img[:,:,c] = offset[c] - sd - noise*10
    img[objects==1,0] = offset[0] + sd + noise[objects==1]*10
    img[objects==2,2] = offset[2] + sd + noise[objects==2]*10
    
    return img