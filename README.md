# PGIMP (Python Graphic Image Manipulation Package)

Originally based on PIL ImageDraw Wrapper with Image proxy class with combined methods and added functionality for drawing plus rudimentary layer support.  The project has gone directly to being a wrapper for multiple low level graphic libraries.  Currently we are targeting Tk, however it includes a wrapper framework so it can be adapted to other libraries.   

Future enhancements will include filling out the rest of the drawing methods with additiona paint modes and methods, plus added rendering and tile support.

This is a quick and very functional class built to compete with PIL, the long term goal is to replace all the functionality in python with C library calls, add nessissary enhancements and optimize it.  But in the meantime this gets close to common requirements I have for supporting animation rendering.

