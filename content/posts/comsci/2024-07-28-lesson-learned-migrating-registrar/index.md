---
title: Lesson Learned Migrating Registrar
description: |
    I made a mistake when trying to change the registrar for my domain. By simultaneously changing the nameserver and the transferring the domain, 
    and not being patient enough to validate changes, I broke my domain, twice.
date: 2024-07-28
slug: lesson-learned-migrating-registrar
tags:
    - domain
    - DNS
    - nameserver
draft: false
---

I originally registered my domain `powersnail.com` on Google Domain, which seemed to be a popular and well-made product at the time. It was all good, until in 2023, the service was announced to terminate and all domains will be transferred to SquareSpace.

Despite receiving notifications of the news, I procrastinated long enough such that I was already transferred to SquareSpace, when I came about to move away. The interface on SquareSpace was quite bare-bone in functionality and there were reports that its name server was very slow when propagating changes.

Additionally, Google Domain was convenient for me because I had and need a Google account, but I didn't have a SquareSpace account, and I was not interested in using any of its core product anyway.

I wanted to move away from it altogether.

To be precise, there were two things that I'd like to change: the name server to CloudFlare and the registrar to porkbun. The former because of its impressive free-tier features, and the latter because it's pretty _cool_ in a no-bullshit, direct way---there's something very candid about their UI that just really make me happy.

The first thing I did was changing the nameserver. It was easy enough, but somehow, the change just was not propagating. It is typical of anything related to DNS to be accompanied by a warning that you may have to wait for a couple of hours, but to be honest, when I was messing with DNS settings in Google Domain, it never took more than a few minutes for the change to propagate. SquareSpace was living up to its reputation of slow propagation and I was growing impatient, so I decided that, well, as long as the change could eventually happen, I might as well proceed.

So I requested transfer of the domain itself from SquareSpace to porkbun. It was said that the process would take days. Good enough. It was set into motion. I went away.

It was, then, a very quiet day. I found myself not being bothered by a single email the entire rest of the day, which was odd. It quickly dawned on me that I had broken my custom domain.

It turns out that the name server was not successfully changed to CloudFlare. On SquareSpace, the name servers were pointing to CloudFlare. For CloudFlare---and also the rest of the world, the domain was still pointing to SquareSpace's server. It was hard to imagine how it ended up in such a state, but the result was that neither of them were handling the DNS queries, and so everything, from my blog to my email to my personal git server, was effectively down.

The fact that changing the name server is not atomic came as a surprise to me. I would have thought that SquareSpace's name server would continue to do its job, during the time where the change was still being propagated, or if some error had occurred, it would rollback. But no, it simply stopped responding to DNS queries first, before the rest of the internet ever saw that change, and then my impatience---initiating the domain transfer too soon---froze the broken state where nothing was proceeding.

The transfer was going to take as much as 15 days, and the customer support refused to expedite the process (come on, SquareSpace, even Godaddy allows it). So, I cancelled the transfer first, restored the name server to SquareSpace, which thankfully fixed the DNS situation, and then, re-requested transfer without messing with name server this time.

Well, here comes the day of radio silence. When the transfer completed, my domain stopped being resolved again, because the moment the domain was off SquareSpace, SquareSpace cut off the name server for that domain. There was also no way to export the DNS records after the transfer. (I don't remember seeing an export options before either, but I could be wrong, since I no longer have access to that UI)

Luckily, I had an old backup copy of my DNS records exported from Google Domain, which was not fully up to date, but better than creating everything from scratch. I imported the records to CF, and pointed porkbun to CF's server (which happened nearly instantly unlike SquareSpace).

Finally, it was all working.

At the end of the day, here are what I learned about doing a domain transfer without down time:

1. Don't mess with two things at the same time when dealing with domains, especially when something is not in a fully functional state.

2. When migrating domains, migrate the DNS records off first. Even if the name server change takes forever, wait until it's done. 

3. There is also the benefit of using a name server that is not also your registrar, so when you transfer the domain, you don't risk the registrar also cut off DNS resolution. I think it isn't unreasonable to expect any sane provider to not cut it off, because these are obviously separate services, but the reality is that they very well might.

And special thanks to SquareSpace for providing a learning opportunity. Had the name server change been swift, or had the name server been available until I disable them, everything would have worked smoothly and I wouldn't even realize that there were lessons to be learned.


