#定義split函式，參數s、delimiter型別皆為str，此函式retrn 的型別為list
def split(s:str,delimiter:str) -> list: 
    s += delimiter # tricky
    start_pos = 0
    lst = []

    for i, ch in enumerate(s):  # enumerate() 對一個list遍歷索引和值
        if ch == delimiter:
            lst.append(s[start_pos:i])
            start_pos = i+1 
    return lst

# hex_to_bin函式，參數hex型別為str，此函式retrn 的型別為int
def hex_to_bin(hex:str) -> int:
    hex = hex.upper() ## 小寫轉大寫
    ms_nibble = hex[0]
    ls_nibble = hex[1]
    

    def nibble_to_bin(ch:str) -> int:  #nibble半位元
        code = ord(ch)
        ret2 = (code - 0x30) if code < 0x41 else (code - 55)
        return ret2

    ret = nibble_to_bin(ms_nibble)*16 + nibble_to_bin(ls_nibble)
    return ret
 


def query_to_utf8(s:str, codec='utf8') -> str:
    i = 0
    length = len(s)
    bya = bytearray()
    while i < length:
        if s[i] == r'%':
            bya.append(hex_to_bin(s[i+1:i+3]))
            i += 3
        else:
            bya.append(ord(s[i]))
            i += 1
    return bya.decode(codec)


def query_components(s:str, codec='utf8') -> str:
    decode_str =  query_to_utf8(s,codec)
    pair_val_list = split(decode_str,'&')
    dic = {}
    for it in pair_val_list:
        key_val = split(it,'=')
        dic.update({key_val[0]:key_val[1]})
    return dic
    
print(query_components(r'name%3D%E8%95%AD%E6%B2%96%26age%3D48%26%E7%95%99%E8%A8%80%3D%E5%A4%AA%E6%9C%89%E8%B6%A3%E4%BA%86'))
print(query_components(r'name%3D%BF%BD%A8R%26age%3D30%26%AFd%A8%A5%3D%A4%A4%A4%E5','big5'))

        
