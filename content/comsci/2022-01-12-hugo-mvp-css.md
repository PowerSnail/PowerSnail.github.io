---
title: "Theme-less Hugo, Almost Pure HTML, Styled with MVP CSS"
tags:
    - computer science
    - blog
    - hugo
    - html
date: "2022-01-12"
---

## Theme-less Hugo

As popular as theming is, I can't help but feel unsatisfied by a plug-and-use theme made by someone else. From WordPress to Jekyll to Hugo, no theme ever stopped me from tinkering with the underlying templates and CSS, during which, the theme inevitably becomes more coupled with my blog and content. This is because while the templates are usually generic enough for the body of blog articles, they are often quite specific on other elements: about, headers, footers, navigation bars, etc. And to customize those elements, I'm practically re-writing the website.

When I started with Hugo, I chose the theme [Rocinante](https://github.com/mavidser/hugo-rocinante), for its clean appearance, and partially for its name, which comes from one of my favorite novels of all time. I forked the theme, and kept maintaining two repositories: the blog itself, and the theme. As more modifications were made, the two codebases tangled with each other so deeply, that I often wonder where I should put a certain element. 

I decided to go theme-less, when the theme no longer bear any resemblance to the original Rocinante. There's no point in maintaining two sets of code if they cannot be decoupled.

Theme-less Hugo is easy: I just needed the templates, everything in the `layouts` directory, to scaffold the site. So, I copied the skeleton code---`layouts`, and `assets` for the styles---into my blog, and removed the `themes` directory. 

In fact, I think if one has finished theme-shopping, and would like to start making customizations, the first thing to do is to copy the theme into their main project, and delete `themes`. It makes the website whole, the workflow more coherent, the workspace better organized, the commit history saner.

## Semantic HTML and MVP.CSS

I have very little need for advanced topography or animations. My blog is just a bunch of static files hosted on GitHub Pages; nothing Fancy.

This is, therefore, a very suitable use case for a classless CSS framework like [MVP.CSS](https://andybrewer.github.io/mvp/). Overall, I think MVP does a fantastic job. 

A few things that I don't like about it:

1. Block quotes. MVP centers and enlarges the text in block quote, as if I'm hanging an inspirational epigram on the wall, which doesn't fit the semantic role of block quotes. It's simply a quotation that occupies a paragraph; it's part of my content, a link in the linear chain of words, not a flyout or illustration. MVP already has `<section><aside>` to deal with that.

2. Links without underlines. This makes the website less accessible to color-blind readers, or anyone who reads on a monochrome monitor.

3. Alternating table row colors. Not a fault of MVP. This is merely a pet peeve of mine.

With regard to code blocks, Hugo defaults to rendering code highlighting with inline style of fixed colors, which is awkward when MVP can react to system-wise dark theme. So, I configured Hugo to output code blocks with CSS classes, and output two themes, `friendly` and `dracula`, for light and dark themes respectively.

```sh
# To generate the CSS files
hugo gen chromastyles --style=friendly > assets/css/_friendly.css
hugo gen chromastyles --style=dracula > assets/css/_dracula.css
```

```scss
// style.scss
// To include both themes
@import "friendly";

@media (prefers-color-scheme: dark) {
  @import "dracula";
}
```

```toml
# config.toml
[markup]
  [markup.highlight]
    noClasses = false
```

I then colored the website with a dark banner image of Bach's manuscript, and a color scheme generated from a picture of a violin. To ensure that the colors have enough contrast, I generated them with [Oklab](https://bottosson.github.io/posts/oklab/) color space, and it seems to be passing accessibility tests so far. It might be a total overkill though, since a few colors on the spectrum are used. But what is a personal project without a few overkills?

## MathJax, and a Little Grievance of Hugo

The only JavaScript I use is [MathJax](https://www.mathjax.org/). I've been considering to use its server-side rendering, but it seems that at the moment of writing this blog, Hugo does not support its use.

In fact, Hugo does not support running its output HTML through an arbitrary command, and I think it's a shame. There is a limit to what the `replace` and `replaceRE` could accomplish, which can be supplemented by custom filters written by other users. 

For instance, math equations can be easily rendered with LaTeX and converted to SVG. This will enable the embedding of arbitrary Tex elements, not just what MathJax supports, and at the same time, eliminates the need to bundle a JS library for client-side rendering. 

One thing that I can do is to add an extra step to `hugo build`, and iterate through all the output HTML with whatever post-processing I want. But I do hope that this could be integrated into Hugo, so I don't have to further butcher the GitHub Action file.

## Final Thoughts

You can find all the code to my blog [here](https://github.com/PowerSnail/PowerSnail.github.io). My modifications to the theme, up to the point that I moved everything into the main repository, can be found [here](https://github.com/PowerSnail/hugo-rocinante).