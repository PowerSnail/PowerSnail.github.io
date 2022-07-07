+++
title = "Test Md Page"
description = "A Markdown document that tests various properties of a static site generator."
date = "2022-07-06"
slug = "test-md-page"
tags = ["computer-science"]
images = ["./cover.svg"]
draft = true
+++

When you are tweaking your blog, creating a new CSS rule, or making a new theme, it is not uncommon to break pages that you are not looking. Maybe tables lose their responsiveness, sentences are too close together, empty pages look weird, etc. I've written this document to test some common pitfalls that I experienced when I was tweaking my own blog.

## This is a second-level heading

### This is a third-level heading

#### This is a fourth-level heading

A paragraph under a fourth level heading.

##### This is a fifth-level heading

A paragraph under a fifth level heading.

###### This is a sixth-level heading

A paragraph under a sixth level heading.

### A very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very long heading

## Shapes of paragraphs

**This is a long paragraph. (Content from _Pride and Prejudice_)**

An invitation to dinner was soon afterwards dispatched; and already had Mrs. Bennet planned the courses that were to do credit to her housekeeping, when an answer arrived which deferred it all. Mr. Bingley was obliged to be in town the following day, and consequently unable to accept the honour of their invitation, etc. Mrs. Bennet was quite disconcerted. She could not imagine what business he could have in town so soon after his arrival in Hertfordshire; and she began to fear that he might be always flying about from one place to another, and never settled at Netherfield as he ought to be. Lady Lucas quieted her fears a little by starting the idea of his being gone to London only to get a large party for the ball; and a report soon followed that Mr. Bingley was to bring twelve ladies and seven gentlemen with him to the assembly. The girls grieved over such a number of ladies; but were comforted the day before the ball by hearing, that instead of twelve, he had brought only six with him from London, his five sisters and a cousin. And when the party entered the assembly room it consisted of only five altogether; Mr. Bingley, his two sisters, the husband of the eldest, and another young man.[^austen]

**This is a succession of paragraphs that each contains a short sentence, but not with an extra white line. According to convention, they should be rendered as a single paragraph.**

A dog is here.
A cat is there.
Look at that.
A spoon drops into the lake.
Ripples radiate to the shore.
The moon wrinkled in the water.

**This is a succession of paragraphs that each contains a short sentence, with an extra line in between.**

Twelve o’clock.

Along the reaches of the street

Held in a lunar synthesis,

Whispering lunar incantations

Disolve the floors of memory

And all its clear relations,

Its divisions and precisions,

Every street lamp that I pass

Beats like a fatalistic drum,

And through the spaces of the dark

Midnight shakes the memory

As a madman shakes a dead geranium.

by T.S. Eliot, *Rhapsody on a Windy Night*[^2]

## Punctuations

- "Quotations marks 'rocks'"
- Question mark?
- Bang!
- Comma, period.
- Ellipses......
- Semicolons; 
- Various dashes: 
  - A single, all-too-lonely dash (usually rendered as a **hyphen**).
  - Two consecutive hyphens, 1--2 (usually rendered as an **En Dash**). 
  - Three consecutive hyphens---usually rendered as an **em dash**.
- It's an apostrophe
- Look: colon.
- Some brackets (regular ones), [square ones], {curly ones}
- Slash/forward\backward

## Block quote

> Blockquote directly under a title

> Multiline blockquote
> Without extra line in between

A regular line.

> Multiline blockquote
> 
> With extra line in between

A very long blockquote:

> Their brother, indeed, was the only one of the party whom she could regard with any complacency. His anxiety for Jane was evident, and his attentions to herself most pleasing, and they prevented her feeling herself so much an intruder as she believed she was considered by the others. She had very little notice from any but him. Miss Bingley was engrossed by Mr. Darcy, her sister scarcely less so; and as for Mr. Hurst, by whom Elizabeth sat, he was an indolent man, who lived only to eat, drink, and play at cards, who when he found her prefer a plain dish to a ragout, had nothing to say to her.[^austen]

## Images

Here is an inline image ![test image](./snail-small.webp). There isn't really a good strategy to place an image that is taller than a line inside a sentence, in my opinion. It's just a wacky form of content allowed by the HTML.

Images put on their own line is better:

![test image](./snail-small.webp)

A bigger image:

![test image](./snail-big.webp)

A gigantic image:

![test image](./snail-gigantic.webp)

A svg image:

![svg image](./snail.svg)

A figure written in HTML:

<figure>
    <img alt="Image inside a figure" 
        src="./snail-big.webp">
    <figcaption>
        Image inside a figure
    </figcaption>
</figure>

Some Markdown parser will always treat images as an inline element. There's nothing an SSG or theme maker can do. So this `figure` is written as raw HTML.

## Lists

1. A numbered list
2. With many elements
3. And a multi-
   line item
4. Then, some
   1. sub 
   2. items

- An unnumbered list
  - sub list
    - sub sub list
- A lot of levels
  - interlacing with
    - other
      - going deeper
    - shalower
      - deeper
        - and deeper
  - Back out again
- And see if the rendering is sensible

## Code blocks

```
Block with no language set.
```

```python
def block_with_a_language(python):
    print()
    for indent for ["multi", "level", "code"]:
        for space in indent:
            if ord(space) % 2 == 0: 
                if ord(space) % 5 == 0:
                    print(" ")
```

```
Block with no language set that is super,  super,  super,  super,  super,  super,  super,  super,  super,  super,  super,  super,  super,  super,  super,  super,  super,  super,  super, long.
```

```python
print("A block with a super,  super,  super,  super,  super,  super,  super,  super,  super,  super,  super,  super,  super,  super,  super,  super,  super,  super,  super, long line")
```

## Tables

A simple table with very few columns and rows:

| simple | table  |
| ------ | ------ |
| item 1 | item 2 |

A table with alignment parameters:

| alignment |  test  | table |
| :-------- | :----: | ----: |
| item 1    | item 2 | item3 |
| item 1    | item 2 | item3 |
| item 1    | item 2 | item3 |
| item 1    | item 2 | item3 |

A table with many columns

| table | table | table | table | table | table | table | table | table | table | table | table | table | table |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| row 1 | row 1 | row 1 | row 1 | row 1 | row 1 | row 1 | row 1 | row 1 | row 1 | row 1 | row 1 | row 1 | row 1 |
| row 2 | row 2 | row 2 | row 2 | row 2 | row 2 | row 2 | row 2 | row 2 | row 2 | row 2 | row 2 | row 2 | row 2 |

A table with a very fat column:

| fat    | column                                                                                                                                                                         |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| item 1 | item 2 is very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very long |

## Some random tests

- Language: 中文测试
- HTML embeded: <br><strong>`<br><strong>`</strong>
- References[^3]


[^austen]: Austen, Jane. *Pride and Prejudice*. Standard Ebooks, 2014.
[^2]: Eliot, T. S. *Poetry*. Standard Ebooks, 2017.
[^3]: A test for reference
