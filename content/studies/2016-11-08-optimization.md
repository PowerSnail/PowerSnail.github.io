---
layout: page
title: "Code Optimizations"
categories:
    - studies
tags:
    - com arc
    - notes
date: "2016-11-08"
---

An example: **Transpose**

```ruby
for i in rows
    for j in cols
        b[i][j] = a[j][i]
```

However, it might be the case that we do not know the size at *compilation time*, so we cannot statically declare this 2D array. Therefore, for this to work, `b[i][j]` needs to be a pointer to an array.

To optimize, we usea 1-D array by flattening the table:

```ruby
a[i][j] -> a[i * N + j]
```

In order to make this statement more readable, we define a macro:

```c
# define RIDX(i, j, N) (i * N + j)

```

This macro will do a pure text replacement that replace all occurrence of `RIDX(i, j, N)` by `(i * N + j)`.

For readability, let us assume that we can write `b[i, j]` for this.

### Which one is better?

`b[i, j] = a[j, i]` vs. `b[j, i] = a[i, j]`

| |Temperal Locality| Spacial Locality |
|---|---|---|
| `b[i, j]` | No | Yes |
| `a[j, i]` | No | No |
| `b[j, i]` | No | No |
| `a[i, j]` | No | Yes |

So, either is bad.

In order to optimize this function, we need to do something else.

If we try to visualize the 2D array:

For the cache lines, when we read `a[0, 0]`, the next few numbers will be put into the same line. But when we read `b`, we will be adding another cache line each time, as we jump across rows. If the array is big enough that we cannot put every row of `b` into the cache lines. However, if the size is **small** enough, we can start each cache lines aligned with each row, and therefore take advantage of spatial locality.

We are going to use this to our advantage. We access each submatrix of the larger matrix, and transpose them one block a time. Because blocks are small, we enjoy the benefit of spatial locality if we pick the size smartly.

After the block-wise transpose, each block is of the right order, and we enjoyed spatial locality.

Note that for each block, the destination is still the desired position and therefore, when block-wise operation is done, the whole array is already transposed.

### Right size of block size

if `block.size` is one (operation), this is meaningless
if `block.size` is $N$, this is also meaningless.

**Good!** : `block.size` = $k \times ${cache line size}$

*NOTE: although it is not possible to optimize the performance without benchmarking on the machine, we can generally optimize it based on some trials.*

### Implementation

```ruby
for each block
    for each cell
        # do something
```

In valid C language, this looks like

```c
for (B_i = 0; B_i < N; B_i++) {
    for (B_j = 0; B_j < N; B_j++) {
        for (int i = B_i; i < B_i + B_size; i++) {
            for (int j = B_j; B_j < B_j + B_size; j++) {
                // do something
            }
        }
    }
}

```

### How is this better?

If we only look at the inner loop, it still looks like we do not have spatial locality for at least one query. However, because of blocking, all information are in cache and locality does not matter anymore.

### loop variables

`B_j + B_size` is run every time with the loop.
If we use a variable to store the value, the performance will increase.

## Compiler Optimizations

### Disadvantage

1. Not changing semantics
2. Limited Contac
3. Conservative Heuristics
    - A *Guess Work**

For example,

```cpp
int a, b, c;

c = a + b - a
```

This will be optimized.

```cpp
float c = 1e50 + 1 - 1e50
```

This will not be optimized. Because this will actually result in `c = 0` instead of `c = 1` as in optimized code.

## Loop Unrolling

```c
for (int i = 0; i < N; ++i)
    s += 1
```

```asm
Loop:
cmp %rdi, %rax
jeg End
addq %rdi, %rsi
irmovq $1, %rcx
add %rcx, %rdi
jmp Loop
End:
```

Only 2/5 of the operations are doing the actual work! The book-keeping is taking a great portion of our time.

The simple solution is to put more operations into the loop:

```c
for (int i = 0; i < N; )
{
    s += 1;
    i += 1;
    s += 1;
    i += 1;
    s += 1;
    i += 1;
}
```

**Caveat**: the unrolled loop operations might exceed `N`, therefore we need to change the boundary: `for (int i = 0; i <  N - 2; )`.

If `N` is big, this should not hurt the performance overall. The advantage of unrolling loops will be more important.

**Unrolling Too Much**: intruction cache miss (But this is unlikely, as it would take quite a number of unrollings to do that)


## Function Inlining

- Difficulty 1: Moving arguments into the right place.

**Caller/Callee Convention**

> `%rax` is a caller saved register. Before calling the subroutine, the caller need to push `%rax` onto the stack, and pop it afterwards. So that the callee can change `%rax` as he wants.


These are tedious work to store register values. In order to avoid this, we inline functions.

For example,

```c
int strlen(char* s) {
 // doing something
}

...

x += strlen(s)
```

We place the content of `strlen` before x, saving the return value as a variable and replace the call with the variable.

```c
// doing something
ans = retVal  // instead of return
x += ans
```
