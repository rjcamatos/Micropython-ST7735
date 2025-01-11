import struct
import random
import math

class CanvasPainterWindow:

    def __init__(self):

        self._bits = 0
        self._bytes = 0

        self._buffer = None
        self._columns = 0
        self._rows = 0

        self._windowBuffer = None
        self._windowColumnStart = 0
        self._windowColumnEnd = 0
        self._windowRowStart = 0
        self._windowRowEnd = 0
        self._windowColumns = 0
        self._windowRows = 0

    def setWindow(self,columnStart,columnEnd,rowStart,rowEnd,copy=True):

        self._windowColumnStart = columnStart
        self._windowColumnEnd = columnEnd
        self._windowRowStart = rowStart
        self._windowRowEnd = rowEnd
        self._windowColumns = self._windowColumnEnd - self._windowColumnStart
        self._windowRows = self._windowRowEnd - self._windowRowStart
        self._windowColumnSize = self._bytes
        self._windowRowSize = self._windowColumns * self._bytes
        
        if self._buffer == None:
            self._buffer = bytearray(self._columns*self._rows*self._bytes)

        self._windowBuffer = bytearray(self._windowColumns*self._windowRows*self._bytes)
        
        if copy == False: return

        nByte = 0
        R = self._windowRowStart * (self._columns*self._bytes)
        for r in range(self._windowRows):            
            C = self._windowColumnStart * self._bytes
            for c in range(self._windowColumns):
                for b in range(self._bytes):
                    self._windowBuffer[nByte] = self._buffer[R+C+b]
                    nByte += 1
                C += self._bytes
            R +=  self._columns*self._bytes

    def flush(self):
        nByte = 0
        R = self._windowRowStart * (self._columns*self._bytes)
        for r in range(self._windowRows):            
            C = self._windowColumnStart * self._bytes
            for c in range(self._windowColumns):
                for b in range(self._bytes):
                    self._buffer[R+C+b] = self._windowBuffer[nByte]
                    nByte += 1
                C += self._bytes
            R +=  self._columns*self._bytes

class CanvasPainter:

    COLOR_LINE = 0
    COLOR_FILL = 1
    COLOR_TRANSPARENCY = 2

    def __init__(self,columns=128,rows=160,bits=16,window=None):

        self._window = window
        if self._window == None: self._window = CanvasPainterWindow()
        self._window._columns = columns
        self._window._rows = rows
        self._window._bits = bits
        self._window._bytes = math.ceil(self._window._bits/8)
        self._window._buffer = None 

        self._flipV = -1
        self._flipH = -1

        self._rotation = 0
        self._xOrigin = 0
        self._yOrigin = 0

        self._color =  None
        self._tmpColor = None

        self._fillColor = None
        self._tmpFillColor = None

        self._transparencyColor = None
        self._tmpTransparencyColor = None

        self._thikness = 0
        self._tmpThikness = 0

        self._roundConers = True

        self._charTable = None

    def setWindow(self,startX,endX,startY,endY,copy=True):
        self._window.setWindow(startX,endX,startY,endY,copy)

        if self._fillColor != None and copy == False:
            self._window._windowBuffer = bytearray( self._fillColor *self._window._windowColumns*self._window._windowRows)
                        
        if self._fillColor == None and copy == False:
            for nByte in range(len(self._window._windowBuffer)):
                self._window._windowBuffer[nByte] = random.getrandbits(8)


    def setColor(self,R,G,B,colorType=0):
        
        color = None

        if self._window._bits == 8: #OK
            color = int((R<<5)&0xE0 | (G<<2)&0X1C | (B>>5)).to_bytes(1,'little')

        if self._window._bits == 16: #OK
            if self._window.__class__.__name__ == 'ST7735':
                color = int( (R&0xF8)<<8 | (G&0xFC)<<3 | (B&0xF8)>>3 ).to_bytes(2,'big')
            else:
                color = int( (R&0xF8)<<8 | (G&0xFC)<<3 | (B&0xF8)>>3 ).to_bytes(2,'little')
            
        if self._window._bits == 24: #OK
            color = int( (R<<16) | (G<<8) | (B) ).to_bytes(3,'little')

        if self._window._bits == 32: #OK
            color = int( (R<<21) | (G<<10) | (B) ).to_bytes(4,'little')

        if colorType ==  CanvasPainter.COLOR_LINE:
            self._tmpColor = self._color
            self._color = color

        if colorType ==  CanvasPainter.COLOR_FILL:
            self._tmpFillColor = self._fillColor
            self._fillColor = color

        if colorType ==  CanvasPainter.COLOR_TRANSPARENCY:
            self._tmpTransparencyColor = self._transparencyColor
            self._transparencyColor = color

    def restoreColor(self,colorType=0):
        if colorType == CanvasPainter.COLOR_LINE: self._color = self._tmpColor
        if colorType == CanvasPainter.COLOR_FILL: self._fillColor = self._tmpFillColor
        if colorType == CanvasPainter.COLOR_TRANSPARENCY: self._transparencyColor = self._tmpTransparencyColor

    def clearColor(self,colorType=1):
        if colorType == CanvasPainter.COLOR_LINE: self._color = None
        if colorType ==  CanvasPainter.COLOR_FILL: self._fillColor = None
        if colorType ==  CanvasPainter.COLOR_TRANSPARENCY: self._transparencyColor = None

    def setThikness(self,thikness):
        self._tmpThikness = self._thikness
        self._thikness = thikness

    def restoreThikness(self):
        self._thikness = self._tmpThikness

    def setRotation(self,degress=0,xOrigin=0,yOrigin=0):
            self._rotation = degress
            self._xOrigin = xOrigin
            self._yOrigin = yOrigin

    def _getOffset(self,xPos,yPos):
        return [xPos*self._window._windowColumnSize,yPos*self._window._windowRowSize]

    def setPixel(self,xPos,yPos):
        if self._color == None: return

        #IMPLEMENTATION OF ROTATION
        if self._rotation == 360: self._rotation = 0
        if self._rotation > 0:
            cos = math.cos(self._rotation*math.pi/180)
            sin = math.sin(self._rotation*math.pi/180)            
            
            cosX = cos*(xPos-self._xOrigin)
            sinX = sin*(xPos-self._xOrigin)
            cosY = cos*(yPos-self._yOrigin)
            sinY = sin*(yPos-self._yOrigin)

            xPos = int( cosX - sinY ) + self._xOrigin 
            yPos = int( sinX + cosY ) + self._yOrigin

        #OVERFLOW CHECK
        if (xPos-self._thikness) < 0 or (xPos+self._thikness) > self._window._windowColumns-1: return
        if (yPos-self._thikness) < 0 or (yPos+self._thikness) > self._window._windowRows-1: return

         #IMPLEMENTATION OF NEAR NEIGHBOR (FOR ROTATION PIXELATED CORRENTION)
         #THIS WORKS VERY BAD WTIH CHARECTERS, MAYBE NEED SPEED IMPLEMENTATION
        if self._rotation > 0 and self._thikness == 0:

            neighborCount = 0
            neighbor = [[0]*2]*8
            
            startOffset = self._getOffset(xPos,yPos)
            startOffset = int(self._flipH*(startOffset[0]))+int(self._flipV*(startOffset[1]))
            if self._window._windowBuffer[startOffset:startOffset+self._window._bytes] == self._color:
                for r in range(1,-2,-1):
                    for c in range(1,-2,-1):
                        if r == 0 and c == 0: continue
                        startOffset = self._getOffset(xPos+r,yPos+c)
                        startOffset = int(self._flipH*(startOffset[0]))+int(self._flipV*(startOffset[1]))
                        if self._window._windowBuffer[startOffset:startOffset+self._window._bytes] == self._color:
                            neighborCount += 1
                        else:
                            neighbor[r] = [r,c]

            if neighborCount > 3:
                for r in range(1,-2,-1):
                    for c in range(1,-2,-1):
                        if r == 0 and c == 0: continue
                        if neighbor[r][c] == 0: continue
                        startOffset = self._getOffset(xPos+r,yPos+c)
                        startOffset = int(self._flipH*(startOffset[0]))+int(self._flipV*(startOffset[1]))
                        self._window._windowBuffer[startOffset:startOffset+self._window._bytes] = self._color                        

        #IMPLEMENTATION OF SET THE PIXEL
        startOffset = self._getOffset(xPos,yPos)
        startOffset = int(self._flipH*(startOffset[0]))+int(self._flipV*(startOffset[1]))
        for nByte in range(self._window._bytes):
            self._window._windowBuffer[startOffset+nByte] = self._color[nByte]

        #IMPLEMENTATION OF BORDER THIKNESS
        for r in range(self._thikness,-self._thikness,-1):
            for c in range(self._thikness,-self._thikness,-1):
                if r == 0 and c==0: continue
                startOffset = self._getOffset(xPos+c,yPos+r)
                startOffset = int(self._flipH*(startOffset[0]))+int(self._flipV*(startOffset[1]))
                for nByte in range(self._window._bytes):
                    self._window._windowBuffer[startOffset+nByte] = self._color[nByte]


    def drawLine(self,startX,endX,startY,endY):
        width = (endX-startX)
        height = (endY-startY)

        len = math.sqrt(math.pow(width,2) + math.pow(height,2))
        rowInc = height/len
        rowStep = 1
        colInc = width/len
        colStep = 1

        for _ in range(int(len)):
            self.setPixel(startX+int(colStep),startY+int(rowStep)) 
            rowStep += rowInc
            colStep += colInc


    def drawLineH(self,xPos,yPos,size):
        rangeStep = int(self._thikness/2) + 1
        if size < 0: rangeStep *= -1

        for step in range(0,size,rangeStep):
            self.setPixel(xPos+step,yPos)
    
    def drawLineV(self,xPos,yPos,size):
        rangeStep = int(self._thikness/2) + 1
        if size < 0: rangeStep *= -1

        for step in range(0,size,rangeStep):
            self.setPixel(xPos,yPos+step)

    def drawRectangle(self,xPos,yPos,width,height,fill=False):
        if fill == True:
            self.setThikness(0)
            tmpColor = self._color
            self._color = self._fillColor
            rangeStep = self._thikness
            if self._thikness == 0: rangeStep = 1
            if height < 0: rangeStep *= -1
            for step in range(0,height-rangeStep,rangeStep):
                self.drawLineH(xPos+rangeStep,yPos+step+rangeStep,width-rangeStep)
            self._color = tmpColor
            self.restoreThikness()

        incW = 1
        incH = 1
        if width < 0: incW *= -1
        if height < 0: incH *= -1

        self.drawLineH(xPos,yPos,width)
        self.drawLineH(xPos,yPos+height,width+incW)
        self.drawLineV(xPos,yPos,height)
        self.drawLineV(xPos+width,yPos,height+incH)


    def drawSquare(self,xPos,yPos,size,fill=False):
        self.drawRectangle(xPos,yPos,size,size,fill)
 

    def drawCircle(self,xPos,yPos,radius,fill=False,startAngle=0,endAngle=360):

        if fill == True:
            self.setThikness(0)
            tmpColor = self._color
            self._color = self._fillColor
            for R in range(radius-self._thikness):
                if R < 1: continue
                len = ((2/360)*(endAngle-startAngle)) * math.pi * R
                inc = (endAngle-startAngle)/(len*2.3) # 2.3 is pixel resolution
                angle = startAngle
                while angle < endAngle:
                    x = int(R * math.cos(math.radians(angle)))
                    y = int(R * math.sin(math.radians(angle)))
                    self.setPixel(xPos+x,yPos+y)
                    angle += inc + (self._thikness/2)
            self._color = tmpColor
            self.restoreThikness()

        len = ((2/360)*(endAngle-startAngle)) * math.pi * radius
        inc = (endAngle-startAngle)/len
        angle = startAngle
        while angle < endAngle:
            x = int(radius * math.cos(math.radians(angle)))
            y = int(radius * math.sin(math.radians(angle)))
            self.setPixel(xPos+x,yPos+y)
            angle += inc + (self._thikness/2)

    def loadRaw(self,xPos,yPos,width,height,rawBytes):
        self._flipV *= -1
        sRow = 0
        for r in range(height):
            if (yPos+r) > self._window._windowRows: break
            sCol = 0
            for c in range(width):
                if (xPos+c) > self._window._windowColumns: break
                startOffset = self._getOffset(xPos+c,yPos+r)
                startOffset = int(self._flipH*(startOffset[0]))+int(self._flipV*(startOffset[1]))
                if self._transparencyColor != None:
                    color = rawBytes[sRow + sCol:sRow+sCol+self._window._bytes]
                    if color != self._transparencyColor:
                        self._window._windowBuffer[startOffset:startOffset+self._window._bytes] = color
                else:
                    for nByte in range(self._window._bytes):
                        self._window._windowBuffer[startOffset+nByte] = rawBytes[sRow + sCol + nByte]
                sCol += self._window._bytes
            sRow += width * self._window._bytes
        self._flipV *= -1

    def loadImage(self,xPos,yPos,file):
        image = open(file,'rb')

        image.seek(14)
        dib_header = struct.unpack_from('<IIIHHIIIIII',image.read(40))
   
        if dib_header[4] != self._window._bits:
            image.close()
            print("loadImage() WARNING: not same Bit depth !!!")
            return

        if dib_header[4] == 16 and dib_header[5] == 3:
            #print("LOAD DIB HEADER",dib_header)
            biColorMask= struct.unpack_from('<III',image.read(12)) #SEEK biColors Header

        width = dib_header[1]
        height = dib_header[2]
        raw = image.read()
        image.close()
        
        self.loadRaw(xPos,yPos,width,height,raw)        

    def loadFont(self,file,debug=False):
        self._charTable = open(file,'rb')
        
        self._charTableMatrix = file[file.rfind('-')+1:file.rfind('.bmp')].split('X')
        self._charTableMatrix[0] = int(self._charTableMatrix[0])
        self._charTableMatrix[1] = int(self._charTableMatrix[1])

        self._charTable.seek(14) #jump to dib header
        dib_header = struct.unpack_from('<IIIHHIIIIII',self._charTable.read(40))

        if dib_header[4] != self._window._bits:
            self._charTable.close()
            self._charTable = None
            print("loadFont() WARNING: charTable not same Bit depth !!!")
            return

        self._charTable = self._charTable.read()
    
        self._charTableWidth = dib_header[1]
        self._charTableHeight = dib_header[2]
        self._charTableCharWidth = int(self._charTableWidth/self._charTableMatrix[0])
        self._charTableCharHeight = int(self._charTableHeight/self._charTableMatrix[1])

        if debug == True:
            for nByte in range(self._charTableWidth*self._charTableHeight*self._window._bytes):
                self._window._windowBuffer[nByte] = self._charTable[nByte]

    def printChar(self,xPos,yPos,char,fontSize=8):
        if self._charTable == None: return

        charIndexs = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
        charIndex = charIndexs.find(char)
 
        atRow =  int(charIndex / self._charTableMatrix[0])
        atCol = charIndex - self._charTableMatrix[0]*atRow

        xRatio = self._charTableCharWidth / fontSize;
        yRatio = self._charTableCharHeight / fontSize;

        self.setThikness(0)
        sRow = atRow * self._charTableCharHeight * self._charTableWidth * self._window._bytes
        for r in range(fontSize):
            y = sRow + int(r*yRatio) * (self._charTableWidth * self._window._bytes)
            if y == sRow: continue
            sCol = atCol * int(self._charTableCharWidth * self._window._bytes)
            for c in range(fontSize):
                x = sCol + int(c*xRatio) * self._window._bytes
                if self._charTable[-(y)+(x)] != 0x00:
                    self.setPixel(xPos+c,yPos+r)
        self.restoreThikness()


    def printChars(self,xPos,yPos,chars,fontSize=8):
        if self._charTable == None: return

        for char in chars:
            self.printChar(xPos,yPos,char,fontSize)
            xPos += fontSize

    def flush(self):
        self._window.flush()

    def saveBitmap(self,file):
        headerSize = 0
        rawSize = self._window._columns*self._window._rows*self._window._bytes

        headerSize += 14 #BMP HEADER
        headerSize += 40 #DIB HEADER
        
        if self._window._bits == 8:
            headerSize += 4*256 #COLOR PALLET

        if self._window._bits == 16:
            headerSize += 4*3 #BI COLORS


        out_file = open(file,'wb')
        # --- THE BITMAP HEADER ---
        #--BMP HEADER 14 bytes
        bmp_header = struct.pack('<2sI2s2sI',
            b'BM',       #BmDescription
            headerSize+rawSize,      #FileSize #THE SISZE OF THE HEADER
            b'\x00\x00',  #ApplicationSpecific_1
            b'\x00\x00',  #ApplicationSpecific_2
            headerSize        #PixelArrayOffset
        )


        colorsInPallet = 0
        colorsImportant = 0
        if self._window._bits == 8:
            colorsInPallet = 256
            colorsImportant = 256

        biCompression = 0
        biMasks = bytearray()

        if self._window._bits == 16:
            biCompression = 3
            biMasks += int(0xF800).to_bytes(4,'little') #Red Mask
            biMasks += int(0x7E0).to_bytes(4,'little') #Blue Mask
            biMasks += int(0x1F).to_bytes(4,'little') #Green Mask

        #--DIB HEADER 40 bytes
        dib_header = struct.pack('<IIIHHIIIIII',
            40,                             #DibHeaderBytes
            self._window._columns,          #ImageWidth
            self._window._rows,             #ImageHeight
            0,                              #ColorPlanes
            self._window._bits,             #BitsPerPixel
            biCompression,                  #BiRGB (biCompression)
            headerSize + rawSize,                        #RawBitmapSize
            self._window._columns,          #PrintResolutionH
            self._window._rows,             #PrintResolutionV
            colorsInPallet,                 #NumberOfColorsInPallet
            colorsImportant                 #ImportantColors
        )

        #WRITE TO FILE
        out_file.write(bmp_header)
        out_file.write(dib_header)

        if self._window._bits == 8:
            out_file.write(self._pallet_8bits_color())

        if self._window._bits == 16 and biCompression == 3:
            out_file.write(biMasks)

        out_file.write(self._window._buffer)

        out_file.close

    def _pallet_8bits_color(self):
        paleta = bytearray()
        for i in range(256):
            R = (i>>5) * 36
            G = ((i>>2)& 0x7) * 36
            B = (i&0x3) * 85
            paleta.append(B&0XFF) #RED
            paleta.append(G&0xFF) #GREEN
            paleta.append(R&0xFF) #BLUE
            paleta.append(0) #?
        return paleta
    
    def _pallet_8bits_grey(self):
        paleta = bytearray()
        for i in range(256):
            paleta.append(i) #RED
            paleta.append(i) #GREEN
            paleta.append(i) #BLUE
            paleta.append(0) #?
        return paleta
    





