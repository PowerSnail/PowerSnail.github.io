---
title: A few fun discoveries about Stable Diffusion
description: Testing the literary limit of Stable Diffusion
date: 2022-11-10
slug: stable-diffusion-fun
tags: 
  - machine learning
  - computer science
draft: true
---

Standing opposed to OpenAI's DALL-E and Midjourney, is the open sourced model Stable Diffusion. Some of the images it painted are genuinely impressive, coherent, and free of artifacts (at least at first glance). But those are almost always the result of prompt engineering: an Edisonian process of random search through the infinite linguistic space. Or in other words, people trying different words until they get a desirable result.

For instance, there's a collection of "magic words" that improves the quality of the model's output: "4k", "detailed", etc.[^prompt-book] The model associates these key words with the high quality images in its training set, because that's how people label their own work, and thus tries to be close to those images.  

What happens if you don't give it a particularly graphic sentence? How does it deal with the abstract, the metaphysical, and the poetic?

## Literatures, Quotes, and Illustrations

It gives you the quote right back:

![Generated image from Oscar Wilde's quote: "Questions are never indiscreet; answers sometimes are."](./quote-1.webp "Questions are never indiscreet; answers sometimes are.  -Oscar Wilde")

......Not quite verbatim, but close enough. Similar to how "4k" nudges the model towards higher quality, if you sound like Brainy Quotes, it will paint like Brainy Quotes for you. 

Sometimes, it will go a different route, and illustrate like a book of classics:

![Generated image from a quote from Oscar Wilde: "If the lower classes don't set us a good example what on earth is the use of them? They seem, as a class, to have absolutely no sense of moral responsibility."](./quote-2.webp "If the lower classes don't set us a good example what on earth is the use of them? They seem, as a class, to have absolutely no sense of moral responsibility.")

Now, this is just a silly experimentation. The model is trained on descriptions of images. It's not surprising that it wouldn't do well on metaphysical epigrams depicting no concrete objects. In fact, if you give me drawing prompt "Questions are never indiscreet; answers sometimes are", I'd probably ask you clarify just what the hell you want me to draw. 

## Where is the cicada?

![Generated image from a quote taken from Pale Fire: "Waxwings are berry-pecking / a cicada sings."](./cicada.webp "Waxwings are berry-pecking / a cicada sings. -Nabokov, _Pale Fire_")

Another limitation I've found is that Stable Diffusion will sometimes ignore a part of the prompt entirely. This is quite interesting because it obviously is capable of juxtaposing unrelated elements together, as demonstrated by various examples in its [repository](https://github.com/CompVis/stable-diffusion). 

A beautiful line of poetry, "Waxwings are berry-pecking / a cicada sings", is not as abstract as the previous section. It depicts two subjects, a bird and a bug, and yet Stable Diffusion absolutely refuses to recognize the existence of the latter.

Could it be the position of the two words in the sentence? Let's try reversing it:

![Generated image from reversing a quote taken from Pale Fire: "A cicada sings / Waxwings are berry-pecking."](./cicada-reverse.webp "A cicada sings / Waxwings are berry-pecking.")

Nope. Only the bird itself. Beautifully drawn, but missing its companion.

Could it be the realistic style which it's going for? Let's try adding some stylistic modifiers to the prompt:

![Generated image from prompt:"Waxwings are berry-pecking / a cicada sings. Illustration."](./cicada-illustration.webp "Waxwings are berry-pecking / a cicada sings. Illustration.")

![Generated image from prompt:"Waxwings are berry-pecking / a cicada sings. Oil painting."](./cicada-oil.webp "Waxwings are berry-pecking / a cicada sings. Oil painting.")

![Generated image from prompt:"Waxwings are berry-pecking / a cicada sings. Photo."](./cicada-photo.webp "Waxwings are berry-pecking / a cicada sings. Photo.")

And if you look carefully, you'll notice that even "berry" isn't always there. The model sees "waxwings" and that's the only thing it cares about.

## Last word

Stable Diffusion, like many other machine learning models dabbling in art, astonishes the programmer part of my brain. It's utterly ridiculous that we can make program generate coherent images according to prompt, without hard-coding any rule about what it means for an image to be coherent. We give zero _priori_ to the model on what constitutes a photo or an oil painting, or the anatomy of waxwings, or the color of trees and leaves. 

But at the same time, the other parts of my brain still smirks a bit at the results. When you jump even slightly out of the box, Stable Diffusion starts to show its limits. And even within the box, it takes a lot of word tweaking and cherry-picking to get some useful images out of the model. A lot of hobbyists left the model to run overnight on a long list of prompts. In other areas, the music generated by machine learnings are still quite bad, and seems to go from nowhere to nowhere, if we judge the music entirely on its own merit. The same goes for text generation.

It is quite disquieting to see just how close we are to computer programs surpassing human in the field of creative arts, and perhaps even programming itself. We are not there yet, but I'm willing to bet that it's going to happen within the life time of my generation. Where would that leave us? To become Olympians of the machines and reap the fruit of their labor? Or to compete with the machines, and eventually---inevitably---become obsolete? Will the society become more equal as the rising productivity and efficiency alleviate scarcity, or will the divide deepen between the wealthy and powerful, and the underprivileged?

> Anybody that competes with slaves becomes a slave
>
> - Vonnegut, _Player Piano_

