
# Lista a tabela ASCII
def charmap() -> list:
    """Cria uma lista contendo todos os caracteres ASCII.

    Returns:
        list: lista com todos os caracteres ASCII.
    """
    chars = list()
    for char in range(128):
        chars.append(chr(char))
    return chars

# Cria a tabela de indexacao da string fazendo o deslocamento na tabela ASCII
def classifier(char_map:str, key=3, encript=True) -> list:
    """ Gera um dicionário onde as chaves são os índices dos caracteres na string original 
    e os valores são os índices dos caracteres na tabela ASCII após o 
    deslocamento (ou inversamente, dependendo da operação).

    Args:
        char_map (str): string a ser processada
        key (int, optional): valor de deslocamento. Defaults to 3. valores mais baixos podem causar perda de dados!
        encript (bool, optional): tipo de operacao: encriptar | reverter. Defaults to True.

    Returns:
        list: retorna uma lista de enderecos ASCII de caracteres
    """
    
    dict_map = dict()
    chars = charmap()
    # percorrendo e enumerando a sequencia de caracteres
    for i, char in enumerate(char_map):
        if char.isascii() : # filtro de caracteres (removendo caracteres nao ASCII)
            try:
                if encript: # caso a configuracao seja encript, executa o deslocamento
                    dict_map[f'{i}-char'] = chars.index(char) + key
                    
                else: # do contrario, executa o deslocamento inverso
                    dict_map[f'{i}-char'] = chars.index(char) - key
                    
            except ValueError: # em caso de erro de valor o caractere sera adicionado intacto.
                print(f"debug_ECTA: {char}")
                dict_map[f'{i}-{char}'] = char  
               
    return list(dict_map.values())

def knife(char_map:str, size:int=4) -> list:
    """Divide a string em partes de tamanho definido em _size_.

    Args:
        char_map (str): string a ser processada
        size (int, optional): quantidade de partes a ser dividida. Defaults to 4.

    Returns:
        list: retorna uma lista com as partes.
    """
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
def truncate(char_map:str, value:int, encript=True):
    """Processador de string | Truncar e reverter trunc

    Args:
        char_map (str): string a ser processada.
        value (int): tamanho do deslocamneto, max: 2 (valores mais altos resultam em perda de dados.)
        encript (bool, optional): tipo de processo, encriptar ou desencriptar. Defaults to True.

    Returns:
        str: retorna uma string truncada de acordo com os valores configurados.
    """
    ascii_map = charmap()
    temp_string = ""
    
    # fatiar a string passada em duas partes
    striped: str = knife(char_map, size=2)
    
    for char in striped[1]: # a segunda metade da string sera truncada
        try:
            if char.isascii():
                if encript:
                    temp_string += ascii_map[ascii_map.index(char)-value]
                else:
                    temp_string += ascii_map[ascii_map.index(char)+value]
            else:
                temp_string += char
                
        except IndexError:
            print(f"debug_ETNA: {char}")
            temp_string += char
            
    return striped[0] + temp_string
    

# Converte uma tabela de indexacao em string
def umpack(sequence:str, invert=False):
    """Converte uma sequência de índices de caracteres na string original.

    Args:
        sequence (str): string a ser processada.
        invert (bool, optional): inverter string. Defaults to False.

    Returns:
        str: retorna uma string processada de acordo com os parametros definidos.
    """
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

_keymap_lenght = 3 # Max: 3 "Um valor alto pode causar perda de caracteres"
_keymap_decode = 1 # 1 ou 0 (0 para desligar o deslocamento truncado)

def encript(message: str):
    temp_msg = str()
    # criptografando
    for seq in knife(message, 4):
        code0 = classifier(seq, _keymap_lenght, True)
        code1 = umpack(code0, True)
        code2 = truncate(code1, _keymap_decode, True)
        temp_msg += code2
    return temp_msg


def decript(message: str):
    temp_msg = str()
    for seq in knife(message, 4):
        # descriptografando
        decode2 = truncate(seq, _keymap_decode, False)
        decode1 = classifier(decode2, _keymap_lenght, False)
        print(f"debug code1: {decode1}")
        decode0 = umpack(decode1, True)
        temp_msg += decode0
    return temp_msg


if __name__ == "__main__":
    message_1 = "1Uma mensagem A ser enviada quando 4forçada | Trunca a string e faz o deslocamento (caso ativado o deslocamento)"
    msg_encript = encript(message_1)
    
    print(f"Encriptada: {msg_encript}")
    print(f"Decriptada: {decript(msg_encript)}")
    