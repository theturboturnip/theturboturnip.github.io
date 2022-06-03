---
title: 'Hacking Lego City Undercover: Shadowmap Resolution'
date: 2022-06-04
permalink: /posts/2022/06/hacking-lcu-shadows/
tags:
  - hacking
  - graphics injection
  - lego city undercover
---

TODO this focuses on the shadowmap bits and kinda sucks lol

<!-- Hello, and welcome to my first blog post! -->
Recently, I've been replaying Lego City Undercover.
<!-- It's an open-world take on the classic Lego formula, and it holds a special place in my heart as my favourite Lego game. -->
It's an open-world take on the classic Lego formula, and the sheer variety of locations make it my favourite Lego game to 100% complete.
The 2017 rerelease had a few technical hiccups on PC, but the one I felt most equipped to handle was the low shadowmap resolution.
In this blog post, I'll explain basic game rendering, how shadowmaps and cascaded shadowmaps work, and how to efficiently(ish) force a game to do what you want.

## Shadowmaps? Resolution?

First, some terminology.
The process of taking a game world and turning it into an image onscreen is called *rendering*.
That resulting image (and indeed most computer images) are represented as a grid of *pixels*.
The number of pixels an image has is known as the *resolution* of the image.
For example, the below images are 50-by-50 pixels and 500-by-500 pixels - the difference should be clear.
Higher resolution images are sharper and more detailed.

<figure>
<figcaption>TODO: A 50x50 image and a 500x500 image</figcaption>
</figure>

So when a game is rendering its world, and it wants to draw lights and shadows, it needs to ask a fundamental question of each pixel/onscreen point.

<blockquote>
Is there any light-blocking object between the light and the point? 
</blockquote>

If there is anything between the point and the light, then the point should be in shadow.
Otherwise, it is directly lit.

<figure>
<figcaption>TODO: example of asking the question</figcaption>
</figure>

A *shadowmap* is an efficient way to answer this question.
The game effectively takes a picture from the perspective of the light.
Instead of colour, this image uses *depth* - how far away each point was from the light.
We make sure that closer things render on top of things that are farther away, so the image holds the depth of the closest solid object

<figure>
<figcaption>TODO: example shadowmap</figcaption>
</figure>

For each point in the final image, the question can then be split into two:

1. Where is this point from the perspective of the light?
  - We can use this to look up the depth-of-the-closest-solid-object in the shadowmap
2. Are we the closest point to the light?
  - 


<!-- When a game wants to draw the shadows of various objects on screen, one of the most common techniques is to render a *shadowmap*.
The game effectively takes a picture from the perspective of a light, except the picture stores *depth* (distance from the light) instead of colour.
This is a shadowmap: a picture where each pixel holds the depth of the closest object to the light.

TODO: example of a shadowmap

When the game renders the main scene, it then asks a set of questions about each pixel it renders.
1. Where am I with respect to the light?
   - This determines where the point would be on the shadowmap.
2. 
             -->