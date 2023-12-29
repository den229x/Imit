from typing import NoReturn
from binascii import crc32

class PNG_img:

    def __get_chunk(self):
        leng = int.from_bytes(self.img.read(4), "big")
        type = self.img.read(4).decode()
        off_data = self.img.tell()
        self.img.seek(leng, 1)
        crc = self.img.read(4)

        if type == '':
            return None

        return [type, (off_data, leng, crc)]
    

    def resize(self, width: int, height: int) -> NoReturn: #type: ignore
        IHDR = self.chunks["IHDR"]
        off_data = IHDR[0]
        leng = IHDR[1]

        self.img.seek(off_data, 0)
        data = self.img.read(leng)

        width = width.to_bytes(4, 'big') #type: ignore
        height = height.to_bytes(4, 'big') #type: ignore
        data = width + height + data[8:] #type: ignore
        
        crc = crc32(b'IHDR' + data).to_bytes(4, 'big')

        self.img.seek(off_data, 0)
        self.img.write(data)
        self.img.write(crc)

    

    def __init__(self, path):
        self.img = open(path, "r+b")
        self.magic = self.img.read(8)
        self.chunks = dict()

        number_IDAT = 0
        c = self.__get_chunk()
        while c != None:
            if c[0] in "IDAT":
                c[0] += str(number_IDAT)
                number_IDAT += 1

            self.chunks[c[0]] = c[1]
            
            c = self.__get_chunk()
            
                

