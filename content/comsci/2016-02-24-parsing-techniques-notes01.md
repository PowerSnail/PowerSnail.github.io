---
layout: page
title: "Generative Grammar and Four Types of Grammars: Parsing Techniques Notes (1)"
description: "some notes on Parsing Techniques A Practical Guide"
tags:
    - computer science
    - notes
    - study
    - parsing
mathjax: true
date: "2016-02-24"
---

## Generative Grammar

There are several views of defining a language. The computer science and formal linguistics perspective:

| terms | definition |
| ---   | --- |
| Language | a set of sentences |
| Sentence | a **sequence** of symbols |
| Alphabet | a set of all symbols |

The semantics - meaning - of a sentence is described by its tokens cooperating with its structure.

Grammar is the set of rules describing a language.
**Generative Grammar** is

- exact
- fixed-sized

### Language can be specified by infinite Bit-String

Sorted Alphabet: $\Sigma$
Language $\Sigma^{* }$ contains all combinations of symbols in $\Sigma$

The order of sentences in $\Sigma^* $ follows that:

*from length $l = 0$*

1. enumerate all combinations that of length $l$
2. these combinations are listed according to alphabetical order (lexicographical sorting)
3. increment $l$ and repeat from 1.

This will form an infinitely long sorted list. Every language composed by alphabet $\Sigma$ can be identified by choosing from $\Sigma^* $. If we encode this by binary representation, 0 -> not including, 1 -> including, we can create an infinitely long bit string that indicates every sentence the language contains.

> For example:
> Language $L = 010010110...$

### Formal Grammar

Recipe of replacing symbols:

```
Name  -> tom | dick | harry // Name may be replaced by tom, dick or harry
...
```

A grammar is a *4-tuple* $(V_N, V_T, R, S)$:

- $V_N$ non-terminals, $V_T$ terminals are finite sets of symbols
- $V_N \cap V_T = \varnothing$ terminals and non-terminals cannot have common symbols
- $R$ is the set of rules, a set that contains ordered pairs: ${(P, Q) \mid P\in (V_N\cup V_T)^+ \land Q\in (V_N \cup V_T)^* }$
- $S$ is the start symbol, $S\in V_N$

## Four types of Grammars

### Type 0: Phrase Structure Grammar (PS Grammar)

Most freedom. Follows *4-tuple* $(V_N, V_T, R, S)$, without further restriction.
Represented as `Directed Acyclic Graph`: No cycle exists

### Type 1: Context-Sensitive Grammar (CS Grammar)

There are two equivalent definitions: `Monotonic` and `Context-Sensitive`.
Can be represented by a DAG, similar to PS Grammar.

#### Monotonic

For each rule, left hand side has more or equal number of symbols to right hand side.

#### Context-Sensitive

Every rule is context-sensitive.
- Left hand side contains only one symbol to be changed in the right hand side.

### Type 2: Context-Free Grammar (CF Grammar)

LHS could only contain one non-terminal symbol. (Thus not related to neighboring symbols).
Represented by a tree, as branches of a node is not relevant to other nodes.

The generative power of CF Grammar comes from two operations:
- Concatenation
- Choice (choosing from one of the alternatives in the RHS)

`NT -> tom | NT dick | ...`

### Type 3: Regular Grammar

mostly referring to `right regular grammar`.
Each rule could only contain one non-terminal, as the rightmost item.
Represented by a list, because each sentential has only one replaceable item (non-terminal), or in a production chain.

All regular grammar can be expressed in a regular expression, which sufficiently equal to all rules in the grammar.

Regular Expression Notation Styles:

| Notation  | Description  |
|--- | --- |
 $^{+ }$ | One or more instances of the left-adjacent item   
 $^{* }$ | Zero or more instances of the left-adjacent item
 $^{? }$ | Zero or one instance of the left-adjacent item
 $[abc]$ | Choosing one from $(a, b, c)$, i.e.,  $(a\mid b\mid c)$  

Example:

$S_S\to(([tdh],)^{* }[tdh] \& )^{? }[tdh]$

### Type 4: Finite Choice Grammar (FC Grammar)

Each rule could have only terminals in right hand side.
Very limited expressive power.
