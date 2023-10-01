
# Lista a tabela ASCII
def charmap():
    chars = list()
    for char in range(128):
        chars.append(chr(char))
    return chars

# Cria a tabela de indexacao da string fazendo o deslocamento na tabela ASCII
def classifier(char_map:str, key=3):
    # ECNA -> Exception in Classifier with non-alpha character
    # ECTA -> Exception in Classifier with true alpha character
    dict_map = dict()
    chars = charmap()
    
    for i, char in enumerate(char_map):
        
        if char.isalnum():
            try:
                dict_map[f'{i}-char'] = chars.index(char) + key
            except ValueError:
                # print(f"debug_ECTA: {char}")
                dict_map[f'{i}-{char}'] = char
        elif char.isspace():
            dict_map[f'{i}-{char}'] = char
            
    return list(dict_map.values())

def knife(char_map, size=4):
    temp_list = list()
    indexer = 0
    counter = 0
    
    for i in range(size):
        temp_list.append(str())
    
    for char in char_map:
        if counter <= len(char_map)/size:
            temp_list[indexer] += char
            counter += 1
        else:
            indexer += 1
            counter = 0
            temp_list[indexer] += char
            
    return temp_list
    

# Trunca a string e faz o deslocamento (caso ativado o deslocamento)
def truncate(char_map:str, value):
    ascii_map = charmap()
    temp_string = ""
    
    for char in char_map:
        if char_map.index(char) >= int(len(char_map)/2):
            try:
                if char.isalnum():
                    temp_string += ascii_map[ascii_map.index(char)-value]
                else:
                    temp_string += char
                    
            except ValueError:
                # print(f"debug_ETNA: {char}")
                temp_string += char
        else:
            temp_string += char
            
    return temp_string

# Converte uma tabela de indexacao em string
def umpack(sequence:str, invert=False):
    temp_str = ""
    for i in sequence:
        if isinstance(i, str):
            try:
                temp_str += chr(int(i))
            except ValueError:
                temp_str += i
        elif isinstance(i, int):
            temp_str += chr(i)
        else:
            temp_str += i
            
    if invert:
        return temp_str[::-1]
    else:
        return temp_str

_keymap_lenght = 1 # Max: 3
_keymap_decode = 1 # 1 ou 0 (0 para desligar o deslocamento truncado)



if __name__ == "__main__":
    message = """A noite, 4 gatos e 3 cães passeavam na 6ª Avenida. A1 lua estava brilhante, e 5 estrelas no céu iluminavam a rua. Eles caminhavam lentamente, 1 dos gatos se 4talecia 7tre os outros, como se fosse o líder do grupo.
De repente, ouviram 2 barulhos altos, eram 8 tiros vindo de uma rua lateral. Os animais entraram em pânico e correram em direções diferentes. 1 dos gatos subiu em cima de 9 latas de lixo, enquanto os 3 cães se esconderam 4 trás de um muro.
A cena era digna de um filme de ação. 6 dos tiros atingiram a parede, fazendo 3 buracos nela. Os animais observavam assustados, e o líder dos gatos, que agora estava em cima de 2 caixas, olhava para os outros com um olhar de preocupação.
Depois de alguns minutos de suspense, os tiros cessaram. Os animais, ainda tremendo, se reuniram e seguiram em frente. Foi uma noite 5quecível, e eles nunca mais se aventuraram na 6ª Avenida à noite."""
    cripto_msg = ""
    decode_msg = ""
    # criptografando
    for seq in knife(message):
        code0 = classifier(seq, _keymap_lenght)
        code1 = umpack(code0, True)
        code2 = truncate(code1, _keymap_decode)
        cripto_msg += code2
    print(f"Criptografada: {cripto_msg}\n")
    
    for seq in knife(cripto_msg):
        # descriptografando
        decode2 = truncate(seq, -_keymap_decode)
        decode1 = classifier(decode2, -_keymap_lenght)
        decode0 = umpack(decode1, True)
        decode_msg += decode0
        
    print(f"descriptografada: {decode_msg}\n")