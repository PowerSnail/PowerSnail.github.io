---
title: Claude Haiku 4.5 - Quotes and Notes
description: Claude Haiku 4.5 is released; here are some quotes and reading notes of mine.
date: 2025-10-22
slug: claude-4-5-notes
tags:
    - llm
    - ai
    - anthropic
    - claude 4.5
draft: true
---

> Claude Haiku 4.5, our latest small model, is available today to all users.

On 2025-10-16, Claude Haiku 4.5 was released. It is a smaller and faster model than the previously released Claude Sonnet 4.5.

Here's the release notes: <https://www.anthropic.com/news/claude-haiku-4-5>

The claim is that Haiku 4.5 is on par with GPT-5 Codex on SWE-bench. This is quite interesting, as in my experience, GPT-5 Codex is incredibly slow for complex tasks, but that extra time seems to be useful as it produces more accurate results. I'm curious whether Haiku 4.5 indeed performs on those kind of tasks as well as GPT-5 Codex but faster, but I'm doubtful.

However, even if it is not as good for large, complex tasks, it still might be useful for completing shorter tasks. If we use GPT-5 Codex as an orchestrator, which then dispatches Haiku 4.5 for writing individual functions, we might get a speed boost while keeping the benefit of GPT-5 Codex's higher level insights.

Compared to the predecessor Haiku 3.5, Anthropic claims that Haiku 4.5 offers better capabilities in agentic coding, computer use (operating browsers, for example). It acknowledges that the model is not a "frontier" model, but suitable for agentic works, which suggests that Anthropic encourages the same kind of architecture where a large model is used for orchestrator and a smaller model is for lower level work.

> It is not a frontier model, but its high levels of intelligence and speed make it appropriate for a wide variety of “agentic” uses, including where multiple instances of the model complete tasks in parallel. 

Haiku 4.5 also is supposed to have better safety and alignment.

Haiku 4.5 provides an "extended thinking mode", with which it will follow a chain of thought before replying. I think the reason that more models (even smaller, faster models) are becoming "reasoning" models, is that accuracy in complex problems must be solved with more time and token. To make the process more user friendly, Anthropic launches another instance of Haiku 4.5 to summary the thoughts, if the chain of thought gets too long.

> [...] agentic episodes in reinforcement learning more frequently encounter physical context-window
limits.

This is an interesting observation, and their solution is to make the model "aware" of this limitation during training. They claim that the model becomes more careful when to "wrap things up", as the limit approaches.

I have encountered the problem with the agents exhausting the context window once when porting a NextJS backend to python, and it was with GPT-5 Codex. I'm not sure if this awareness will help; as I suspect that when dealing with tasks that involves a huge amount of input (e.g. coding in a large code base), the application layer must also pick up the responsibility to more reasonably pump data into the model, but at least the model probably won't exhaust its context window by outputing too much.

Sources:

- https://www.anthropic.com/news/claude-haiku-4-5
- https://assets.anthropic.com/m/99128ddd009bdcb/Claude-Haiku-4-5-System-Card.pdf
