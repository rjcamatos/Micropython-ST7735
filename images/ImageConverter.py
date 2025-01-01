import struct

'''
CONVERT A 24bits Little Endian BITMAP TO 16bits Big Endian Bitmap
'''

IN_FILE = './images/picture24bits.bmp'
OUT_FILE = './images/picture16bits.bmp'


# ---------------------------//--------------------------------

def pack_color(R,G,B):
    return int( (R&0xF8)<<8 | (G&0xFC)<<3 | (B&0xF1)>>3 ).to_bytes(2,'big')

def conv(in_file,out_file):
    out_file = open(out_file,'wb')
    in_file = open(in_file,'rb')

    bmp_header = struct.unpack_from('<2sI2s2sI',in_file.read(14))
    bmp_header = struct.pack('<2sI2s2sI',
        bmp_header[0],  #BmDescription
        bmp_header[1],  #FileSize #THE SISZE OF THE HEADER
        bmp_header[2],  #ApplicationSpecific_1
        bmp_header[3],  #ApplicationSpecific_2
        bmp_header[4]   #PixelArrayOffset
    )

    dib_header = struct.unpack_from('<IIIHHIIIIII',in_file.read(40))
    dib_header = struct.pack('<IIIHHIIIIII',
        dib_header[0],  #DibHeaderBytes
        dib_header[1],  #ImageWidth
        dib_header[2],  #ImageHeight
        dib_header[3],  #ColorPlanes
        16,             #BitsPerPixel
        dib_header[5],  #BiRGB
        dib_header[6],  #RawBitmapSize
        dib_header[7],  #PrintResolutionH
        dib_header[8],  #PrintResolutionV
        dib_header[9],  #NumberOfColorsInPallet
        dib_header[10]  #ImportantColors
    )
    
    out_file.write(bytes(bmp_header))
    out_file.write(dib_header)
    
    while True:
        in_data = in_file.read(3)
        if len(in_data) == 0: break
        out_data = pack_color(in_data[2],in_data[1],in_data[0])
        out_file.write(out_data)

    out_file.close()
    in_file.close()

conv(IN_FILE,OUT_FILE)
print('CONVERTION DONE !!!')