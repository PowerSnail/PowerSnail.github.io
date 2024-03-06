---
title: How to Make Neovim Open PDF and Images External Viewers
description: Configuring neovim with Lua.
date: 2024-03-05
slug: open-binary-files-external
tags:
    - neovim
    - system
    - editor
    - text editing
    - pdf
    - image
    - lua
draft: false
---

After some serious attempts to equip my terminal emulator with the ability rendering images, I've given up on it. My experience is that in 2024, it's still not quite a practical endeavor, at least on my machine with all the CLI tools that I'm using, specifically `tmux` and `neovim`. There are a handful of image protocols out there made for this purpose, but each comes with enough caveats, or limitations on what terminal/multiplexer/scrolling capabilities that it can work with.

Still, there is the need to display images and PDFs while I'm working, and using `neovim` as my main editor, I find it tedious to have to open a preview of a file in another pane by typing out its full path, when there is a perfectly functional fuzzy search capability right there in the editor. It's also annoying when I accidentally select a binary file and `neovim` shows me gibberish.

As a workaround, I set up some auto-commands that trigger external previewers for these files:

```lua
-- Open binary files
vim.api.nvim_create_autocmd("BufReadCmd", {
  pattern = "*.pdf",
  callback = function()
    local filename = vim.fn.shellescape(vim.api.nvim_buf_get_name(0))
    vim.cmd("silent !mupdf " .. filename .. " &")
    vim.cmd("let tobedeleted = bufnr('%') | b# | exe \"bd! \" . tobedeleted")
  end
})

vim.api.nvim_create_autocmd("BufReadCmd", {
  pattern = { "*.png", "*.jpg", "*.jpeg", "*.gif", "*.webp" },
  callback = function()
    local filename = vim.fn.shellescape(vim.api.nvim_buf_get_name(0))
    vim.cmd("silent !eyestalk " .. filename .. " &")
    vim.cmd("let tobedeleted = bufnr('%') | b# | exe \"bd! \" . tobedeleted")
  end
})
```

The snippet is predominantly based on [this Stack Exchange post](https://vi.stackexchange.com/questions/7217/how-can-i-cancel-reading-a-file-into-a-buffer-on-bufreadpre).

## Some explanations

- `BufReadCmd`. This function is triggered before the file is loaded into the buffer, and in fact, it is supposed to do the actual work of reading the file. By not doing that work, the reading is avoided. [^vim] [^muru]
- `vim.fn.shellescape(vim.api.nvim_buf_get_name(0))`. This line retrieves the name of the current buffer's file using `vim.api.nvim_buf_get_name(0)` and then escapes the filename for safe use in a shell command using `vim.fn.shellescape()`.
- The trailing `&` puts the process of the external program into the background, so the editor is not frozen by it.
- `vim.cmd("let tobedeleted = bufnr('%') | b# | exe \"bd! \" . tobedeleted")`. This command first switches the previous buffer to the front, and deletes the buffer of the binary file. [^louwers]

## Further work

The next step is to find or make a fast, general purpose file viewer, so I can open all binary files---or any file that's not suitable for text-based editing---in the same app. At the moment, `mupdf` is the fastest simple PDF viewer I've found, at least the fastest among the packages in my system repo.

[^vim]: Bram Moolenaar. (2024, January 25). VIM REFERENCE MANUAL. https://vimhelp.org/autocmd.txt.html#BufReadCmd

[^muru]: muru. (2016, April 6). Answer to “How can I cancel reading a file into a buffer on BufReadPre?” Vi and Vim Stack Exchange. https://vi.stackexchange.com/a/7223

[^louwers]: Louwers, B. (2016, April 6). Answer to “How can I cancel reading a file into a buffer on BufReadPre?” Vi and Vim Stack Exchange. https://vi.stackexchange.com/a/7236

