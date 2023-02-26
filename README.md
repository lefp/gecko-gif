# gecko-gif

A simple Python/OpenCV script that turns this

![gecko-recolored](https://user-images.githubusercontent.com/70862148/221388294-5610b591-6d69-4c29-8135-2027f5f91bca.jpg)

into this

![HECKIN-GECKIN-L70r120-eye](https://user-images.githubusercontent.com/70862148/221388307-bdedf81f-f867-4a06-bdd8-0e679ff1ca99.gif)

.

Requires ImageMagick to be installed, because it calls `convert` to produce the GIF from frames.

There is a switch at the top of the code to toggle writing to file (in case you just want to see it, without saving).

There is another switch that produces a Discord profile-picture-sized version, because (when I wrote the code) Discord's auto-downscaling ruined the image.
