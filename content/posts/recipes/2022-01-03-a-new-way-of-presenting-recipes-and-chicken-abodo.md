---
title: A New Way of Presenting Recipes and Chicken Abodo
description: Sour, sweet, succulent chicken from the Philippines
tags:
  - Recipe
  - Chicken
date: "2022-01-05"
slug: "a-new-way-of-presenting-recipes-and-chicken-abodo"
---

## Cooking for Engineers

I bumped into a site called [Cooking for Engineers](http://www.cookingforengineers.com/) today, and at the bottom of some recipes, they have this succinct table that summarizes the procedure in a refreshingly simple manner:

{{< rawhtml >}}
<table><tbody><tr><td style="border: solid 1px"><span itemprop="ingredient" itemscope="" itemtype="http://data-vocabulary.org/RecipeIngredient"><span itemprop="amount">3 chicken</span> <span itemprop="name">breasts</span></span></td><td style="border: solid 1px">brine</td><td style="border: solid 1px" rowspan="3">season</td><td style="border: solid 1px" rowspan="3" class="vertical">cook medium-high</td><td style="border: solid 1px" rowspan="3">remove</td><td style="border: solid 1px" colspan="3" rowspan="3" class="righthide"></td><td style="border: solid 1px" rowspan="6" class="vertical">coat with sauce</td></tr><tr><td style="border: solid 1px"><span itemprop="ingredient" itemscope="" itemtype="http://data-vocabulary.org/RecipeIngredient"><span itemprop="name">salt</span></span></td><td style="border: solid 1px" rowspan="2" class="righthide"></td></tr><tr><td style="border: solid 1px"><span itemprop="ingredient" itemscope="" itemtype="http://data-vocabulary.org/RecipeIngredient"><span itemprop="name">pepper</span></span></td></tr><tr><td style="border: solid 1px"><span itemprop="ingredient" itemscope="" itemtype="http://data-vocabulary.org/RecipeIngredient"><span itemprop="amount">4 oz. (120 g)</span> <span itemprop="name">button mushrooms</span></span></td><td style="border: solid 1px">slice</td><td style="border: solid 1px" colspan="3" class="righthide"></td><td style="border: solid 1px">cook 1 min.</td><td style="border: solid 1px" rowspan="2" class="vertical">reduce</td><td style="border: solid 1px" rowspan="3" class="vertical">reduce</td></tr><tr><td style="border: solid 1px"><span itemprop="ingredient" itemscope="" itemtype="http://data-vocabulary.org/RecipeIngredient"><span itemprop="amount">1 cup</span> <span itemprop="name">sweet marsala wine</span></span></td><td style="border: solid 1px" colspan="5" class="righthide"></td></tr><tr><td style="border: solid 1px"><span itemprop="ingredient" itemscope="" itemtype="http://data-vocabulary.org/RecipeIngredient"><span itemprop="amount">4 Tbs.</span> <span itemprop="name">heavy cream</span></span></td><td style="border: solid 1px" colspan="6" class="righthide"></td></tr></tbody></table>
{{< /rawhtml >}}

\* Copied from [this recipe](http://www.cookingforengineers.com/recipe/59/Chicken-Mushroom-Marsala)

The drawback of this method is that it's not easily written in Markdown, which is sadly the backbone of Hugo. Markdown table is not as flexible as the HTML one, but the HTML one, with a lot of spans, is not readable inside a markdown file. Not to mention the fact that I probably have to further mess with the CSS to hide some cell walls.

## Modernist Cuisine

I encountered another website Modernist Cuisine, which, too, offered their own summary card for each recipe. Instead of a hacky HTML table, they chose to upload an image of a better-formatted table, like the one on this [page](https://modernistcuisine.com/recipes/hanukkah-short-ribs/).

It's not as succinct as the approach taken by Cooking for Engineers. The pro is that the procedure is listed in chronological order. The con is that it's not immediately obvious what can be made in parallel.

But, it's actually more readable, and aesthetically more pleasing. In fact, the aesthetics of the table reminds me of LaTeX and the famous [booktabs](https://ctan.org/pkg/booktabs) package.

So, I decided to go with the Modernist's approach.

## Chicken Abodo

Chicken Abodo is a famous dish from the Philippines, which I first saw on [J. Kenji López-Alt](http://www.kenjilopezalt.com/)'s YouTube channel. At the time I took some short notes on my phone:

```markdown
- Sear the chicken, lightly salted
- Prepare a bunch of garlic, bay leaves, sugar, black pepper
- Add ground pepper and pepper corns
- Add garlic, bay leaves, sugar, and sauce,
    - Ratio by weight: 1 vinegar : 2/3 soy sauce : 2/3 sugar
- Simmer for 1 hour
```

Since then, I've nailed down the quantities of the ingredients more precisely. To re-document this recipe, I wrote this Latex document:

{{< codefile latex "static/latex/chicken-abodo.tex" >}}

And to convert this into an image, which tightly bounds the table rather than being a full letter sized white page, I rendered the document into a `DVI` file and converted it into `SVG` with `dvisvgm`. The tool automatically crops the image, so it doesn't end being a full letter sized page.

![Recipe Summary for Chicken Abodo](/images/chicken-abodo.svg)

This is the final result of a printable, succinct, summary card for my chicken abodo recipe. After reading on the web (and fiddling with HTML and CSS) for so long, there's something very satisfying about LaTeX. It just looks nice.

I then wrote a [Justfile](https://github.com/casey/just) recipe to automate the process:

```
latex-svg name:
    mkdir -p output
    latex --output-directory=output/ --output-format=dvi static/latex/{{ name }}.tex
    dvisvgm --stdout -O -n output/{{ name }}.dvi > static/images/{{ name }}.svg
```

The option `-n` causes the SVG to turn all the glyphs into paths. Using fonts causes the browser to substitute the fonts, which is desirable in some cases, but not in a LaTeX document where the placement of elements are fixed.
