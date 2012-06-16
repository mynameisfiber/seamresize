# Seam Resize #

This little script will resize images using seam extraction instead of croping or scaling.  Essentially what it does is find paths that are "uninteresting" (ie: have a small sum over the square of the sobal transformation fo the image) and extracts them.  What results is a rescaled image that looks the same.  For example

##### Original:
![picture alt](https://github.com/mynameisfiber/seamresize/raw/master/torre-guaceto-beach.png "Original")

##### Resized:
![picture alt](https://github.com/mynameisfiber/seamresize/raw/master/torre-guaceto-beach-seamed.png "Scaled")


## TODO ##

* Make it so you can make an image larger
* Speed up path finding algorithm (fortran?)
* Interface to manually change regions' weighting
