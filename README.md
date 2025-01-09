# Micropython-ST7735

A Python Canvas Painter Interface for Micropython ST7735


# *** Canvas Painter v0.2 API TO ST7735 ***

# -- Construct the main object, bits should be 16 and window an ST7735 object

CanvasPainter(columns=128,rows=160,bits=16,window=None)

# -- Set the the window area to be draw (Mandatory, at least once)

setWindow(startX,endX,startY,endY,copy=True)

# -- Set the current color (Color type: COLOR_LINE, COLOR_FILL, COLOR_TRANSPARENCY)

setColor(R,G,B,colorType=CanvasPainter.COLOR_LINE):

# -- Restore to last previous color (Color type: COLOR_LINE, COLOR_FILL, COLOR_TRANSPARENCY)

restoreColor(colorType=CanvasPainter.COLOR_LINE):

# -- Clear current color (Color type: COLOR_LINE, COLOR_FILL, COLOR_TRANSPARENCY)

clearColor(colorType=CanvasPainter.COLOR_FILL):

# -- Set current border thikness

setThikness(thikness):

# -- Restore to last previous border thikness

restoreThikness():

# -- Set rotation to given degress, with the given x and y as origin (x and y should be the center of the image to rotate) call with empty args to set normal painting

setRotation(degress=0,xOrigin=0,yOrigin=0):

# -- Set a pixel with the current color

setPixel(xPos,yPos):

# -- Draw a line

drawLine(startX,endX,startY,endY):

# -- Draw a horizontal line

drawLineH(xPos,yPos,size):

# -- Draw a vertical line

drawLineV(xPos,yPos,size):

# -- Draw a rectangle, if "fill=True", fill with the fill color

drawRectangle(xPos,yPos,width,height,fill=False):

# -- Draw a square, if "fill=True", fill with the fill color

drawSquare(xPos,yPos,size,fill=False):

# -- Draw a circle, if "fill=True", fill with the fill color

drawCircle(xPos,yPos,radius,fill=False,startAngle=0,endAngle=360):

# -- Load image at given position from raw bytes (need to be same bit depth)

loadRaw(xPos,yPos,width,height,rawBytes)

# -- Load image at given position (need to be same bit depth)

loadImage(xPos,yPos,file)

# -- Load a font to print charecters as it is (need to be same bit depth)

loadFont(file):

# -- Print a given charecter

printChar(xPos,yPos,char):

# -- Print a given string 

printChars(xPos,yPos,chars):

# -- Write the contents to main buffer

flush():

# -- Save the main buffer as a bitmap ( before use this call flush() )

saveBitmap(file):
