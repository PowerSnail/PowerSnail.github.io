---
title: "Plants"
tags:
    - graphics
    - notes
date: "2016-11-10"
slug: "drawing-plants"
---



## Turtle Graphics

A turtle with a pen and draws a line along the path it moves. It receives commands like "forward", "turning left", etc. 

A tree can be drawn by a turtle with the commands: `T = F L T R R T L B`.

An L-System can be described using this turtle. 

## Trend in Graphics

Planes: *Good!*

 - Ops, *Bad*

Fractals!: *Good!*

 - Ops, *Bad*

How **nature** does it? *Now we understand it!*

 - Build a simulation, but it turns out to be a bad one
 - As a result, we are exploring increasingly complex simulations/models of the nature. 


### How to model a tree?

Woody Plants:

- Buds: where growth happens
- Tip: One active tip at a time, all further growth occur here.

Branching:

- Side-Buds grows into branches.

#### Simpler Model: Vines

They do not branch unless it is snipped. When a vine is snipped, the next available bud will become the new tip, and starts growing there. This is called **reiteration**. 

#### Branching Model

- Active Bud: Seek up and light
- All Bud has a chance to branch
- Reiteration: snipping and go to the next available tip

### 2D Model

Elements:

- branches
- old buds (in case of reiteration)
- active buds
- The paths to each bud

This can be easily modelled by a Computer Science Tree. 

Pruning: Move the pointer of active buds to the next node closer to root after the cut. 


Side Bugs will have their own growth over time. 


### Basic Structure of Plants

#### Trunk


- Outer Bark
- Inner Bark
- Live Wood
- Core

The outer bark are dead tissues, that are cracked when the inner parts grow larger. The thickness, cracking patterns, etc. all have impacts on the exact outcome of the growth of barks. 

Usually, we photograph the bark, and use the photo as a texture, or even with depth information. Then we patch the photograph all over the trunk. 

#### Leaves

Most leaves have simple structures. They either have parallel veins, or a principal vein with side veins. 

![two types of leaves](https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&cad=rja&uact=8&ved=0ahUKEwjL26nbvp7QAhUJ5iYKHU-ZC2UQjRwIBw&url=http%3A%2F%2Fwww.cactus-art.biz%2Fnote-book%2FDictionary%2FDictionary_V%2Fdictionary_vein.htm&bvm=bv.138169073,d.amc&psig=AFQjCNHAFlfCJVIDpQdWhr5hfzpHQckNkw&ust=1478877646424834)

Leaves are hard to draw, not because of the shape, but because leaves are designed to absorb light. It has to let the light in but little light out.

Four things affect its appearance:

- Surface
- Thickness
- Translucency
- Layers

##### Surface

Some leaves have a tendency to dry, by having either wax or fur. Wax results in high reflectivity. Therefore, there has to be a lot of shine. This is just specularity for modelling. Fur, on the other hand, is complicated. When furs, especially short furs, are struck by light, it is more interesting. Example of furry plants: Peach Fruit
![peach](http://www.fumari.com/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/h/o/hookah-tobacco-white-peach.png)

It is more fuzzy when the angle is getting perpendicular to our plane, because there are more furs that light has to travel through. When we model it, we have two colors, for surface and for furs independently, mixed according to the angle between the *Normal* of surface and *eye* vector. i.e. $$\nabla N \cdot \nabla e$

##### Thickness

Sub-surface Scattering occurs in leaves, and the thicker the leaves are, the more light bounces inside the leaves. Moreover, there is chlorophyll inside the leaves that absorb different light wavelengths. 

##### Translucency

This is dependent on the concentration of chlorophyll. The less chlorophyll, the more transparent the leaves are.

##### Layers

In some leaves, there are reflective layers below the chlorophyll layer, so light can be reflected and passes chlorophyll layer twice. 

## Pixar Short Film: Lifted

Tree Scene: Light through trees

How to do this?

A Big Clutter of fractal structure, plus some surface finishing. Then, just simulate the light travel through the tree.  




































