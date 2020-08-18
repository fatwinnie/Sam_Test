#定義split函式，參數s、delimiter型別皆為str，此函式retrn 的型別為list
def split(s:str,delimiter:str) -> list: 
    s += delimiter # tricky 偷偷先多加一個分號，為了在for裡面取最後的片段
    start_pos = 0
    lst = []

    for i, ch in enumerate(s):  # enumerate() 對一個list遍歷索引和值
        if ch == delimiter:
            lst.append(s[start_pos:i]) # slicing切片 start_pos到i
            start_pos = i+1 
    return lst

# hex_to_bin函式，參數hex型別為str，此函式retrn 的型別為int
def hex_to_bin(hex:str) -> int:
    hex = hex.upper() ## 小寫轉大寫
    ms_nibble = hex[0] # ms_nibble最大位數
    ls_nibble = hex[1] # ls_nibble 最小位數
    
# nibble_to_bin函示，參數ch 型別為str，retrun的型別為int
# nibble_to_bin 是4-bit to 2-bit嗎? 
    def nibble_to_bin(ch:str) -> int:  #nibble半位元(4-bit)
        code = ord(ch) #ord()參數返回對應的ASCII
        ret2 = (code - 0x30) if code < 0x41 else (code - 55) # 0x30=0 , 0x41=A ,code-55?       
        return ret2

    ret = nibble_to_bin(ms_nibble)*16 + nibble_to_bin(ls_nibble) #不懂
    return ret   
 

# query_to_utf8 函式，參數s型別為str，解碼為utf8，返回型別為str。此函式目的為解譯
def query_to_utf8(s:str, codec='utf8') -> str: 
    i = 0
    length = len(s) # s字串的長度
    bya = bytearray() # return新的位元組陣列,元素必須為0~255的整數
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
#{'name': '蕭沖', 'age': '48', '留言': '太有趣了'} // utf-8 為3-byte
#{'name': '蕭沖', 'age': '30', '留言': '中文'} // big5 為2-byte
        
