---
layout: page
title: "Linear Algebra Notes - Definitions & Theorems"
categories:
    - studies
tags:
    - linear algebra
    - notes
---

Information is based on [Linear Algebra with Applications](https://www.amazon.com/Loose-leaf-Version-Linear-Algebra-Applications/dp/1464131821) by Jeffrey Holt.

## System of Equations

### Definition 1.1

A system of linear equations is a collection of equations of the form

$$a_{11}x_{1} + a_{12}x_{2} + ... + a_{1n}x{n} = b_1$$

### Theorem 1.2

A system of linear equations has no solutions, exactly one solution, or infinitely many solutions.

### Definition 1.3

A linear system is in echelon form if

1. Every variable is the leading variable of *at most* one equation.
2. The system is organized in a descending "stair step" pattern so that the index of the leading variables increases from the top to bottom.
3. Every equation has a leading variable.

### Definition 1.4

A matrix is in **echelon form** if

1. Every leading term is in a column the left of the leading term of the row below it
2. Any zero rows are at the bottom of the matrix

### Definition 1.5

A matrix is in **reduced (row) echelon form** (RREF) if

1. it is in echelon form
2. all pivot positions contain a "1"
3. the only nonzero term in a pivot column is in the pivot position

### Theorem 1.6

A given matrix is equivalent to a unique matrix that is in reduced row echelon form.

## Vectors

### Definition 2.1

A **vector** is an ordered list of real numbers $u_1, u_2, ..., u_n$ expressed as

$$\pmb{u}= \begin{bmatrix} u_1 \\ u_2 \\ ... \\ u_n \end{bmatrix}$$

or as $\pmb{u}=(u_1, u_2, ..., u_n)$. The set of all vectors with _n_ entries is denoted by $\mathbb{R}^n$.

### Definition 2.2

Let $\pmb{u}$ and $\pmb{v}$ be vectors in $\mathbb{R}^n$ given by

$$\pmb{u} = \begin{bmatrix} u_1 \\ u_2 \\ ... \\ u_n \end{bmatrix} \text{ and } \pmb{v} = \begin{bmatrix} v_1 \\ v_2 \\ ... \\ v_n \end{bmatrix}$$

Suppose that $c$ is a real number, called a **scalar** in this context. Then we have the following definitions:

**Equality** $\pmb{u} = \pmb{v}$ if and only if $u_1 = v_1$, $u_2 = v_2$...

**Addition** $$\pmb{u} + \pmb{v} = \begin{bmatrix} u_1 \\ u_2 \\ ... \\ u_n \end{bmatrix} + \begin{bmatrix} v_1 \\ v_2 \\ ... \\ v_n \end{bmatrix} = \begin{bmatrix} u_1 + v_1 \\ u_2 + v_2 \\ ... \\ u_n + v_n \end{bmatrix}$$

**Scalar Multiplication** $$c\pmb{u} = c\begin{bmatrix} u_1 \\ u_2 \\ ... \\ u_n \end{bmatrix} = \begin{bmatrix} c\cdot u_1 \\ c\cdot u_2 \\ ... \\ c\cdot u_n \end{bmatrix}$$

The set of all vectors in $\mathbb{R}^n$, taken together with these definitions of addition and scalar multiplication, is called **Euclidean space**.

### Theorem 2.3: Algebraic Properties of Vectors

Let $a$ and $b$ be scalars, and $\pmb{u}$, $v$, and $w$ be vectors in $\mathbb{R}^n$. Then

1. $\pmb{u} + \pmb{v} = \pmb{v} + \pmb{u}$
2. $a(\pmb{u} + \pmb{v}) = a\pmb{u} + a\pmb{v}$
3. $(a + b) \pmb{u} = a\pmb{u} + b\pmb{u}$
4. $(\pmb{u} + \pmb{v}) + \pmb{w} = \pmb{u} + (\pmb{v} + w)$
5. $a(b\pmb{u}) = (ab)\pmb{u}$
6. $\pmb{u} + (-\pmb{u}) = 0$
7. $\pmb{u} + 0 = 0 + \pmb{u} = \pmb{u}$
8. $l\pmb{u} = \pmb{u}$

### Definition 2.4

If $u_1, u_2, ..., u_m$ are vectors and $c_1, c_2, ..., c_m$ are scalars, then

$$c_1 \pmb{u}_1 + c_2 \pmb{u}_2 + ... + c_m \pmb{u}_m$$

is a **linear combination** of the vectors. Note that it is possible for scalars to be negative or equal to zero,

### Definition 2.5

Let ${u_1, u_2, ..., u_m}$ be a set of vectors in $\mathbb{R}^n$. The **span** of this set is denoted $span\{u_1, u_2, ..., u_m\}$and its defined to be the set of all linear combinations

$$x_1 \pmb{u}_1 + x_2 \pmb{u}_2 + ... + x_m \pmb{u}+m$$

where $x_1, x_2, ..., x_m$ can be any real numbers.

### Theorem 2.6

Let $\pmb{u}_1, \pmb{u}_2, ..., \pmb{u}_m$ and $\pmb{v}$ be vectors in $\mathbb{R}^n$. Then $\pmb{v}$ is an element of $span\{\pmb{u_1}, \pmb{u_2}, ..., \pmb{u_m}\}$ if and only if the linear system represented by the augmented matrix

$$\begin{bmatrix}\pmb{u_1} & \pmb{u_2} & ... &\pmb{u_m} & \pmb{v}\end{bmatrix}$$

has a solution.

### Theorem 2.7

Let $\pmb{u}_1, \pmb{u}_2, ..., \pmb{u}_m$ and $\pmb{u}$ be vectors in $\mathbb{R}^n$. If $\pmb{u}$ is in $span\{\pmb{u}_1, \pmb{u}_2, ..., \pmb{u}_m\}$, then $span\{\pmb{u}, \pmb{u}_1, \pmb{u}_2, ..., \pmb{u}_m\} = span\{\pmb{u}_1, \pmb{u}_2, ..., \pmb{u}_m\}$.

### Theorem 2.8

Let ${\pmb{u}_1, \pmb{u}_2, ..., \pmb{u}_m}$ be a set of vectors in $\mathbb{R}^n$. If $m < n$, then this set does not span $\mathbb{R}^n$. If $m \geq n$, then the set might span $\mathbb{R}^n$ or it might not. In this case, we cannot say more without additional information about the vectors.

<a name="2.9"></a>

### Definition 2.9

Let $ \pmb{a}_1, \pmb{a}_2, ..., \pmb{a}_m$ be vectors in $\mathbb{R}^n$. If

$$A = \begin{bmatrix} \pmb{a}_1 & \pmb{a}_2 & ... & \pmb{a}_m \end{bmatrix} \text{ and }\pmb{x}=\begin{bmatrix} x1 \\ x2 \\ ... \\ xm \end{bmatrix}$$


then $A \pmb{x} = x_1 \pmb{a}_1 + x_2 \pmb{a}_2 + ... + x_m \pmb{a}_m$.

### Theorem 2.10

Let $ \pmb{a}_1, \pmb{a}_2,..., \pmb{a}_m$ and $\pmb{b}$ be vectors in $\mathbb{R}^n$. Then the following statements are equivalent. That is, if one is true, then so are the others, and if one is false, then so are the others.

1. $\pmb{b}$ is in $span\{\pmb{a}1,\pmb{a}2,...,\pmb{a}m\}$.
2. The vector equation $x_1 \pmb{a}_1 + x_2 \pmb{a}_2 + ... + x_m \pmb{a}_m = \pmb{b}$ has at least one solution.
3. The linear system corresponding to $\begin{bmatrix} \pmb{a}_1 & \pmb{a}_2 & ... & \pmb{a}_m & \pmb{b}\end{bmatrix}$ has at least one solution.
4. The equation $A \pmb{x} = \pmb{b}$, with $A$, and $\pmb{x}$ given as in [Definition 2.9](#2.9).

### Definition 2.11

Let ${ \pmb{u}_1,  \pmb{u}_2, ...,  \pmb{u}_m}$ be a set of vectors in $\mathbb{R}^n$. If the only solution to the vector equation

$$ x_1 \pmb{u}_1,  x_2 \pmb{u}_2, ...,  x_m \pmb{u}_m = \pmb{0}$$

is the trivil solution given by $x_1 = x_2 = ... = x_m = 0$, then the set ${ \pmb{u}_1   \pmb{u}_2  ...   \pmb{u}_m}$ is **linearly independent**. If there are nontrivial solutions, then the set is **linearly dependent**.

### Theorem 2.12

Suppose that ${\pmb{-}, \pmb{u}_1 , \pmb{u}_2 , ... , \pmb{u}_m}$ is a set of vectors in $\mathbb{R}^n$. Then the set is linearly dependent.

### Theorem 2.14

Let ${\pmb{u}_1 , \pmb{u}_2 , ... , \pmb{u}_m}$ be a set of vectors in $\mathbb{R}^n$. Then the set is linearly dependent if and only if one of the vectors in the set is in the span of the other vectors.

### Theorem 2.15

Let $A = \begin{bmatrix} \pmb{a}_1 & \pmb{a}_2 & ... & \pmb{a}_m \end{bmatrix}$ and $\pmb{x} = (x_1 , x_2 , ... , x_m)$. The set ${ \pmb{a}_1 ,  \pmb{a}_2 ,  ... ,  \pmb{a}_m}$ is linearly independent if and only if the homogeneous linear system

$$A \pmb{x} = \pmb{0}$$

has only the trivial solution.

### Theorem 2.16

Suppose that $A = \begin{bmatrix} \pmb{a}_1 & \pmb{a}_2 & ... & \pmb{a}_m \end{bmatrix}$, and let $\pmb{x} = (x_1 , x_2 , ... , x_m)$ and $\pmb{y} = y_1 , y_2 , ... , y_m$. Then

1. $A (\pmb{x} + \pmb{y} ) = A \pmb{x} + A \pmb{y} $
2. $A (\pmb{x} - \pmb{y} ) = A \pmb{x} - A \pmb{y} $

### Theorem 2.17

Let $\pmb{x}_p$ be a particular solution to

$$A \pmb{x} = \pmb{b}$$

Then all solution $\pmb{x}_g$ to it have the form $ \pmb{x}_g - \pmb{x}_p + \pmb{x}_h$, where $\pmb{x}_h$ is a solution to the associated homogeneous system $A \pmb{x} = \pmb{0}$.

### Theorem 2.19: The Big Theorem - Version 1

Let $\mathcal{A} = { \pmb{a}_1 ,  \pmb{a}_2 , ... ,  \pmb{a}_m}$ be a set of $n$ vectors in $\mathbb{R}^n$, an dlet $A = \begin{bmatrix} \pmb{a}_1 & \pmb{a}_2 & ... & \pmb{a}_m \end{bmatrix}$. Then the followign are equivalent:

1. $\mathcal{A}$ spans $\mathbb{R}^n$.
2. $\mathcal{A}$ is linearly independent.
3. $A \pmb{x} = \pmb{b}$ has a unique solution for all $ \pmb{b}$ in $\mathbb{R}^n$.

















<!-- line -->
