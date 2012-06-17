#!/bin/env python

import numpy as np
from scipy.ndimage.filters import laplace 
from PIL import Image

import sys

def cost(image):
    return laplace(image)**2

def find_seams(image):
    print "Finding seams"
    im_w, im_h = image.shape
    seams_raw = {}
    costs = {}
    for y in range(image.shape[1]):
        costs[(0, y)] = image[1, y]
    for x in range(image.shape[0]):
        costs[(x, -1)] = np.inf
        costs[(x, image.shape[1])] = np.inf
    for x in range(1, image.shape[0]):
        for y in range(image.shape[1]):
            m = min(costs[x-1,y-1], costs[x-1,y], costs[x-1,y+1])
            costs[(x, y)] = m + image[x,y]
            if m == costs[x-1, y]:
                seams_raw[(x,y)] = (x-1, y)
            elif m == costs[x-1, y-1]:
                seams_raw[(x,y)] = (x-1, y-1)
            elif m == costs[x-1, y+1]:
                seams_raw[(x,y)] = (x-1, y+1)

    seams = {}
    i = image.shape[0]-1
    min_cost = np.inf
    for j in range(image.shape[1]):
        path = [(i,j),]
        total_cost = 0
        x, y = i, j
        try:
            while x > 0:
                total_cost += costs[x, y]
                if total_cost > min_cost:
                    raise KeyError
                x,y = seams_raw[(x,y)]
                path.append((x,y))
        except KeyError:
            continue
        total_cost += costs[x, y]
        if y in seams and total_cost > seams[y]["cost"]:
            continue
        seams[y] = {"start":j, "cost":total_cost, "path":path}
    return sorted(seams.values(), key=lambda x : x["cost"])

def remove_path(image, path):
    print "Removing Path"
    im_w, im_h, im_c = image.shape
    image[zip(*path)] = -1
    return image[image>=0].reshape((im_w, im_h-len(path)//im_w, im_c))

def stretch_path(image, paths):
    print "Stretching Path"
    im_w, im_h, im_c = image.shape
    image_new = np.concatenate((image, np.zeros((im_w,len(paths)//im_w, im_c))), axis=1)
    for x, y in paths:
        # This statement deals with if we have already made changes in this row
        y_orig = y
        while np.any(image[x,y_orig] != image_new[x,y]):
            y += 1
        interpolated = (np.sum(image_new[x,y-1:y+2], axis=0)+np.sum(image_new[x-1:x+2,y], axis=0))/6.
        image_new[x,:,:] = np.vstack((image_new[x,:y], interpolated.reshape((1,3)), image_new[x, y:-1]))
    return image_new

def resize(image, dim):
    print "Resizing"
    todo = [True, True]
    while any(todo):
        if dim[1] != image.shape[1]:
            virtical_seams = find_seams(cost(image.sum(axis=-1)/3.))
            num_needed = abs(image.shape[1]-dim[1])
            print "Found %d vert seams (%d more)"%(len(virtical_seams), num_needed)
            allpaths = reduce(lambda a,b : a+b, (seam["path"] for seam in virtical_seams[:num_needed]))
            if dim[1] < image.shape[1]:
                image = remove_path(image, allpaths)
            else:
                image = stretch_path(image, allpaths)
        else:
            todo[1] = False

        if dim[0] != image.shape[0]:
            horizontal_seams = find_seams(cost((image.sum(axis=-1)/3.).T))
            num_needed = abs(image.shape[0]-dim[0])
            print "Found %d horiz seams (%d more)"%(len(horizontal_seams), num_needed)
            allpaths = reduce(lambda a,b : a+b, (seam["path"] for seam in horizontal_seams[:num_needed]))
            if dim[0] < image.shape[0]:
                image = remove_path(image.swapaxes(0,1), allpaths).swapaxes(0,1)
            else:
                image = stretch_path(image.swapaxes(0,1), allpaths).swapaxes(0,1)
        else:
            todo[0] = False

    Image.fromarray(image.astype('uint8')).save("out.png")

if __name__ == "__main__":
    filename = sys.argv[1]
    width = int(sys.argv[2])
    height = int(sys.argv[3])

    im = Image.open(filename)
    image = np.asarray(im, dtype=np.float)

    resize(image, (width, height))

