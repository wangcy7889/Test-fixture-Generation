from googletrans import Translator
global des_file
translator = Translator(service_urls=['translate.google.cn'])

def tran_sub(line):
    global des_file
    global count
    global translator
    count += 1
    print('count,%d' % count)
    line = line.decode('utf-8')
    if line.startswith('Dialogue') and 'student speaking' not in line:
        des_file.write(line.encode('utf-8'))
        head_str, english_str = tuple(line.rsplit(',,', 1))
        chinese_str = translator.translate(english_str, dest='zh-CN').text
        print(chinese_str)
        c_line = ',,'.join([head_str, chinese_str + '\n']).replace('English', 'Chinese').replace('您', '你').encode('utf-8')
        des_file.write(c_line)
    else:
        des_file.write(line.encode('utf-8'))