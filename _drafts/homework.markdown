## 10.1 Definition

Let $\vec{u}, \vec{v}$ and $\vec{w}$ be elements of a vector space $V$, and let $c$ be a scalar. An **inner product** on $V$ is a function that takes two vectors in $V$ as input and produces a scalar as output. An inner product function is denoted by $<\vec{u}, \vec{v}>$ and must satisfy the following conditions:

1. $<\vec{u}, \vec{v}> = <\vec{v}, \vec{u}>$
2. $<\vec{u} + \vec{v}, \vec{w}> = <\vec{u}, \vec{w}> + <\vec{v}, \vec{w}>$
3. $<c\vec{u}, \vec{v}> = <\vec{u}, c\vec{v}> = c<\vec{u}, \vec{v}>$
4. $<\vec{u}, \vec{u}> \geq 0$, and $<\vec{u}, \vec{u}>=0$ only when $\vec{u} = 0$

A vector space $V$ with an innner product defined on it is called an **inner product space**.

## 10.2 Definition

Two vector $\vec{U}$ and $\vec{v}$ in an inner product space $V$ are **orthogonal** if an donly if $<\vec{u}, \vec{v}> = 0$.

## 10.3 Definition

Let $\vec{v}$ be a vector in an inner product space $V$. Then the **norm** of $\vec{v}$ is given by
$$||\vec{v}||=\sqrt{<\vec{v}, \vec{v}>}$$

## 10.4 Theorem

Let $\vec{u}$ and $\vec{v}$ be vectors in an inner product space $V$. Then $\vec{u}$ and $\vec{v}$ are orthogonal if and only if
$$||\vec{u}||^2 + ||\vec{v}||^2 = ||\vec{u} + \vec{v}||^2$$

## 10.5 Definition

Let $\vec{u}$ and $\vec{v}$ be vectors in an inner product space $V$, with $\vec{v}$ nonzero. Then the **projection of $\vec{u}$ onto $\vec{v}$** is given by
$$proj_{\vec{v}}\vec{u}=\dfrac{<\vec{v}, \vec{u}>}{<\vec{v}, \vec{v}>}\vec{v} = \dfrac{<\vec{v}, \vec{u}>}{||\vec{v}||^2}\vec{v}$$

## 10.6 Theorem

Let $\vec{u}$ and $\vec{v}$ be vectors in an inner product space $V$, with $\vec{v}$ nonzero, and let $c$ be a nonzero scalar. Then

1. $proj_\vec{v} \vec{u}$ is in $span\{v\}$.
2. $\vec{u} - proj_\vec{v} \vec{u}$ is orthogonal to $\vec{v}$.
3. If $\vec{u}$ is in $span\{\vec{v}\}$, then $\vec{u} = proj_\vec{v} \vec{u}$.
4. $proj_\vec{v} \vec{u} = proj_{c\vec{v}} \vec{u}$

## 10.7 Theorem

For all $\vec{u}$ and $\vec{v}$ in an inner product space $V$.

$$ |<\vec{u}, \vec{v}>| \leq ||\vec{u}||\cdot||\vec{v}||$$

## 10.8 Theorem

For all $\vec{u}$ and $\vec{v}$ in an inner product space $V$,

$$ ||\vec{u} + \vec{v}|| \leq ||\vec{u}|| + ||\vec{v}||$$
