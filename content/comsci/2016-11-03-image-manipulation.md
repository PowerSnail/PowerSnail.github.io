---
layout: page
title: "Gradient Detection Convolutions, Seam Carving, and Patch March"
tags:
    - graphics
    - notes
date: "2016-11-03"
---

## gradient detection convolutions

Square instead of rectangle: to avoid problems concerning diagonal
  - usually 3 x 3

## edge detection

- apply gradient detection convolution
- find where gradient appears


```

 / \    / \    / \   / \
  |      |      |     |
 _____________________________  <- at this line, the gradient is extreme
 ******************************
 ******************************
 ******************************
```


- find maximum gradient points
- edge is perpendicular to gradients

## Segmentation: Intelligent Scissors

INPUT: a set of points
OUTPUT: find a path(curve) that is following edge as much as possible

This is a graph traversal problem. Each pixel has some neighbors, and we choose points based on gradient at each point.

ALGORITHM

- treat the picture as a graph
- each pixel is connected to neighboring pixels
- cost minimization
  - cost = 1 - gradient  // higher gradient, better to choose
  - optionally, cost for diagonal is higher, etc.
- simply adding up cost of each step

## Segmentation: k-means

automatic algorithm: k neighbor

It finds pixels that are close in color-space & geometry, and connect them. By tweaking the weight of adjacency and color-space closeness, we can have different results. This can be used in color reduction. It reduces the amount of gradient exists in the graph.

[segmentation](https://en.wikipedia.org/wiki/Image_segmentation)

## Image Processing Algorithms: Machine Learning

### Machine Learning Model

A black box, that takes in independent and dependent vars, and output a function that describes the relationship between those.

$$Black-Box(x, y) \to y = f(x)$$

### In Image Processing

- Independent var: features of the image
- Dependent var: classification(is it a dog?)

To find features, we try to find patterns of gradient in the image.

There are parts of the image that are more informative than others. It contains patterns that are robust against small changes. It will be stable across different images sharing the same pattern, despite small differences.

This could be represented by:

- maxima of gradient
- area of gradient turns

These are works for feature detection algorithms.

For example, a gray box.

This is easily identified, because the right angles of the square corners are a robust feature. The change in gradient pattern is consistent in different images.

## Seam Carving

- INPUT: Image
- OUTPUT: Smaller image, that does not look distorted.

Requirement:

- focus objects are in frame
- no obvious distortion
- only boring parts are cut off

[Seam Carving](https://en.wikipedia.org/wiki/Seam_carving)

Use magnitude of gradient to approximate the "interestingness".

- large gradient: an object -> interest
- low gradient: same across image -> less information

In order to get a better estimate, we might need to blur the image a little bit.

*NOTE: the reason that the gradient image on Wikipedia has squares is because JPEG compression*

**How to decide what to remove?**

In order to narrow an image for 1 pixel, every row needs to be smaller by 1 pixel.

1. For each row, pick the least interesting pixel
  - [FAILED]
  - line shifts, and the image will be distorted

2. Select one vertical line
  - [FAILED]
  - This will create a visible vertical line of discontinuous

3. Make sure that pixels removed are *adjacent* to each other
  - [CORRECT]
  - After selecting one pixel, select one of the 3 pixels below it.
  - Pick first pixel:
    - dynamic programming
    - minimize cost from first row to each pixel of the next row
    - for each pixel, we have a `prev`, and a minimized accumulative cost
    - at the last row, find the smallest accumulative cost, and follow the `prev`s back up to generate the path to be cut.

**Enlarging the image with the same algorithm**

Duplicate paths, from the lowest cost path to higher ones in the **original image**.

But this is less well-defined. Because we need to add details, there are many complications. The one rule is not to duplicate the same path over and over again.

## Patch March

- look at the hole's boundary
- find patches in the image that matches the best with the boundary's patches
- fill the area with the patches inwards

### find one patch

- ||patch - image||
- ||patch.gradient - image.gradient||

### the whole hole

It is only after the hole is filled, do we know whether this is done well.

It works well when there are plenty of similar patterns, it will work well.

Removing a part of a critical component, nose from the face for example, cannot work.

### random selection of patches

Randomly replacing patches with better patches, until the whole patched area is smoothly integrated.

Because there are too many choices, we use randomized search to iteratively improve the patch quality.

Heuristics, for example interpolated color gradient, can be used as an initial guess.

Another improvement could be giving the algorithm more images to draw patches from.

### applications

- remove whole persons from the scene
- replace a person from the scene

### computer detection of tempering

- Although human cannot see some anomalies, computers can detect them
- 3D Geometric features:
  - shadow length / light source angle























































