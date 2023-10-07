

class Criptofy:
    CHARMAP = [x for i in range(128) for x in chr(i)]
    
    def __init__(self, public_key, private_key, reverse=False) -> None:
        self.public_key = public_key
        self.__private_key__ = private_key
        self.reverse = reverse
        
        self.n = self.public_key * self.__private_key__
        self.fii = (self.public_key - 1) * (self.__private_key__ - 1)
        self.swift_key = self.catch_mdc(self.n, self.fii)

    def map_char(self, source:str) -> list:
        
        char_map_list = list()
        
        for char in source:
            if char.isascii():
                if self.CHARMAP.index(char)+self.swift_key> 1 < 127:
                    if self.reverse:
                        char_map_list.append(self.CHARMAP.index(char)-self.swift_key)
                    else:
                        char_map_list.append(self.CHARMAP.index(char)+self.swift_key)
                else:
                    if self.reverse:
                        char_map_list.append(self.CHARMAP.index(char)+self.swift_key-128)
                    else:
                        char_map_list.append(self.CHARMAP.index(char)+self.swift_key+128)
        
        return char_map_list
    
    def catch_mdc(self, y, x):
        last_number = int()
        while y:
            x, y = y, x%y
            
            if y > 1:
                last_number = y
        
        return last_number

message = "1Uma mensagem a ser enviada c0m 10 espacos e 48 CARACTERES"

cript = Criptofy(1277, 177).map_char(message)
tmp_str = ""
for char in cript:
    tmp_str+=chr(char)
print(tmp_str)
cript2 = Criptofy(1277, 177, True).map_char(tmp_str)
tmp_str2 = ""
for char in cript2:
    tmp_str2+=chr(char)
print(tmp_str2)