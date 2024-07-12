from typing import NoReturn
from binascii import crc32

SEEK_START = 0
SEEK_CUR = 1
SEEK_END = 2

class PNG_img:

    def __get_chunk(self):
        leng = int.from_bytes(self.img.read(4), "big")

        try:
            type = self.img.read(4).decode()
        except:
            type = 'CHUNK'

        off_data = self.img.tell()
        self.img.seek(leng, SEEK_CUR)
        crc = self.img.read(4)

        if type == '':
            return None

        return [type, (off_data, leng, crc)]

    def __get_info(self) ->  None:
        self.file_width = 0
        self.file_height = 0

        IHDR = self.chunks["IHDR-0"]
        off_data = IHDR[0]
        leng = IHDR[1]

        self.img.seek(off_data, SEEK_START)
        data = self.img.read(leng)

        self.file_width = int.from_bytes(data[:4], byteorder='big')
        self.file_height = int.from_bytes(data[4:8], byteorder='big')

    def info(self) -> dict:
        res = dict()

        res["name"] = self.file_name
        res["height"] = self.file_height
        res["widht"] = self.file_width

        return res

    def resize(self, width: int, height: int) -> None:
        IHDR = self.chunks["IHDR-0"]
        off_data = IHDR[0]
        leng = IHDR[1]

        self.img.seek(off_data, SEEK_START)
        data = self.img.read(leng)

        width_b = width.to_bytes(4, 'big') 
        height_b = height.to_bytes(4, 'big') 
        data = width_b + height_b + data[8:] 
        
        crc = crc32(b'IHDR' + data).to_bytes(4, 'big')

        self.img.seek(off_data, 0)
        self.img.write(data)
        self.img.write(crc)

        self.file_height = height
        self.file_width = width

    def rresize(self, rwidth: int, rheight: int) -> None:
        IHDR = self.chunks["IHDR-0"]
        off_data = IHDR[0]
        leng = IHDR[1]

        self.img.seek(off_data, SEEK_START)
        data = self.img.read(leng)

        width = self.file_width + rwidth
        height = self.file_height + rheight

        width_b = width.to_bytes(4, 'big') 
        height_b = height.to_bytes(4, 'big')
        data = width_b + height_b + data[8:]
        
        crc = crc32(b'IHDR' + data).to_bytes(4, 'big')

        self.img.seek(off_data, 0)
        self.img.write(data)
        self.img.write(crc)
    
        self.file_height += rheight
        self.file_width += rwidth

    def __init__(self, path):
        self.img = open(path, "r+b")
        self.magic = self.img.read(8)
        self.file_name = path
        self.chunks = dict()
        
        number_chunks = dict()
        # number_chunks["IDAT"] = 0
        # number_chunks["CHUNK"] = 0

        c = self.__get_chunk()
        while c != None:
            if c[0] in number_chunks:
                c[0] += '-' + str(number_chunks[c[0]])
                number_chunks[c[0]] += 1
            else:
                number_chunks[c[0]] = 0
                c[0] += '-' + str(number_chunks[c[0]])

            self.chunks[c[0]] = c[1]
            
            c = self.__get_chunk()
        
        self.__get_info()
            
                

