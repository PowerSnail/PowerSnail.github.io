---
title: {{ replace (substr .Name 11) "-" " " | title }}
description: 
date: {{ substr .Name 0 10 }}
slug: {{ substr .Name 11 }}
tags:
draft: true
---