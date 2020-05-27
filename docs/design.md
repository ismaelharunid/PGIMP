# PillowCase Design

PillowCase an extended set of class that wrap the PIL package, deigned to be more usable for complete graphic manipulation, drawing with bezier sequence support.

The core feature are a set of classes that inherit from Drawable.  These include both Simple, Tiled and Layered Drawable classes.  The Abstract Drawable class itself includes an image instance and proxy methods of that image property.

# PillowCase Class and Interface summary

## The abstract Drawable class

This is used both as an interface for the use classes and includes core functionality for extended drawing methods, namely the inclusion of stroke width and smoothing for all draw methods, and extended fill options for methods that utilize filling, and finally dynamic text layers which can be modified and rendered of pasting, export or display.

## The abstract Renderable class

This is used both as an interface for the use classes and extends the abstract Drawable class and implements hook methods for maintaining rendering functionality.  It is the template for drawables which contain dynamic image information such as text, path and models.  This abstract class may also be used as a Mixin when extending other classes.

## The abstract Vector class

This is used both as an interface for the use classes and extends the abstract Renderable class and implements hook methods for maintaining segment and line sequence functionality.  It is implemented by the DrawablePath, DrawableModel and various specialized Drawable classes

## The SimpleDrawable class

This is the simplest full implemented Drawable class, which simple includes a PIL.Image.Image instance with proxy methods to it.

## The TiledDrawable class

This is the functionally the same as the SimpleDrawable class, except that the it uses an image grid and is suitable for very large image layers or to reduce memory usage. 

## The LayeredDrawable class

This is the functionally the same as the SimpleDrawable class, but also implements the abstarct Renderable class with support for layered sub-drawables. 

## The DrawablePath class

Support for line and various path types, such as cubic Bezier.


## The DrawableModel class

Same as the DrawablePath except it also supports faces with 2 or more dimensions.

# PillowCase Class and Interface reference

TBA


> Written with [StackEdit](https://stackedit.io/).
