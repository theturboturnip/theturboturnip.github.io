---
layout: single
title:  "On Domains and Servers"
permalink: /posts/2026/09/on-domains-and-servers
categories: 
  - Side Projects
tags:
  - vps
  - hetzner
  - docker
  - rust
  - qemu
  - ssh
  - networking
author_profile: true
excerpt: After submitting my PhD thesis, one of my side projects over my final(?) unemployed summer has been setting up a couple of domains and a server. You remember those things, servers? Those things we all used before lambdas, workers, microservices, etc.? Well, I found one in the wild, and I wrangled it just right, and now I'm here to talk about it.

---

{% include toc %}

After submitting my PhD thesis, one of my side projects over my final(?) unemployed summer has been setting up a couple of domains.
I already had <https://theturboturnip.com>, which hosted this blog with GitHub Pages, but then I added <https://samuelwstark.com> to the stable to seem somewhat professional, and then I had this wonderful idea for [some custom web APIs](https://github.com/theturboturnip/turnip_api) and started foolishly dreaming of a real server.

You remember those things, servers?
Those things we all used before lambdas, workers, microservices, etc.?

Well, I found one in the wild, and I wrangled it just right, and now I'm here to talk about it.

<!--got one set up.-->
I have tried to use vaguely appropriate technologies that those dev-ops folks might approve of, which has required me to struggle through a lot of inscrutable documentation.
<!--I must say th-->
Dev-ops are in an odd place, I think, because so much of this technology can be grokked pretty easily *if* you have a deep computing background ("Docker? Well, that's just [chroot](https://wiki.archlinux.org/title/Chroot) and [namespaces](https://man.archlinux.org/man/namespaces.7.en). Kind of.").
Unfortunately, if I'm anything to go by, that sort of background takes around 8 years to develop.
Anyone who doesn't have that kind of time to spare has to learn the abstraction itself, not the underlying technology, and so you end up with a lot of documentation that assumes you know both too much ("Of course we all know what images, stages, and layers are!") and not enough ("What data does an image actually contain? Don't worry your little head about it!").

In any case, this post goes through the different steps and tools I went through to get my server set up.
Right now it hosts <https://theturboturnip.com>, which redirects to this blog e.g. <https://theturboturnip.com{{ page.permalink }}>, and hosts my set of [turnip_apis](https://github.com/theturboturnip/turnip_api).
I'm sure it's jankier than what a professional would come up with, but it is reliable, it is debuggable, and it works in a way I can understand.
Hopefully by the end you will as well!

<!--This blog post is the result of my spelunking through a lot of DevOps documentation that seems to assume the reader knows both too much and not enough.-->
<!--I, as a hardware-y, OS-y, non-devops-y person, have traversed -->
<!--
It was finally over! I submitted my PhD thesis, found a job, and I had one last summer of independence before entering the perpetual grind.
There's only one thing for it: build some random personal projects, buy some domains, and waste a bunch of time hosting them on a server!
I went on this little odyssey over the last few months and learned a lot about how servers are managed in the cloud, and thought it would be nice to post about how I managed to figure it all out.-->
<!--I now have two domains: <https://samuelwstark.com>, which hosts this blog with GitHub Pages, and <https://theturboturnip.com>, a server which redirects to this blog e.g. <https://theturboturnip.com{{ page.permalink }}> and hosts my custom web APIs <https://github.com/theturboturnip/turnip_api>.-->

<!--my Turnip-Search service with useful autocomplete **[Blogpost Pending]** along with my other web APIs .-->
<!--Aside from [watching movies](https://letterboxd.com/theturboturnip/), there is only one thing to do: screw around with personal projects and do very little of use!-->

<!--I'm sure my setup is jankier than a professional dev-ops work, but it's reliable, it's debuggable, and it works in a way that I can understand as a hardware-y, OS-y, non-dev-ops-y person.-->
<!--The goal of this post is to explain how I figured this all out, and hopefully by the end you'll be able to as well.-->
<!--briefly how some of these tools work from my perspective, and maybe even show you some new ways to think about them.-->

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
<!--Notably this was advertised as £38, because tax was added later --- Americans may be used to this, but here in the UK that's just not on.-->

When I started looking for <https://samuelwstark.com>, I poked around on Reddit and saw a few recommendations for [Porkbun](https://porkbun.com).
They have been great --- they have a competent, utilitarian UI for changing DNS records, and they're about half the price.
It cost \$11 USD to transfer <https://theturboturnip.com> to Porkbun, it cost \$9 to register <https://samuelwstark.com> initially (there was a sale on), and the estimated yearly renewal price for each domain is also \$11.
On top of that, they carried over the rest of my 3-year term from GoDaddy before needing me to renew.
I would certainly recommend Porkbun. 

## Setting up Email

One of my guiding principles was "I don't want to rely on my server".
Servers are fickle things, they can go down, they can be attacked, they can lose data.
I am not a dev-ops professional and I am not always going to be around to manage my server --- if anything happens, I need it to be recoverable.
Thus, anything truly important should be deferred to other services, even if it uses my domains.
Email hosting is one of those things.

<!--Proton struck a good balance for my goals of reputable (no issues sending/receiving emails) and configurable.-->
<!--I hate Microsoft's cloud suite, and I wanted to avoid Google --- I already have quite a few eggs in that basket.-->
Microsoft and Google only support hosting email for custom domains if you have a business account, which I am not interested in.
<!-- https://learn.microsoft.com/en-us/microsoft-365/admin/setup/add-domain?view=o365-worldwide&tabs=domain-connect -->
<!-- -->
You can set up Gmail to send and receive emails from a custom domain *hosted elsewhere*, or set up a forwarding service with your hosting provider, but that defeats the whole point --- I was looking for someone to host my email!
<!--https://www.reddit.com/r/gsuitelegacymigration/comments/14l04k6/comment/jptuujq/-->
<!--Probably not what you want to hear, but I‘d either pay for Workspace or not use Gmail (as in: Google‘s mail services). I can even give you an objective reason: forwarded emails will always be at risk to be labeled as spam either on your side or on the receiver‘s side. Those emails are also often marked as either insecure or marked as not coming from the original domain, depending on how you sent mails out (via a different smtp server or Gmails send as).-->
<!--On top of that, the forwarding services itself will apply spam filtering to make sure that their servers aren’t abused, so you add another point of failure. And if you use a different smtp server to send the mail, you would have to go find one that is not normally used for newsletters and marketing messages because you don’t want to send out your important personal emails via, for example, SendGrid. This means you would have to pay for a reputable email provider (so you get good scores) just to use their SMTP server.-->
<!--That‘s a lot of hoops to jump through just to get Gmail‘s UI.-->
Anyway, I already had eggs in their baskets, so I looked further afield.

[Fastmail](https://www.fastmail.com/) seemed reputable, and would be a good choice if I only wanted email and calendar, but it doesn't have an office suite or Google Drive equivalent.
[iCloud+](https://www.icloud.com/en-gb/icloudplus) allows custom email domains, and does cover more of the office suite, but it's all centered on the Apple ecosystem.
<!-- https://support.apple.com/en-gb/102540 -->
I ended up choosing [Proton](https://proton.me/) with the Unlimited plan (approximately £100/yr) to host email for both of my domains.
Their office suite is not quite as powerful, but it gets the job done, and I feel more comfortable holding sensitive files (e.g. work contracts, payslips, personal info) where they won't be used for AI training and are less likely to arbitrarily disappear.
I've seen quite a few horror stories of Google capriciously deleting accounts, with no reversal process, due to vague "terms of service violations".

Setting up Proton Mail required some screwing around with DNS records, but the Proton website had [step-by-step instructions](https://proton.me/support/custom-domain), and Porkbun has a good interface for changing records.
It went off without a hitch.
Because of Proton's focus on encryption, the whole office suite including email and calendar requires you to use their apps specifically.
You can set up [an email bridge](https://proton.me/mail/bridge) and [calendar sharing](https://proton.me/support/share-calendar-via-link) to avoid this, but it can be less secure, and the apps are good so I haven't seen reason to.
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
My home internet connection doesn't have a static IP address, my home PC is not always on, and I dual-boot Windows and Linux --- so I would need to have a consistent server configuration on both sides if I wanted good availability.

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

AWS does actually provide VPSs through [AWS Lightsail](https://aws.amazon.com/lightsail/pricing/), which to their credit does have explicit pricing --- it's just more expensive.
I got my VPS on a Hetzner sale for \$6 USD/month, which includes static IPv4 and IPv6, 2 vCPUs, 4GB RAM, and a 40GB disk.
At time of writing, the AWS price for a comparable server is \$24/mo.
There are also some other reasons to avoid AWS --- I prefer pure European hosting for latency, and because the EU is better on privacy than the US (except for [Chat Control](https://fightchatcontrol.eu)).
I also don't really want to use Amazon any more than I need to, considering their generally [inhumane working practices](https://www.theguardian.com/technology/2026/apr/22/amazon-workplace-safety-record) and Bezos' [capitulation to authoritarianism](https://www.wsj.com/business/jeff-bezos-donald-trump-relationship-7e6a742e).


<!--(2x domains => need another server to redirect)-->
<!--(as a student my living situations are variable and don't always have the option of static IP --- better to rent a VPS (TODO define))-->
<!--(hetzner, also considered netcup but I had an issue with a voucher not working and got a better vibe for hetzner)-->
<!--(I use hetzner for a public IPV4, IPV6, and the cheapest server money can buy)-->

## Cloud-init for basic setup

My Hetzner VPS is a virtual machine running on Hetzner-owned hardware.
When you create a new Hetzner VM with the web interface, you have the option to select a base image (the initial operating system, I stick with Debian personally) and to provide a [cloud-init](https://docs.cloud-init.io/en/latest/explanation/introduction.html) script.
I find it important to use cloud-init to make sure crucial hardening steps are performed ASAP.
Once a server is exposed to the public internet, it will be attacked by malicious actors immediately and constantly, so it is important to:

- Upgrade all packages, to keep security patches up to date
- Configure `ufw` to block attackers from connecting to arbitrary ports
  - Most of your machine's ports do not need to be open, and should be closed.
- Configure `fail2ban` to blocking attackers who fail login attempts
  - Attackers will try to login using common username/password combinations, fail2ban blocks them if they fail
  - There are [arguments against fail2ban](https://j3s.sh/thought/fail2ban-sux.html), though I haven't looked at them thoroughly, so I may revert this at some point.
- Configure SSH to only allow login with a known keypair, and disable username/password authentication.

Password logins are guessable by attackers, you have to enter them manually which is error-prone, and they're just better off avoided.
Hetzner generates a random root account password each time you re-create the VM, and if you wanted to use password login you'd need to remember a new password each time, which makes it harder to interact with the server automatically. 
Instead, I generated a single [SSH key pair](https://wiki.archlinux.org/title/SSH_keys), and my cloud-init script sets up a user with that pair's *public key*, which means I (as the only person who knows the *private key*) can always log in.
It's more secure and easier than a password.

I initially based my cloud-init script off of [this tutorial](https://community.hetzner.com/tutorials/basic-cloud-config), and then I also found a [cloud-init generator](https://deployn.de/en/hetzner-cloud-init/) with a few more features.
You should definitely use a generator or template initially, as it will include things you haven't thought of that could be useful, but you should also take the time to understand what it's doing.
cloud-init is little more than a set of shell commands to run --- it should be self explanatory.
This script is the first line of defence for your server, and if there's anything fishy you should figure out why it's there.

<!--(initially I provisioned it with a basic cloud-init script and poked at it manually --- i got things wrong. Not so wrong as to be attacked, but still wrong. I would recommend reading through other people's scripts and setups and starting from there, they will likely have thought of things you didn't.)-->


<!--(nicer than an init script)-->

<!--(necessary to set up firewalls and ssh keys as early as possible --- the public internet is a hostile environment)-->

<!--(try and find the two places I generated my script from)-->


### Re-initing the server

When I want to change how my server works and what it does, I prefer to completely wipe it and start over instead of stacking changes on top while it's still running.
This makes sure the setup is rock solid and doesn't depend on leftover state, and makes it easier for me to migrate to a different provider if I ever wanted to.
My first few configurations relied on using the Hetzner web console to provision a new server, which allowed me to paste in a cloud-init script, and then delete the old one --- but my server has a special pricing deal, and provisioning a new one would revert to a more expensive price.
<!--The web console does not (to my knowledge) give you the ability to run cloud-init on an excisting-->
Instead, I use the [Hetzner Cloud API `/rebuild` endpoint](https://docs.hetzner.cloud/reference/cloud#tag/server-actions/rebuild_server) which wipes the server and reboots it with a new cloud-init script all in one go.
<!--(hetzner has an API endpoint for reimaging servers with new cloud-init, which i relied on to make sure I kept my cheap server)-->

## Ansible for complex setup

Once the server is secure, I initialize it more thoroughly.
This requires downloading more packages, editing configuration, and starting up background services --- as time consuming and finnicky process that would be a pain to go through manually.
Instead, I use [Ansible](https://github.com/ansible/ansible) to configure the server automatically.
The flow is pretty simple: you write a bunch of YAML files that describe how different services need to be set up and kicked off, and then you run Ansible on your local machine and point it at the server.
Ansible runs the necessary commands on the server and leaves it fully set up.
<!--(ansible runs from a different computer and targets the server --- you don't need to copy it into the server itself!)-->

I based my Ansible config on [this repository from Eric Driussi](https://github.com/EricDriussi/host-your-own/), though I changed quite a lot of it.
It references RSA-based SSH keys throughout, which I recommend switching to the newer ED25519 standard.
I switched the [nginx](nginx.org) web server for [Caddy](https://caddyserver.com/), which enables HTTPS automatically instead of needing a separate service.
I turned off most of the services it comes with (the [Nextcloud](https://nextcloud.com/) office suite, [Gitea](https://github.com/go-gitea/gitea) git server, [Vaultwarden](https://github.com/dani-garcia/vaultwarden) password manager, [Umami](https://github.com/umami-software/umami) analytics server, etc.) but I used their config files as a base for my own services like [turnip_api](https://github.com/theturboturnip/turnip_api).
This massively reduced the amount of persistent state on the server.
In fact, it reduced it to zero save for HTTPS certificates [(see below)](#caddy) and service configuration files.
That means it's enough to keep copies of the server configuration and I don't need to do backups of the server state, which is a big plus.
<!--(based on this person's base --- I would recommend changing some things, esp the RSA-based SSH key to ED25519.)-->
<!--(i tore out everything I didn't need, which is to say most of it. this has kept the server stateless, which might not be the case forever, but does allow me to avoid doing backups. if something goes wrong, I can reimage and consistently get the same result, and if the server itself is attacked the 'important data' is minimal --- just a few API keys.)-->

### Ansible alternatives

I briefly considered [Nix and NixOS](https://nixos.org/) as an alternative to Ansible.
Nix is a tool for reproducible package management: you write a config file declaring what packages you need for a specific workload, it downloads and installs an immutable environment for that workload, and it runs that workload in that environment the same way every time.
Different workloads are run in completely separate isolated environments, avoiding issues if two workloads depend on different versions of a dependency.
NixOS is a Linux distribution that extends this principle to the entire system, allowing users, SSH keys, and other configuration to be controlled by the Nix description language.

In theory, this should be enough to replace cloud-init and the Ansible config entirely.
However, I wasn't completely confident in its ability to handle security patches and upgrades.
In general, Nix is designed to pin versions, so what happens if a security patch comes along?
Would I have to keep looking at the server, regenerating the config for every new patch?
I use [unattended-upgrades](https://wiki.debian.org/PeriodicUpdates) specifically to avoid doing that!

I was also a little unsure how it would handle global system state.
My [turnip_api](https://github.com/theturboturnip/turnip_api) can do time zone conversions, and it does them using the server's OS-level time zone info.
I designed it that way on purpose because [some countries are threatening to change how their time zones work](https://www.bbc.co.uk/news/articles/cz9l9venjd8o) and I don't want to have to rebuild the API service if that happens.
I just want to treat it like any other OS upgrade: download, reboot, and move on; but that would mean the timezone info isn't isolated or reproducible by Nix's standards and I don't want to figure that out.
<!--Unfortunately I've had problems in the past with isolation and sandboxing features -->
<!--depends on the system's time zone database for time conversions, so that I won't have to rebuild it if countries change their time zones [like the US is threatening to do](), and I've had problems in the past with isolation and sandboxing features breaking this sort of system-wide -->

These may be unfounded fears --- I haven't done a deep enough dive into NixOS to understand how it would handle these cases --- but they were enough to tip me towards Ansible for now.
I have also heard anecdotally that the Nix language/specification is still in flux and not super well documented, which tipped me further.
I'll look at it again once it's more mature, but for now I'm happy with Ansible.

<!--(decided against nixos and immuatability to allow e.g. security patches through unattended-upgrades, timezone file updates)-->

## Caddy for HTTP(S)

As noted above, I use [Caddy](https://caddyserver.com) instead of the more mature [nginx](nginx.org).
This is because I am lazy.
I want my server to support HTTPS, which means it has to fetch [SSL certificates](https://www.cloudflare.com/learning/ssl/what-is-an-ssl-certificate/) from a trusted certificate authority like [Let's Encrypt](https://letsencrypt.org/).
<!--I want my server to support HTTPS, which requires it to periodically fetch new SSL certificates from a trusted certificate authority like [Let's Encrypt]().-->
These certificates are used to *authenticate* me to users: my server shows them the certificates, users can check them against the certificate authorities they trust, and it proves that (for a set period of time) *this* server is the only legitimate source of <https://theturboturnip.com> information.
These certificates eventually expire and need to be periodically renewed by the server.
<!--When a new user connects, you show them the certificate, and they can check it against their trusted certificate authorities so they know it's authentic.-->
<!--This is quite easy nowadays, because authorities like [Let's Encrypt]() give you certificates for free, but you still need to go ask them for new certificates regularly.-->
Under nginx I would have to use a seprarate service like [certbot](https://certbot.eff.org) to renew them, which is [somewhat non-trivial to set up](https://certbot.eff.org/instructions?ws=nginx&os=ubuntufocal), and I just don't want to bother.
Caddy does it all for me.
<!--(nginx requires a bunch of extra certbot things for HTTPS --- don't worry! use caddy!)-->

These certificates are also the only instance of persistent state on my server.
When I rebuild the server, I have a special workflow to copy certificate data off and then copy it back once the server is ready again.
<!--(that said, caddy does require the 'data directory' to be kept consistent. I have a workflow to copy it off the server and then copy it back after reimaging so it can persist.)-->

In terms of actual configuration, I set Caddy up to do three things:

1. Redirect all requests to <https://theturboturnip.com> to <https://samuelwstark.com>
2. Redirect all requests to <https://www.theturboturnip.com> to <https://samuelwstark.com>
3. Handle requests for <https://api.theturboturnip.com> by sending them to the [turnip_api](https://github.com/theturboturnip/turnip_api) executable, which is listening on `localhost:3000`.

## Docker for turnip_api

The [turnip_api](https://github.com/theturboturnip/turnip_api) executable is written in Rust.
In order to get it running on the server, I'd either need to compile it locally and copy it over to the server, or compile it on the server itself.
[Docker](https://docker.com) provides a convenient way to do the latter, and also allows me to run the executable inside a container.
Containers execute processes within a separate(ish) filesystem and network from the rest of the machine, while still using the same OS kernel.
<!--They aren't completely isolated like they would be in a virtual machine, -->
This allows me to share some files with turnip_api, like the system-wide timezone data, but not others --- which helps limit the blast radius if turnip_api is ever compromised by an attacker (though container security is much weaker than other forms of isolation such as VMs).
<!--This allows me to directly control what files turnip_api can see, which helps limit the blast radius if turnip_api is ever compromised by an attacker, and -->
<!--Containers are a limited form of sandbox, which limits the files that the contained process can see.-->
<!--Basically, a container allows me to limit the files that turnip_api can see.-->
<!--That means if turnip_api has a security flaw, an attacker would -->
<!--As far as I care, the container is useful for two reasons.
It limits the files that turnip_api can touch, which reduces the blast radius if it ends up being compromised, and it isolates turnip_api's view of the network.-->
<!--turnip_api can open what it thinks is port 80, and Docker will redirect it to the server's -->
<!--Containers are a limited form of sandbox, which limits how the contained process a limited view of the system and a limited -->
<!--(The effectiveness of this sandboxing is )-->

Docker has a lot of documentation, but I found most of it to be too high-level for me.
After some digging, I figured the best way to go was to write a Dockerfile for turnip_api based on the [Rust Dockerfile example](https://docs.docker.com/guides/rust/).
This Dockerfile splits the process into two ["stages"](https://docs.docker.com/build/building/multi-stage/): build and run.
<!--This demonstrates another interesting benefit of containers.-->
<!--The system Docker uses for filesystem isolation also allows you to split the filesystem into layers.-->
The build stage, which pulls the source files from GitHub, installs the compiler, downloads dependencies from Cargo, and compiles them together, creates a lot of intermediate files you don't need to actually run the executable.
The final executable is copied out into a separate stage --- basically a separate container without any of the intermediate files --- and is thus a lot smaller.
 <!--puts all of those build files into one layer, and then copies the final executable out into a separate layer.-->
When the server runs the executable, all it needs is the 'run' stage and not the 'build' stage.
It doesn't need to download any of the 'build' files.
<!--and doesn't need to download them.-->
<!--The server still has to run the build process at startup, which will be isolated in a container just like the final executable, and then once it's done the build layer will be dropped and the executable will be the only thing left.-->
<!--When this runs on the server, the server will still go through the build process and create those files, but then once it's done it will get rid of them.-->
<!--(Dockerfiles are easier than you think (sort of) (follow the tutorial))-->
After building the Dockerfile, I published the turnip_api container image on the [Docker hub](https://hub.docker.com/repository/docker/theturboturnip/turnip_server/general).
This image contains the data generated by the executable stage, and my Ansible script tells the server to download the image and run the executable stage inside a container.
<!-- which means Docker has a copy of the executable stage's data.-->

This was my first time properly using Docker, and there were a few teething problems.
The biggest learning curve for me was to do with networking.
Docker isolates the container inside a separate network namespace from the rest of the machine, and if you want to communicate with a process running in a container you have to `EXPOSE` the container-port in the Dockerfile and then [`publish`](https://docs.docker.com/get-started/docker-concepts/running-containers/publishing-ports/) the container-port as a server-port.
I chose to publish turnip_api at the server's `localhost:3000`.
Any process listening on server-`localhost`, including port 3000, will only receive messages from *inside the server* --- so turnip_api cannot be directly contacted from the outside.
Caddy, on the other hand, is listening on `0.0.0.0`.
It can receive messages from outside the server, handle HTTPS encryption/decryption, and then it will *reroute* messages for `api.theturboturnip.com` to the server's `localhost:3000` --- this is exactly what we want.
<!--This is exactly what we want --- the port isn't accessible from outside, you can't ping <https://theturboturnip.com:3000> directly, but Caddy r internally all requests to `api.theturboturnip.com` are redirected to `localhost:3000` for turnip_api to handle.-->
However, for this to work, the executable inside the container has to listen on `0.0.0.0` and NOT `localhost`!
Just like server-`localhost` is only accessible by processes inside the server, container-`localhost` is only accessible by other processes *inside the container*.
For a process to receive messages from outside the container, it needs to listen on container-`0.0.0.0`.
<!--A process listening on server-`localhost` will only -->
<!--`0.0.0.0` is the -->
This was a pain to debug.
Do not make the same silly mistake as me and hardcode the executable to bind to `localhost`!
I ended up making both the port and the listening IP for turnip_api configurable through environment variables, and [the turnip_api Dockerfile](https://github.com/theturboturnip/turnip_api/blob/main/Dockerfile) sets those variables before running.


## QEMU for testing

Testing is important, and anything involving shell scripting is going to be finnicky.
I wanted a way to test my cloud-init and Ansible setups without shutting down and rebuilding my server every time I made a change, so I put together a little something based on QEMU virtual machines.
[QEMU](qemu.org) is a full-system emulator program.
You set up the machine through command-line arguments, setting how much RAM it should have, what disks should be mounted, etc., and it runs everything inside a single process on the host machine.
By default it will emulate the CPU with just-in-time compilation, just like popular game console emulators such as [Dolphin](https://dolphin-emu.org/blog/tags/JIT/), or you can use a [hypervisor](https://en.wikipedia.org/wiki/Hypervisor) to run the emulated CPU as a native virtual machine.

The first step is grabbing the correct operating system disk image.
My server uses Debian 13, and Debian has a set of cloud-ready images hosted at <https://cloud.debian.org/images/cloud/>.
In my case, the relevant Debian 13 image is found at <https://cloud.debian.org/images/cloud/trixie/latest/debian-13-generic-amd64.qcow2>.
`debian-13` is self-explanatory, `generic` means it's the generic cloud-ready image and will run cloud-init on boot, `amd64` is for 64-bit x86 machines (which the real server is, so I keep it the same for consistency) and `qcow2` is a compressed disk image format that QEMU and many other tools can read.

<!--it's important to use `generic` or `genericcloud` because they actually run cloud-init scripts-->
This isn't the only disk image it needs.
`cloud-init` is set up to search for initialization scripts from various sources, and one way to provide them is through a separate disk image mounted as a CD drive or similar.
[The `cloud-init` tutorial](https://docs.cloud-init.io/en/latest/howto/launch_qemu.html) has more details about this, but ultimately I regenerate this disk image every time using this command:

{% raw %}
```
genisoimage \
  -output "{{IMAGES}}/local-cloud-init.iso" \
  -volid cidata -rational-rock -joliet \
  -graft-points user-data={{PAYLOAD}}/cloudinit meta-data=/dev/null network-config=/dev/null
```
{% endraw %}

- `-volid` sets the VOLume ID of the image, naming it 'cidata', [so that cloud-init detects it as a valid source](https://docs.cloud-init.io/en/latest/reference/datasources/nocloud.html#source-2-drive-with-labeled-filesystem).
- `-rational-rock` and `-joliet` are compatability options for the ISO filesystem.
- `-graft-points` and its arguments create three files 'user-data', 'meta-data', and 'network-config' on the filesystem --- 'user-data' is the actual cloud-init script, and I don't use the others so I set them as `/dev/null` to keep them empty.

When running the actual virtual machine, it's important to always use a copy of the base OS image instead of overwriting it:

{% raw %}
```
rm -f "{{IMAGES}}/local.qcow2"
cp "{{IMAGES}}/debian-13.qcow2" "{{IMAGES}}/local.qcow2"
```
{% endraw %}

and then it is as simple as running QEMU:

{% raw %}
```
qemu-system-x86_64 -m 4g -net nic \
    -net user,hostfwd=tcp:127.0.0.1:2222-:2222,hostfwd=tcp:127.0.0.1:3000-:80 \
    -drive file={{IMAGES}}/local.qcow2,index=0,format=qcow2,media=disk \
    -drive file={{IMAGES}}/local-cloud-init.iso,index=1,media=cdrom \
    -machine accel=kvm:tcg \
    -daemonize
```
{% endraw %}

- `-net nic` tells QEMU to create an emulated network card.
- `-net user,...` tells QEMU to use [user-mode networking](https://wiki.qemu.org/Documentation/Networking), which emulates an entire TCP/IP network within QEMU, with some extra port forwarding options:
  - `hostfwd=tcp:127.0.0.1:2222-:2222` ensures that `127.0.0.1:2222` on the host (i.e. localhost port 2222) redirects to port `2222` on the emulated machine.
    - This is for SSH --- I use port 2222 instead of the default port 22, a choice inherited from the first cloud-init tutorial I used. In practice I don't believe it's a security benefit, but it does prove advantageous here. It means my scripts can always SSH into 2222 whether they are targeting the Hetzner server or the QEMU testbed.
  - `hostfwd=tcp:127.0.0.1:3000-:80` ensures that localhost port `3000` on the host redirects to port `80` on the emulated machine.
    - This allows me to send requests to the turnip_api server running on QEMU once the setup completes. Unfortunately you mostly cannot send requests targeting a specific domain to this port, so the HTTP server will need to be configured differently on QEMU. See below.
- `-drive file=local.qcow2` creates the main disk drive with the Debian copy.
- `-drive file=local-cloud-init.iso` loads the cloud-init ISO into an emulated CD drive.
- `-machine accel=kvm:tcg` configures QEMU to use the [KVM hypervisor](https://linux-kvm.org/page/Main_Page), which runs x86 instructions directly instead of emulating them and will be faster.
- `-daemonize` makes QEMU detach from the terminal instead of blocking until the VM has booted.

Running this command should open a QEMU console window, where you can watch the logs fly by as the cloud-init script executes.
<!--The QEMU window will stay open if the virtual machine reboots.-->
Once cloud-init is done, you can mostly just point Ansible at it, with a few exceptions. 
<!--(grab a cloud-init debian image and set it up correctly, keep the same cloud-init script (it is important to test!))-->

### QEMU-specific problems

QEMU user-mode networking is kind of weird, and doesn't point the virtual machine at a DNS server correctly.
You will have to reset the DNS servers on QEMU (but not on the real thing) if you want the server to make outbound connections --- say, to download Docker images or Debian packages.
On Debian, that may look something like this:

```
resolvectl dns ens3 8.8.8.8 8.8.4.4 || { echo "Setting DNS failed, exiting..." ; exit 1 ; }
```
<!--(QEMU user-mode networking (i.e. the easy networking) does weird DNS things --- I upload a setup script that updates to the correct DNS )-->

Next: if you point Ansible at 'localhost', it will assume it's been told to configure "the computer you are running this on" and [generate an implicit definition to that effect](https://docs.ansible.com/projects/ansible/latest/inventory_guide/implicit_localhost.html).
You can get around this by explicitly setting `ansible_connection = ssh`, which it would otherwise implicitly define, and ensuring all the SSH commands Ansible runs in this context use a non-standard port that connects to QEMU and not just your local machine.
<!--This is another benefit of using a non-standard SSH port --- a non-standard SSH port should never end up SSHing into your local machine.-->
<!--(ansible localhost weirdness - it thinks localhost = this computer, instead of a target named 'localhost')-->

Finally, as noted above, your HTTP server config must be different between QEMU and the real server.
At the very least, you need to make sure QEMU does not try to provision real HTTPS certificates for your domain --- it isn't the real server!
I set this up with a minimal Caddy configuration that completely ignores the domains and just redirects HTTP port 80 to turnip_api.
This means I can't test HTTP redirect behaviour for my domains, but I can still verify the server is running correctly by sending requests to turnip_api through host-`localhost:3000`.
Both this and my script for resetting the QEMU DNS rely on a `TURNIP_TARGET` environment variable that I set to `localhost` for QEMU and `theturboturnip.com` for the real thing.
Divergences like this are unfortunate but necessary, and the best we can do is remain aware of them and try to minimize them.
<!--(Caddyfile.localhost important --- don't try to provision HTTPS into your localhost!)-->


After all that, the testing process was very much worth it.
The vast majority of the bugs I encountered in this process were shell scripts doing something *slightly* wrong, which were much more tolerable to fix thanks to the improved iteration times of QEMU vs. the real server.
<!--Of course, it also avoids server downtime.-->


<!--(90% of the bugs I encountered over the course of this process were shell scripts doing something slightly different to what I want. This makes the iteration time on those bugs a lot nicer and avoids server downtime.)-->

# In conclusion

Wasn't that a thrilling ride?
Kept you on the edge of your seat?
I bet it was.
It even works!
Right now there's not much to show for it beyond the Turnip Search API, but that really does work --- you should be able to right click the URL bar and select "Add Search Engine" (Firefox) or right click the URL bar and select "Manage Search Engines" (Chrome/derivatives) or stare pensively into the middle distance, wondering what could have been (Safari) to install/use it.
I won't be able to do nearly as much with this stuff now that I have a Real Actual Job, but hopefully I'll still be able to pick at it here and there.
Until next time!
