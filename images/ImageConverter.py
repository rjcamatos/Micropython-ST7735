import struct

'''
CONVERT A 24bits Little Endian BITMAP TO 16bits Big Endian Bitmap
'''

IN_FILE = './images/picture24bits.bmp'
OUT_FILE = './images/picture16bits.bmp'


# ---------------------------//--------------------------------

def pack_color(R,G,B):
    return int( (R&0xF8)<<8 | (G&0xFC)<<3 | (B&0xF8)>>3 ).to_bytes(2,'big')

def conv(in_file,out_file):
    print("START CONVERSION FROM",in_file,"TO",out_file)

    
    in_file = open(in_file,'rb')
    in_file.seek(54)    
    out_data = bytearray()
    while True:
        in_data = in_file.read(3)
        if len(in_data) == 0: break
        out_data += pack_color(in_data[2],in_data[1],in_data[0])

    in_file.seek(0)
    bmp_header = struct.unpack_from('<2sI2s2sI',in_file.read(14))
    bmp_header = struct.pack('<2sI2s2sI',
        bmp_header[0],  #BmDescription
        len(out_data)+66,  #FileSize #THE SISZE OF THE HEADER
        bmp_header[2],  #ApplicationSpecific_1
        bmp_header[3],  #ApplicationSpecific_2
        66   #PixelArrayOffset
    )

    dib_header = struct.unpack_from('<IIIHHIIIIII',in_file.read(40))
    dib_header = struct.pack('<IIIHHIIIIII',
        dib_header[0],  #DibHeaderBytes
        dib_header[1],  #ImageWidth
        dib_header[2],  #ImageHeight
        dib_header[3],  #ColorPlanes
        16,             #BitsPerPixel
        3,  #BiRGB
        len(out_data)+66,  #RawBitmapSize
        dib_header[7],  #PrintResolutionH
        dib_header[8],  #PrintResolutionV
        dib_header[9],  #NumberOfColorsInPallet
        dib_header[10]  #ImportantColors
    )
    in_file.close()

    biMasks = bytearray() #--> NEED TO SEE HOW TO SET THIS MASK TO BIG USE ENDIAN
    biMasks += int(63488).to_bytes(4,'little') #Red Mask
    biMasks += int(2016).to_bytes(4,'little') #Blue Mask
    biMasks += int(31).to_bytes(4,'little') #Green Mask

    out_file = open(out_file,'wb')
    out_file.write(bytes(bmp_header))
    out_file.write(dib_header)
    out_file.write(biMasks)
    out_file.write(out_data)

    
    in_file.close()
    print('CONVERTION DONE !!!')

def print_header(in_file):
    print("FILE",in_file,"HEADERS")
    in_file = open(in_file,'rb')

    bmp_header = struct.unpack_from('<2sI2s2sI',in_file.read(14))
    dib_header = struct.unpack_from('<IIIHHIIIIII',in_file.read(40))
    bi_colors = struct.unpack_from('<III',in_file.read(12))

    in_file.close()

    print("BMP HEADER",bmp_header)
    print("DIB HEADER",dib_header)
    print("BI COLORS",bi_colors)

conv(IN_FILE,OUT_FILE)

#print_header('./images/OK_FILE.bmp')
#print_header('./images/picture16bits.bmp')


