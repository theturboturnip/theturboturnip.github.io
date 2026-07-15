---
layout: single
title:  "A layperson's server"
date: 2026-07-xx
permalink: /posts/2026/07/a-laypersons-server
categories: 
  - Side Projects
tags:
  - vps
  - hetzner
  - docker
  - api
  - rust
author_profile: true
---

So, it's finally over! You've submitted your PhD thesis **[Blogpost Pending]**, found a job **[Blogpost Pending]**, and you have one last summer of independence before entering the perpetual grind.
There's only one thing for it: build some random personal projects, such as a web search suggestion API **[Blogpost Pending]**, and host them on a server.

<!--Aside from [watching movies](https://letterboxd.com/theturboturnip/), there is only one thing to do: screw around with personal projects and do very little of use!-->

(todo soemthing here)

To preface, I'm sure this is not how professional devops work, but it *is* reliable, debuggable, and works in a way that I can understand as a non-devops-y, hardware-y, OS-y person.
The goal of this post is to explain briefly how some of these tools work from my perspective, and maybe even show you some new ways to approach or think about them.

# DNS

(moved from godaddy to porkbun. porkbun has nicer DNS modification, and was also cheaper for my case)

# Email

<!--Proton struck a good balance for my goals of reputable (no issues sending/receiving emails) and configurable.-->
To my knowledge M365 and Gmail can't be used for custom domains, and I chose Proton to move some of my eggs out of their baskets.
Their office suite is not quite as powerful but it gets the job done, and I feel more comfortable holding more sensitive files (e.g. work contracts, payslips, personal info) on something that won't be scanned for AI and is less likely to arbitrarily disappear.

(evidence for arbitrary disappearance?)

# Web Hosting

(static hosting with GitHub, need to move apps away)

(2x servers => need another server to redirect)
(hetzner, also considered netcup but I had an issue with a voucher not working and got a better vibe for hetzner)
(I use hetzner for a public IPV4, IPV6, and the cheapest server money can buy)

# An Actual Server

(initially I provisioned it with a basic cloud-init script and poked at it manually - i got things wrong. Not so wrong as to be attacked, but still wrong. I would recommend reading through other people's scripts and setups and starting from there, they will likely have thought of things you didn't.)

## Caddy for web serving

(nginx requires a bunch of extra certbot things for HTTPS - don't worry! use caddy!)

(that said, caddy does require the 'data directory' to be kept consistent. I have a workflow to copy it off the server and then copy it back after reimaging so it can persist.)

## Docker for custom services

(Dockerfiles are easier than you think (sort of) (follow the tutorial))

## Cloud-init for initial setup

(nicer than an init script)

(necessary to set up firewalls and ssh keys as early as possible - the public internet is a hostile environment)

(hetzner has an API endpoint for reimaging servers with new cloud-init, which i relied on to make sure I kept my cheap server)

(try and find the two places I generated my script from)

## Ansible for complex setup

(ansible runs from a different computer and targets the server - you don't need to copy it into the server itself!)

(based on this person's base - I would recommend changing some things, esp the RSA-based SSH key to ED25519.)

(i tore out everything I didn't need, which is to say most of it. this has kept the server stateless, which might not be the case forever, but does allow me to avoid doing backups. if something goes wrong, I can reimage and consistently get the same result, and if the server itself is attacked the 'important data' is minimal - just a few API keys.)

(decided against nixos and immuatability to allow e.g. security patches through unattended-upgrades, timezone file updates)

## QEMU for testing

(grab a cloud-init image and set it up correctly, keep the same cloud-init script (it is important to test!))

(QEMU user-mode networking (i.e. the easy networking) does weird DNS things - I upload a setup script that updates to the correct DNS )

(Caddyfile.localhost important - don't try to provision HTTPS into your localhost!)

(ansible localhost weirdness)

(90% of the bugs I encountered over the course of this process were shell scripts doing something slightly different to what I want. This makes the interation time on those bugs a lot nicer and avoids server downtime.)
