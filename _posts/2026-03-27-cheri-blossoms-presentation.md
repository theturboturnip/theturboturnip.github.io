---
layout: single
title:  "All-Caps - My talk at CHERI Blossoms 2026"
date: 2026-03-27
permalink: /posts/2026/03/cheri-blossoms-all-caps
categories: 
  - PhD
tags:
  - cheri
  - publications
author_profile: true
---

I was super excited to gave this talk on my PhD work to close out the CHERI Blossoms conference on 27th March 2026!
Many thanks to my supervisor Simon W. Moore and collaborator Theo Markettos.

<iframe src="https://www.youtube-nocookie.com/embed/qV_4stih5tc" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

CHERI's capability system has shown to be secure and incredibly flexible. It can layer on top of virtual memory, or operate in single-address-space systems (e.g. CHERIoT and CheriOS). It can be used in the kernel as well as userspace (e.g. CheriBSD, Paul Metzger's work on deprivileged GPU drivers, and CHERI CAPIO), providing both with fine-grained spatial memory safety. It can even extend beyond the CPU to trusted hardware peripherals (e.g. CHERI-SIMT) — but not all peripherals can be trusted. Untrusted hardware, well, can't be trusted to store CHERI capabilities or manipulate them correctly. What other kinds of capability are there, and how can they fill the gaps to provide full system protection, unified with CHERI?

This talk explores other kinds of capability system, starting with the very first systems from the 1960s, splitting them into two broad categories of 'C-list' and 'Ticket' capabilities. We explore the pros and cons of these kinds of systems, where they are suitable and where they aren't, and evaluate this in practice by looking at a new I/O-focused system from the University of Cambridge based on cryptographic verification. Just as CHERI can compose with virtual memory, we demonstrate how this system can layer with I/O virtual memory and host-bound CHERI to step closer towards full system protection. It also includes the history of capability systems, insights on how to develop new ones, and how we can apply the principles of capabilities everywhere to make our systems safer.

We also discuss the future of secure computing, challenges in adopting CHERI specifically in I/O, opportunities in adopting CHERI principles in I/O, and integrating these alternate capability systems with CHERI.
