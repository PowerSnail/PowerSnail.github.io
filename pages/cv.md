---
layout: page
show_meta: false
title: "Han Jin"
permalink: "/cv/"
---

## Education

University of Virginia, Charlottesville, VA
Bachelor of Science, Computer Science, 2018

## Skills

### Programming Languages

Python, C++, Java, Ruby, C#, C, Bash

### Machine Learning Framework

Tensorflow/Keras, Pytorch

### Web Framework

Django

## Research

**Automatically Co-locating Data Sensors in Buildings**  
_2018 - present_

Apply machine learning to raw sensor data with python and Tensorflow, that group sensors
based on their location with accuracy as high as 96%. The method

1. Extracts features from raw sensory data with canny edge detection

2. Encodes signal that maximizes the Pearson Correlation Coefficient difference between
in-group and out-group sensors, with a CNN-based Siamese network trained by Triplet loss

3. A genetic algorithm that clusters sensor to maximize the mean intra-group correlation
coefficients, which is faster than Integer Linear Programming (linear vs. exponential
complexity), and more accurate than approximation by Linear Programming and simulated 
annealing (both proposed by previous work).

## Work Experience

**Student Intern (Reinforcement Learning) at Happy Elements**  
_2017 Summer_

Assisted in building, improving, and accelerating an AI player in python with Tensorflow
for a modern mobile game, achieving better winning rate (from ~23% to ~70%, higher than
average human), and 4 – 5 times better performance, by changing the training program and
model:

- Distributed work across servers with asynchronous workers and backpropagations;
- Implemented Gradients broadcast without centralized parameter server;
- Refactored the architecture to fully convolutional, with less overfitting, earlier
convergence, and better score.


**Teaching Assistant for CS 2102 (Discrete Math) at University of Virginia** 
_2015 Spring – 2016 Spring_

Assisted in the teaching of multiple semesters of CS 2102 (Discrete Mathematics) by
grading examinations, hosting office hours, and pre-viewing some assignment questions.

## Project

**Ticket-To-Ride AI Player**
_2016 Summer_

Created an AI player (Java) for Ticket-To-Ride that won the first place in the class 
tournament, by modeling the game with Markov Decision Process.

**Randot Studio**
_2018_

Created a desktop application that helps generating stereo-images for ophthalmology 
tests with Python and Qt. It draws stereo symbols with fully customizable size, color, 
stereo depth, orientation, and places. It generates two formats of stereoimage: plain 
PNGs and randot images (filled with randomly placed pixels).


Interpreter for Classroom Object Oriented Language 2017 Spring
Created a lexer, a parser, a type system, and interpreter for COOL. It efficiently evaluated a COOL program, could
produce annotated AST, and had some debugging capability. The core of the program was written in OCaml.
POSIX Shell 2017 Fall
Wrote a simple shell that can evaluate user input and execute proper program in a separate process. The program was
written in C++ on Linux, using POSIX interface for system calls.
PUBLICATION
Co-authored a paper on the application of 3D Shutter Glass Technology in eye examination.
Wu, H., Jin, H., Sun, Y., Wang, Y., Ge, M., Chen, Y., & Chi, Y. (2016). Evaluating stereoacuity with 3D shutter glasses
technology. BMC Ophthalmology BMC Ophthalmol, 16(1). doi:10.1186/s12886-016-0223-3