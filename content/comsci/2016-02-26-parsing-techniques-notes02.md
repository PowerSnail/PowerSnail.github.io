---
layout: page
title: "Production of Sentences and Properties of Languages: Parsing Techniques Notes (2)"
description: "some notes on Parsing Techniques A Practical Guide"
categories:
    - comsci
tags:
    - computer science
    - notes
    - study
    - parsing
mathjax: true
---



## Generating Sentences



|  | sentence _vs._ sentential |
|--|--|
| sentence  | all symbols belongs to terminals (a valid element of the language) |
| sentential | may contain non-terminals, an intermediate form during sentence production |

#### Example:

For a language where $V_N = {P, Q} \land V_T = {a, b, c, d}$, a valid sentential would be $aP$; a valid sentence would be $ac$.


### Type 0 and Type 1 (CS) Languages

**Breadth-first Production**: for each sentential, make copies of it for each applicable rule. Then, repeat the operation on each copy. If there is no _non-terminal_ in the sentential, it is then a sentence, and could be printed and discarded in the production.

This process may be infinitely long, but it is guaranteed that an arbitrary sentence will definitely be produced.

#### Two Remarks about CS Language Sentence Production

1. We cannot decide whether a CS language is empty, i.e. whether its rules could produce a sentence. <br> The process takes infinite time, and therefore is _undecidable_.
    - It is possible to prove a CS language being non-empty by giving an example of sentence it generates.
    - It is impossible to prove a CS language is empty.

2. General parsing of CS language is _unsolvable_. We cannot produce a list of sentences in a CS language in order by length. Because it is context sensitive, the length of the sentence could "shrink" suddenly and unpredictably. <br> As a result, we cannot determine a sentence is not in the language; there is always possibility that it may show up in further production.

Type 0 language has the same properties.

### Type 2 (CF) Language

Monotonic nature of CF language means that the length of sentence will not "shrink". Therefore, we could solve the two problems of CS language by a rather simple algorithm:

1. Scan rules that have terminal on right hand side,
2. marking those as productive;
3. scan rules that have productive on right hand side,
4. repeat 2, 3 until meeting the start symbol or no new productive symbols could be found

If the above process is able to reach the start symbol then it is not empty; otherwise, it finds no way up to the start symbol, the language is empty.

The length of sentence does not shrink in CF language. Therefore, we could determine a sentence's existence. If we meet the sentence obviously, it belongs to the language. If we keep producing and exceed the length of the sentence, then further production on the sentential will definitely not produce the sentence. We could therefore decide the inclusion of an arbitrary sentence of finite length in finite time.

### Type 3 (Regular) Language

Regular language has rules that right hand side contains at most one non-terminal, and it should be the rightmost symbol. Regular language could be written as regular expressions that is composed of only terminals and regular operators. As a result, if a non-empty regular expression could be constructed, then the language is non-empty.

It is also possible to enumerate sentences without breath-first production, as only one non-terminal could be replaced in each sentential. When looking for a sentence $K$ of length $l$, if the length of sentential exceeds $l$, then $K$ cannot be included in the language. Finding any sentence in the process would prove that the language is not empty.























<!-- page -->
