# Seam Resize #

This little script will resize images using seam extraction instead of cropping or scaling.  Essentially what it does is find paths that are "uninteresting" (ie: have a small sum over the square of the sobal transformation of the image) and extracts them.  What results is a rescaled image that looks the same without squeezing or scale abnormalities.  For example

##### Original:
![picture alt](https://github.com/mynameisfiber/seamresize/raw/master/torre-guaceto-beach.png "Original")

##### Resized Thin:
![picture alt](https://github.com/mynameisfiber/seamresize/raw/master/torre-guaceto-beach-seamed1.png "Thin")

##### Resized Square:
![picture alt](https://github.com/mynameisfiber/seamresize/raw/master/torre-guaceto-beach-seamed2.png "Square")


##### Original:
![picture alt](https://github.com/mynameisfiber/seamresize/raw/master/Earth and Moon.png "Original")

##### Resized:
![picture alt](https://github.com/mynameisfiber/seamresize/raw/master/Earth and Moon-seamed.png "Resized")

##### Stretched:
![picture alt](https://github.com/mynameisfiber/seamresize/raw/master/Earth and Moon-stretched.png "Stretched")
(You can see the artifacts from the stretching... it happens because, for some reason, the seaming algorithm always finds seams in the same region)

## TODO ##

* Make it so you can make an image larger
* Speed up path finding algorithm (fortran?)
* Interface to manually change regions' weighting
