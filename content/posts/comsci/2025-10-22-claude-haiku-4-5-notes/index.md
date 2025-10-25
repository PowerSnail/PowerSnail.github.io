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
draft: false
---

> Claude Haiku 4.5, our latest small model, is available today to all users.

On 2025-10-16, Claude Haiku 4.5 was released. It is a smaller, faster model than the previously released Claude Sonnet 4.5.

Here are the release notes: <https://www.anthropic.com/news/claude-haiku-4-5>

The claim is that Haiku 4.5 is on par with GPT-5 Codex on SWE-bench. This is quite interesting, as in my experience GPT-5 Codex is incredibly slow for complex tasks, but that extra time seems useful, as it produces more accurate results. I'm curious whether Haiku 4.5 performs as well on those kinds of tasks as GPT-5 Codex, but faster, though I'm doubtful.

However, even if it is not as good for large, complex tasks, it might still be useful for completing shorter tasks. If we use GPT-5 Codex as the orchestrator, which then dispatches Haiku 4.5 to write individual functions, we might get a speed boost while keeping the benefit of GPT-5 Codex's higher-level insights.

Compared with its predecessor, Haiku 3.5, Anthropic claims that Haiku 4.5 offers better capabilities in agentic coding and computer use (for example, operating browsers). Anthropic acknowledges that the model is not a "frontier" model but is suitable for agentic work, which suggests that Anthropic encourages the same kind of architecture where a large model serves as the orchestrator and a smaller model handles lower-level work.

> It is not a frontier model, but its high levels of intelligence and speed make it appropriate for a wide variety of “agentic” uses, including where multiple instances of the model complete tasks in parallel.

Haiku 4.5 is also supposed to have better safety and alignment.

Haiku 4.5 provides an "extended thinking mode" in which it follows a chain of thought before replying. I think the reason more models (even smaller, faster models) are becoming "reasoning" models is that accuracy on complex problems requires more time and tokens. To alleviate this slowness, Anthropic launches another instance of Haiku 4.5 to summarize the thoughts if the chain of thought gets too long.

> [...] agentic episodes in reinforcement learning more frequently encounter physical context-window
> limits.

This is an interesting observation, and their solution is to make the model "aware" of this limitation during training. They claim that the model becomes more careful about when to "wrap things up" as the limit approaches.

I had once before encountered agents exhausting the context window when porting a Next.js backend to Python with GPT-5 Codex. I'm not sure this awareness will help, as I suspect that when dealing with tasks that involve a huge amount of input (e.g., coding in a large codebase), the application layer must also take responsibility for feeding data into the model more judiciously. At least the model probably won't exhaust its context window by outputting too much.

Sources:

- https://www.anthropic.com/news/claude-haiku-4-5
- https://assets.anthropic.com/m/99128ddd009bdcb/Claude-Haiku-4-5-System-Card.pdf

