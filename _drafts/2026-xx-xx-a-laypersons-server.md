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

{% include toc %}

So, it's finally over! You've submitted your PhD thesis, found a job, and you have one last summer of independence before entering the perpetual grind.
There's only one thing for it: build some random personal projects, buy some domains, and waste a bunch of time hosting them on a server!
I went on this little odyssey over the last few months and learned a lot about how servers are managed in the cloud, and thought it would be nice to post about how I managed to figure it all out.
My server now hosts <https://theturboturnip.com>, which can be used to access this blog e.g. <https://theturboturnip.com{{ page.permalink }}>, and my custom web APIs <https://github.com/theturboturnip/turnip_api>.

<!--my Turnip-Search service with useful autocomplete **[Blogpost Pending]** along with my other web APIs .-->


<!--Aside from [watching movies](https://letterboxd.com/theturboturnip/), there is only one thing to do: screw around with personal projects and do very little of use!-->


I'm sure my setup is jankier than a professional devops work, but it *is* reliable, debuggable, and works in a way that I can understand as a non-devops-y, hardware-y, OS-y person.
The goal of this post is to explain briefly how some of these tools work from my perspective, and maybe even show you some new ways to think about them.

# Domains & Email

A year or so ago I bought the domain <https://theturboturnip.com>, having accepted that this username will forever be attached to my real identity.
For a while this website was hosted there, but once I started hosting my CV here I felt that the domain wasn't quite professional enough.
<!--A more professional -->
<!--That matched my GitHub username and for a while I used it to host this website.-->
<!--However, this website also includes my CV, and I felt that the domain didn't really match the level of professionalism I'd want to show potential employers.-->
I also wanted to start using the domain for email, which would have the same problem.
I ended up buying <https://samuelwstark.com>, where this website is now hosted, and keeping both domains active.
<https://theturboturnip.com> now redirects to <https://samuelwstark.com> to ensure old links stick around.

## Registering Domains

I initially registered <https://theturboturnip.com> with GoDaddy, but I would not recommend them.
Editing DNS was a pain, they kept trying to push website builder services on me, and they're overpriced.
I bought the domain for 3 years for £45 i.e. £15/yr ($20 USD/yr at time of writing).
<!--Notably this was advertised as £38, because tax was added later - Americans may be used to this, but here in the UK that's just not on.-->

When I started looking for <https://samuelwstark.com>, I poked around on Reddit and saw a few recommendations for [Porkbun](https://porkbun.com).
They have been great - they have a competent, utilitarian UI for changing DNS records, and they're about half the price.
It cost \$11 USD to transfer <https://theturboturnip.com> to Porkbun, it cost \$9 to register <https://samuelwstark.com> initially (there was a sale on), and the estimated yearly renewal price for each domain is also \$11.
On top of that, they carried over the rest of my 3-year term from GoDaddy before needing me to renew.
I would certainly recommend Porkbun. 

## Setting up Email

One of my guiding principles was "I don't want to rely on my server".
Servers are fickle things, they can go down, they can be attacked, they can lose data.
I am not a devops professional and I am not always going to be around to manage my server --- if anything happens, I need it to be recoverable.
Thus, anything truly important should be deferred to other services, even if it uses my domains.
Email hosting is one of those things.

<!--Proton struck a good balance for my goals of reputable (no issues sending/receiving emails) and configurable.-->
<!--I hate Microsoft's cloud suite, and I wanted to avoid Google - I already have quite a few eggs in that basket.-->
Microsoft and Google only support hosting email for custom domains if you have a business account, which I am not interested in.
<!-- https://learn.microsoft.com/en-us/microsoft-365/admin/setup/add-domain?view=o365-worldwide&tabs=domain-connect -->
<!-- -->
You can set up Gmail to send and receive emails from a custom domain *hosted elsewhere*, or set up a forwarding service with your hosting provider, but that defeats the whole point - I was looking for someone to host my email!
<!--https://www.reddit.com/r/gsuitelegacymigration/comments/14l04k6/comment/jptuujq/-->
<!--Probably not what you want to hear, but I‘d either pay for Workspace or not use Gmail (as in: Google‘s mail services). I can even give you an objective reason: forwarded emails will always be at risk to be labeled as spam either on your side or on the receiver‘s side. Those emails are also often marked as either insecure or marked as not coming from the original domain, depending on how you sent mails out (via a different smtp server or Gmails send as).-->
<!--On top of that, the forwarding services itself will apply spam filtering to make sure that their servers aren’t abused, so you add another point of failure. And if you use a different smtp server to send the mail, you would have to go find one that is not normally used for newsletters and marketing messages because you don’t want to send out your important personal emails via, for example, SendGrid. This means you would have to pay for a reputable email provider (so you get good scores) just to use their SMTP server.-->
<!--That‘s a lot of hoops to jump through just to get Gmail‘s UI.-->
Anyway, I already had eggs in their baskets, so I looked further afield.

[Fastmail](https://www.fastmail.com/) seemed reputable, and would be a good choice if I only wanted email and calendar, but it doesn't have an office suite or Google Drive equivalent.
[iCloud+](https://www.icloud.com/en-gb/icloudplus) allows custom email domains, and does cover more of the office suite, but it's all centered on the Apple ecosystem.
<!-- https://support.apple.com/en-gb/102540 -->
I ended up choosing [Proton](https://proton.me/) with the Unlimited plan (approximately £100/yr) to host email for both of my domains.
Their office suite is not quite as powerful, but it gets the job done, and I feel more comfortable holding sensitive files (e.g. work contracts, payslips, personal info) where they won't be scanned for AI and are less likely to arbitrarily disappear.
I've seen quite a few horror stories of Google capriciously deleting accounts, with no reversal process, due to vague "terms of service violations".

Setting up Proton Mail required some screwing around with DNS records, but the Proton website had [step-by-step instructions](https://proton.me/support/custom-domain), and Porkbun has a good interface for changing records.
It went off without a hitch.
Because of Proton's focus on encryption, the whole office suite including email and calendar requires you to use their apps specifically.
You can set up email forwarding and calendar sharing to avoid this, but it's less secure, and the apps are good so I haven't seen reason to.
<!--I can now send and receive email from both domains on my phone with Proton's app suite, and  -->

## Hosting a Blog

This blog is statically hosted using [GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site).
That's been the case since before I had any custom domains, and I haven't seen reason to change it.
<!--migrated this up from -->
<!--(static hosting with GitHub, need to move apps away)-->
The one issue I have had are my apps, hosted at <https://samuelwstark.com/apps>, which have large binaries and files that take up my Git LFS quota.
I'm considering moving those files to my server instead of hosting them through GitHub Pages, but I haven't gone through with that yet. 

# Renting a Server

GitHub Pages can only host one custom domain at a time, so once I got a second domain I needed a server to redirect one to the other.
Unless I start doing some wacky [Tailscale-esque](https://tailscale.com/) shenanigans, I can't use my own PC as the server.
<!-- https://www.reddit.com/r/selfhosted/comments/18491e9/tailscale_the_marvellous_tool_that_became/ -->
My home internet connection doesn't have a static IP address, my home PC is not always on, and I dual-boot Windows and Linux - so I would need to have a consistent server configuration on both sides if I wanted good availability.

I looked into full cloud computing at [AWS](https://aws.amazon.com/) and [Cloudflare](https://www.cloudflare.com/en-gb/developer-platform/use-cases/hosting/), but they both seemed far too complicated.
Cloudflare advertises compatability with "full-stack applications" based on huge JavaScript frameworks, AWS is designed for scaling out, and neither give a straight answer for "what can I buy if I just want to run some code on a single server".
There are also AWS Lambdas and Cloudflare Workers, both examples of ["serverless functions"](https://en.wikipedia.org/wiki/Serverless_computing) that you hypothetically deploy directly from the code you write, but again I find that much more difficult to get a handle on.
In general these services are complex enough that you risk spending far more than you expect, especially if something is misconfigured.
I just want a small, consistent bill and a server I can screw around with; so I rent a Virtual Private Server ([VPS](https://en.wikipedia.org/wiki/Virtual_private_server)).

There are many VPS providers.
Google Cloud claims to provide VPSs, but has the same opaque billing problems as AWS and Cloudflare, and seems to desparately try to push you towards "scalable" products.
I ended up choosing between [Hetzner](https://www.hetzner.com/) and [Netcup](https://www.netcup.com/en), two European providers.
This seemed to be a toss-up, and ultimately I chose Hetzner because Netcup gave me a coupon that didn't work.
I can vouch that Hetzner has been a great no-nonsense provider, but I'm sure Netcup would have worked just as well.

AWS does actually provide VPSs through [AWS Lightsail](https://aws.amazon.com/lightsail/pricing/), which to their credit does have explicit pricing - it's just more expensive.
I got my VPS on a Hetzner sale for \$6 USD/month, which includes static IPv4 and IPv6, 2 vCPUs, 4GB RAM, and a 40GB disk.
At time of writing, the AWS price for a comparable server is \$24/mo.
There are also some other reasons to avoid AWS - I prefer pure European hosting for latency, and because the EU is better on privacy than the US (except for [Chat Control](https://fightchatcontrol.eu)).
I also don't really want to use Amazon any more than I need to, considering their generally [inhumane working practices](https://www.theguardian.com/technology/2026/apr/22/amazon-workplace-safety-record) and Bezos' [capitulation to authoritarianism](https://www.wsj.com/business/jeff-bezos-donald-trump-relationship-7e6a742e).


<!--(2x domains => need another server to redirect)-->
<!--(as a student my living situations are variable and don't always have the option of static IP - better to rent a VPS (TODO define))-->
<!--(hetzner, also considered netcup but I had an issue with a voucher not working and got a better vibe for hetzner)-->
<!--(I use hetzner for a public IPV4, IPV6, and the cheapest server money can buy)-->

## Setting up the Server

My Hetzner VPS is a virtual machine running on Hetzner-owned hardware.


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
