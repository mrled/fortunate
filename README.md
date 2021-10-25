# Fortune databases

Databases for the `fortune` command.

## What is this?

Per [Wikipedia](https://en.wikipedia.org/wiki/Fortune_%28Unix%29),

> `fortune` is a program that displays a pseudorandom message from a database of quotations that first appeared in Version 7 Unix.

Here's an example:

```
$ fortune
Fortune favors the lucky.
```

This repo contains databases for use with the `fortune` command.

## Is there an online demo?

Why yes, I did indeed
[spend way too much time customizing a Linux emulator that runs inside your browser and lets you see the results](https://unfortunate.micahrl.com).
In fact, I can even embed it right here.
(It may take a few seconds to boot.)

<script src="https://unfortunate.micahrl.com/build/v86_all.js"></script>
<link rel="stylesheet" href="https://unfortunate.micahrl.com/v86.css">

<script>
"use strict";

window.onload = function()
{
    var emulator = window.emulator = new V86Starter({
        wasm_path: "https://unfortunate.micahrl.com/build/v86.wasm",
        memory_size: 256 * 1024 * 1024,
        vga_memory_size: 8 * 1024 * 1024,
        screen_container: document.getElementById("screen_container"),
        serial_container_xtermjs: document.getElementById("terminal"),
        bios: {
            url: "https://unfortunate.micahrl.com/bios/seabios.bin",
        },
        vga_bios: {
            url: "https://unfortunate.micahrl.com/bios/vgabios.bin",
        },
        cdrom: {
            url: "https://unfortunate.micahrl.com/unfortunate.iso",
        },
        autostart: true,
        disable_speaker: true,
        disable_keyboard: true,
    });
};
</script>

<div id="terminal"></div>
<div id="video-console-section" style="display:none">
    <h2>Video console</h2>
    <p>You cannot type here, but use this to watch the boot process</p>
    <div id="screen_container">
    <div style="white-space: pre; font: 14px monospace; line-height: 14px"></div>
    <canvas style="display: none"></canvas>
    </div>
    <br style="clear: both">
</div>

## What fortune databases are here?

1. [THE INVISIBLE STATES OF AMERICA](invisiblestates), some of my favorite microfiction from [@ThePatanoiac](https://twitter.com/ThePatanoiac)
2. [tweetfortune.py](tweets), a script to build fortune databases from a public Twitter timeline

## How do I use this?

1. Install `fortune`. This can be done on macOS with Homebrew or pkgin, or on Linux, BSD, and most other Unix variants with the standard package manager.

2. Build one of the databases here. Fortune's `strfile` can assemble the text files in this repo into databases:

        $ strfile invisiblestates/invisiblestates
        "invisiblestates/invisiblestates.dat" created
        There were 50 strings
        Longest string: 210 bytes
        Shortest string: 172 bytes

3. Run `fortune` against your newly built database:

        $ fortune invisiblestates/invisiblestates | fold -w 80 -s
        RUSH: Abandoned riverboats have been made into cathedrals by mermaids. There
        are giant toads here, whose legs are served with rose mustard.
        - THE INVISIBLE STATES OF AMERICA
          A TOURISM GUIDE BY UEL ARAMCHEK

## What is this for?

I think it is nice to put in your `.bashrc` or equivalent shell startup script.

## What other great tastes go great with this one?

- `fold -w 80 -s` will insert line breaks after a space at or before 80 characters. This command is actually [part of POSIX](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/fold.html#top) so should be on any Unix system.
- [lolcatjs](https://github.com/robertmarsal/lolcatjs) makes pretty colors.

Here's an example of those two in action:

![screenshot](fortune-invisiblestates-fold-lolcatjs.png)

## Other cool fortune databases

- [The top 10,000 /r/ShowerThoughts posts](https://nullprogram.com/blog/2016/12/01/)
