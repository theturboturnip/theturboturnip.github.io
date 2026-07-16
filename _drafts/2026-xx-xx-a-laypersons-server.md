---
layout: single
title:  "A layperson's server"
permalink: /posts/2026/07/a-laypersons-server
categories: 
  - Side Projects
tags:
  - vps
  - hetzner
  - docker
  - rust
author_profile: true
---

So, it's finally over! You've submitted your PhD thesis, found a job, and you have one last summer of independence before entering the perpetual grind.
There's only one thing for it: build some random personal projects, buy some domains, and waste a bunch of time hosting them on a server!
I went on this little odyssey over the last few months and learned a lot about how servers are managed in the cloud, and thought it would be nice to post about how I managed to figure it all out.
My server now hosts <https://theturboturnip.com>, which can be used to access this blog e.g. <https://theturboturnip.com{{ page.permalink }}>, and my custom web APIs <https://github.com/theturboturnip/turnip_api>.

<!--my Turnip-Search service with useful autocomplete **[Blogpost Pending]** along with my other web APIs .-->


<!--Aside from [watching movies](https://letterboxd.com/theturboturnip/), there is only one thing to do: screw around with personal projects and do very little of use!-->


I'm sure my setup is jankier than a professional devops work, but it *is* reliable, debuggable, and works in a way that I can understand as a non-devops-y, hardware-y, OS-y person.
The goal of this post is to explain briefly how some of these tools work from my perspective, and maybe even show you some new ways to think about them.

# Domains & DNS

A year or so ago I bought the domain <https://theturboturnip.com>, having accepted that this username will forever be attached to my real identity.
For a while this website was hosted there, but once I started hosting my CV here I felt that the domain wasn't quite professional enough.
<!--A more professional -->
<!--That matched my GitHub username and for a while I used it to host this website.-->
<!--However, this website also includes my CV, and I felt that the domain didn't really match the level of professionalism I'd want to show potential employers.-->
I also wanted to start using the domain for email, which would have the same problem.
I ended up buying <https://samuelwstark.com>, where this website is now hosted, and keeping both domains active.
<https://theturboturnip.com> now redirects to <https://samuelwstark.com> to ensure old links stick around.

(moved from godaddy to porkbun. porkbun has nicer DNS modification, and was also cheaper for my case)
GoDaddy £45/3 years (they don't include tax in their stated prices!!!!)

# Email

One of my guiding principles was "I don't want to rely on my server".
Servers are fickle things, they can go down, they can be attacked, they can lose data.
I am not a devops professional and I am not always going to be around to manage my server --- if anything happens, I need it to be recoverable.
Thus, anything truly important should be deferred to other services, even if it uses my domains.
Email is one of those things.

<!--Proton struck a good balance for my goals of reputable (no issues sending/receiving emails) and configurable.-->
To my knowledge M365 and Gmail can't be used for custom domains, and I chose Proton to move some of my eggs out of their baskets.
Their office suite is not quite as powerful but it gets the job done, and I feel more comfortable holding more sensitive files (e.g. work contracts, payslips, personal info) on something that won't be scanned for AI and is less likely to arbitrarily disappear.

(evidence for arbitrary disappearance?)

# Web Hosting

(static hosting with GitHub, need to move apps away)

(2x domains => need another server to redirect)
(as a student my living situations are variable and don't always have the option of static IP - better to rent a VPS (TODO define))
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
