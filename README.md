# PillowCase
A PIL ImageDraw Wrapper with Image proxy class with combined methods and added functionality for drawing plus rudimentary layer support.

PIL is great although it could be a lot better.  In the meantime I created this Drawable class which simply extends PIL.ImageDarw.ImageDraw and adds proxy methods from the PIL.Image.Image instance used to create it.

The constructor argument order is changed to make defaults more practical.  Polygon Line methods changed to allow for stroke width, and moothing added to both polygon and line methods.  

Future enhancements will include filling out the rest of the drawing methods with additiona paint modes and methods, plus added rendering and tile support.

This is a quick and very functional class built on PIL, but the long term goal is to replace all the functionality in python with C library calls, add nessissary enhancements and optimize it.  But in the meantime this gets close to common requirements I have for supporting animation rendering.

