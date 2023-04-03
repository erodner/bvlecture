import numpy as np
from skimage.draw import rectangle, polygon
import matplotlib.pylab as plt

try:
    from skimage.draw import disk
except:
    try:
        from skimage.draw import circle
    except:
        pass
     

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
        rr, cc = circle(center[0], center[1], radius, shape=img_shape)
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

def rect_image_with_ground_truth():
    """ This function generates a rotated rectangle in the center of an image """
    img_shape = np.array((512, 512))
    objects = np.zeros(img_shape)
    h, w = np.random.randint(80, 230, (2))
    c_point = img_shape/2.0
    points = np.array([ [w,h], [w,-h], [-w,-h], [-w,h] ]) / 2.0
    theta = (np.random.rand()-0.5)*np.pi/2.0
    R = np.array([[ np.cos(theta), np.sin(theta)], [-np.sin(theta), np.cos(theta)]])
    r_points = c_point + np.dot(points, R)
    rr, cc = polygon(r_points[:,1], r_points[:,0], shape=img_shape)
    objects[rr, cc] = 128
    
    # add some noiseness
    sd = 30
    bg = objects==0
    fg = np.logical_not(bg)
    noise = np.random.randn(*img_shape)
    objects[fg] += noise[fg]*20
    objects[bg] += noise[bg]*50 + 30
    
    objects[objects>255] = 255
    objects[objects<0] = 0
    objects = objects.astype(np.uint8)
    
    
    return objects, theta, h, w

def rect_image():
    """ returns an image of a rotated rectangle """
    img, _, _, _ = rect_image_with_ground_truth()
    return img

def print_stats(desc, errors):
    """ simple function to output statistics of a list/array """
    print (f"{desc} min: {np.min(errors)}")
    print (f"{desc} max: {np.max(errors)}")
    print (f"{desc} mean: {np.mean(errors)}")

def test_algorithm(my_algorithm, num_tests=10):
    """ this function generates synthetic images and compares the
        image processing result with the ground-truth """
    len_error = []
    theta_error = []
    for i in range(num_tests):
        img, theta, h, w = rect_image_with_ground_truth()
        print (f"{i}: {h} x {w} {theta}")
        try:
            a_len_sorted, a_orientation = my_algorithm(img)
        except:
            plt.figure()
            plt.imshow(img)
            plt.show()
            raise
        
        print (f"{i}= {a_len_sorted[0]} x {a_len_sorted[1]} {a_orientation}")
        theta_error.append(np.abs(theta-a_orientation))
        len_error.append(np.linalg.norm(np.array(a_len_sorted) - np.array(sorted([h,w]))))
        
    print_stats("Orientation angle error", theta_error)
    print_stats("Length error", len_error)