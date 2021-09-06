---
layout: page
title: "Count 1s in Range"
categories:
    - comsci
tags:
    - computer science
    - algorithm
    - codefights
    - C++
mathjax: true
isCJKLanguage: true
lang: zh
---

在 codefights 上做到了一个很有意思的题。给你 a, b 两个数，假设你构建了一个从 a 到 b 的 array，所有这些数的 binary representation 里面有多少个 1？

# Naive Solution

最简单的办法 (随手翻了两个别人的答案都是这个), 就是一个数一个数查有多少 1. 笨一点的手工查, 聪明一点的用 built-in function 查. 但是无论如何, 复杂度都是 O(b - a).

# Log(n) Solution

我们先思考一个简化版本的问题: 所有 `unsigned int (c++)` 里面有多少 1? 答案是所有的 bit / 2, 因为当我们把所有数都写成 2 进制, 一半是 1, 一半是0.

我们 generalize 一下: 对于任意的 $m$, 所有 $m$ 位的正整数里有 $(2^m * m) / 2$.

当我们的上限不是*位数*，而是一个数字 $b$, 我们可以把 $b$ 分成 3 各部分。假设 $b$ 不为 0, $b$ 的二进制形式应该是 $1xxxx$... 假设 $b$ 有 $m + 1$ 位.

现在以 $100...0$ 为 `line`:

1. **line** 一个 '1'
2. **below line**: 所有 $m$ 位数有$ (2^m * m) / 2$ 个 '1'. 这个数从前面的结论得来.
3. **above line**: 除去最左边的 $1$， 右边的部分又变成从 $0$ 开始查. 我们可以用一个简单地递归来解决这个部分。

pseudo code:

```ruby
function allBits(b) {
    if (b < 0) return 0; // 不考虑负数
    if (b < 2) return b; // basecase: 只有一位

    m = num_of_bits(b) - 1;
    line = 1 << m;
    onesBelowLine = m * (line - 1) / 2;
    onesAboveLine = allBits(b - line) + (b - line);

    return 1 + onesBelowLine + onesAboveLine;
}
```

下面回到原始问题，给定底线和上限，a, b， 我们可以简单地转换一下：

```ruby
function rangeBitCount(a, b)
{
    return allBits(b) - allBits(a);
}
```

# 复杂度证明

这个算法的复杂度很简单，因为这个 recursion 可以很容易的转换成 tail recursion，再变成复杂度相同的 iteration. 这个 iteration 每次去掉最高位的 1，因此最多有 $\log(b)$ 次循环；每次循环做了 constant 的基本算数，因此最后的复杂度应该是 $\log(b)$。


# C++ Source Code

```cpp
int allBits(int b) {
    if (b < 0) return 0;
    if (b < 2) return b;
    int num_bit = 31 - __builtin_clz((unsigned) b);
    int line = (1 << num_bit);
    int count_below = (num_bit * line) / 2;
    int above = b - line;
    int count_above = above + allBits(above);
    return count_above + count_below + 1;
}

int rangeBitCount(int a, int b) {
    return allBits(b) - allBits(a - 1);
}
```
