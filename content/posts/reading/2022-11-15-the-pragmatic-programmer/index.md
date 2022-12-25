---
title: The Pragmatic Programmer 
description: 
date: 2022-11-15
slug: the-pragmatic-programmer
tags:
  - book
  - computer science
  - reading
draft: true
---

The book: [The Pragmatic Programmer](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/).

What an informative, well-written book. I found this gem while I was combing through the Newark Public Library, which is not so big, but still has quite a few good books. 

_The Pragmatic Programmer_ is not only packed with information, but also supplies real-code example (not pseudocode, not English description of algorithm) to demonstrate what it means. I don't want to over-sell the book; they are short, toy examples. If one wants to fully grasp the how and why of all the concepts, one needs to read more and code more. But the snippets of real code provides a comfortable starting point.

At 40 USD, this is a book that I would recommend keeping on your shelf, if shelf space isn't too much of a problem. Leafing through the book once a while can be a good reminder of some of the most important disciplines in software development.

The author advocates for _orthogonality_, the independence between components. Orthogonality makes it easier and safer to change code, as changing one component would ideally not affect other components. In reality, I find that this is very hard to do. Unless it's some sort of bug fix or performance fix, it's very difficult to completely isolate a change to just _one_ component. But a good architecture usually minimize the amount of code that has to be touched.

Global state, including singleton, is coupling. 

Another interesting point is the _tracer bullet_ method for starting a new projecting, an end-to-end methodology. A complex project usually have multiple layers or components, and we have to choose where to start. We could do it with a top-down approach: design the overall architecture and start filling the blank, or with a bottom-up approach: design and code individual components, which are linked together later. Both approaches have the problem that the system can only be up and running after the majority of the work gets done. 

The tracer-bullet method attacks the project like a bullet piercing through layers of obstruction: from one end to the other. We pick the most fundamental requirement, and implement all the code required, regardless of how many components have to be touched. We'll end up with many unfinished components, but the system is ready to run. This makes it possible to start writing integrated tests, confirming that the architecture and tool chains actually works together, and gather feedbacks from customers. Then, we go down the requirements by their priority, gradually fleshing out the half-written components. 

In reality, this might mean scaffolding the front-end, the back-end, and the database right in the beginning. The very first thing is to implement the most important functionality required by the customer, and it has to have a UI, and goes all the way to the database. Not fake buttons, not mocked API. Real data, real servers, real functions.




