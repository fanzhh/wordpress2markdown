# wordpress2markdown
export wordpress's posts to markdown files contain images.

A few years ago, I once built my blog use wordpress. Later I learned markdown and enjoy it, now I built blog use [grav](https://getgrav.org/), a cms system based markdown file. I want to export my old blogs in wordpress into  grav system, so I write this code.

This file supposed you have copy your entire wordpress direcotry to local, and import the wordpress mysql database to your local mysql. Generally speaking, the path of images in a post in wordpress should in direcotry like this: 
```
(wordpress root direcotry)/wp-content/uploads/(year)/(month)/
```
This file's job is to read posts in wordpress and write it into a markdown file, at the same time copy the images in the posts into the markdown same direcotry and update links in markdown file.
