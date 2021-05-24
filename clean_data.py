import re

word_pattern = re.compile('[A-Za-z]{2,}')
sentence_pattern = re.compile('[A-Za-z，\.。,:?！!\'\s]{2,}')
max_word_pattern = re.compile('[A-Za-z\d\-_\']{40,}')
url_pattern = re.compile('(http|ftp|https)(：|:)\/\/([\w\-_]+(\.[\w\-_]+)+|localhost)([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?') # ****
www_pattern = re.compile('www\.[A-Za-z]+')
upper_char = re.compile('[A-Z]{1}')
downer_char = re.compile('[a-z]{1,}')
book_pattern = re.compile("《[\w\s']+》")
reference_pattern = re.compile('\.\[\d+\]')
js_code_pattern = re.compile('{.*}')
cs_code_pattern = re.compile('margin-bottom:.*px;')
reference_year_pattern = re.compile('\（\d{4}\）.')
downline_pattern = re.compile('_{2,}')


def judge_enlgish_setence(line, en_single_handler, ch_single_handler):
    if downline_pattern.search(line) is not None: # 过滤下划线
        return 
    if cs_code_pattern.search(line) is not None: # 过滤 css 代码
        return
    if js_code_pattern.search(line) is not None: # 过滤 js 代码
        return
    if url_pattern.search(line) is not None:  # 删除含有网址的
        return
    if www_pattern.search(line) is not None: # 删除含有网址的
        return 
    for rule in del_rule:
        if rule in line:
            return
    
    cnt = 0
    for ch in line:
        if u'\u4e00' <= ch <= u'\u9fff': 
            cnt += 1
            
    if cnt == 0 and reference_pattern.search(line) is not None: # 过滤引用 . [12]
        return
    if cnt == 0 and reference_year_pattern.search(line) is not None: # 过滤引用 (1991).
        return
    
    try:
        setence_len = line.strip().split('\t')[-1]
        if setence_len == '一一':
            return
        if not  setence_len.isnumeric() or eval(setence_len) <= 5: # ********************
            return
        
        sentences = sentence_pattern.findall(line)
        english_word_num = 0
        for sentence in sentences:
            words = re.split('[,，\s]', sentence.strip())
            words_len = len(words)
            english_word_num += words_len
            
        if cnt == 0 and english_word_num > 1 and  downer_char.search(line) is not None:
            en_single_handler.write(line)
            return
        
        if cnt > 0 and english_word_num <= 3 or float(english_word_num) / float(cnt) < 0.1:
            ch_single_handler.write(line)
            return 
    except: 
        print(line)
    else:
        return 
    
def read_del_rule_from_file(file):
    del_rule = []
    with open(file, 'r', encoding='utf-8',errors='ignore') as f:
        done = False
        while not done:
            line = f.readline()
            if line == "":
                done = True
            else:
                del_rule.append(line.strip())
    return del_rule

if __name__ == '__main__':
    en_single_handler = open("english_single.txt", 'w', errors='ignore', encoding='utf-8',)
    ch_single_handler = open("chinese_single.txt", 'w', errors='ignore', encoding='utf-8',)
    file_path = '/mnt/yardcephfs/mmyard/g_wxg_td_prc/poetniu/0.data/mp_text'
    with open(file_path, 'r', encoding='utf-8',errors='ignore') as f:
        done = False
        while not done:
            line = f.readline()
            if line == "":
                done = True
            else:
                judge_enlgish_setence(line, en_single_handler, ch_single_handler)