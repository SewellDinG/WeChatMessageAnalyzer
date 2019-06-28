#!/usr/bin/env python
# -*- encoding: utf-8 -*-

class KeywordProcesser(object):
    """
    中文keyword processer

    Args:
        ignore_space: bool, default is false
        keywords: str, list, dict, if str, then call
            self.add_keyword_from_file

    Attributes:
        keyword_trie_dict (dict): trie tree
        keyword_count (int): trie tree树中关键词数目
    """

    def __init__(self, keywords=None, ignore_space=False):
        self.keyword_trie_dict = dict()
        self.keyword_count = 0
        self._keyword_flag = '_type_'

        self._ignore_space = ignore_space

        if isinstance(keywords, str):
            self.add_keyword_from_file(keywords)
        elif isinstance (keywords, list):
            self.add_keyword_from_list(keywords)
        elif isinstance(keywords, dict):
            self.add_keyword_from_dict(keywords)
        else:
            pass

    def add_keyword(self, keyword, keyword_type=None):
        """
        Add keyword to keyword_trie_dict.

        Args:
            keyword (str): 关键词
            keyword_type (str): 关键词类型

        Examples:
            >>> keyword_processer = KeywordProcesser()
            >>> keyword_processer.add_keyword('苏州')
            >>> keyword_processer.add_keyword('苏州', 'GPE')
        """
        if not keyword_type:
            keyword_type = keyword
        current_dict = self.keyword_trie_dict
        for char in keyword:
            current_dict = current_dict.setdefault(char, {})
        if self._keyword_flag not in current_dict:
            self.keyword_count += 1
            current_dict[self._keyword_flag] = keyword_type

    def add_keyword_from_list(self, keyword_list):
        """
        Add keywords from list.

        Args:
            keyword_list (list): list of keywords

        Examples:
            >>> keyword_processer = KeywordProcesser()
            >>> keyword_processer.add_keyword_from_list(['苏州', '江苏'])
        """
        for keyword in keyword_list:
            self.add_keyword(keyword)

    def add_keyword_from_dict(self, keyword_dict):
        """
        Add keywords from list.

        Args:
            keyword_dict (dict): keywords dict, {keyword: keyword_type}

        Examples:
            >>> keyword_processer = KeywordProcesser()
            >>> keyword_processer.add_keyword_from_dict({'苏州': 'GPE', '小明': 'PER'})
        """
        for keyword in keyword_dict:
            self.add_keyword(keyword, keyword_dict[keyword])

    def add_keyword_from_file(self, path, split='\t'):
        """
        Add keyword from file.

        Args:
            path (str): 关键词存放路径
            split (str): 分隔符，用于分隔关键词和关键词类型

        Examples:
            >>> keyword_processer = KeywordProcesser()
            >>> path = 'path to your keywords'
            >>> keyword_processer.add_keyword_from_file(path, split=',')
        """
        import codecs
        file_r = codecs.open(path, 'r', encoding='utf-8')
        line = file_r.readline()
        while line:
            line = line.strip()
            if not line:
                line = file_r.readline()
                continue
            items = line.split(split)
            if len(items) == 1:
                self.add_keyword(items[0])
            else:
                self.add_keyword(items[0], items[1])
            line = file_r.readline()
        file_r.close()

    def delete_keyword(self, keyword):
        """
        Delete keyword.

        Args:
            keyword (str): 关键词

        Return:
            state (bool): 删除是否成功

        Examples:
            >>> keyword_processer = KeywordProcesser()
            >>> keyword_processer.delete_keyword('your keyword')
        """
        current_dict = self.keyword_trie_dict
        level_node_list = []
        for char in keyword:
            if char not in current_dict:
                return False
            level_node_list.append((char, current_dict))
            current_dict = current_dict[char]

        if self._keyword_flag not in current_dict:
            return False

        level_node_list.append((self._keyword_flag, current_dict))
        for char, level_dict in level_node_list[::-1]:
            if len(level_dict) == 1:
                level_dict.pop(char)
            else:
                level_dict.pop(char)
                break
        self.keyword_count -= 1
        return True

    def delete_keyword_from_list(self, keyword_list):
        """
        Delete keywords from list
        Args:
            keyword_list (list): list of keyword
        """
        for keyword in keyword_list:
            self.delete_keyword(keyword)

    def _match_text(self, text, start, end):
        """
        Args:
            text (str): text
            start (int): 匹配的起始位置
            end (int): 匹配的结束位置

        Returns:
            end, entity_len, entity_type
        """
        current_dict = self.keyword_trie_dict
        index, entity_type = -1, ''

        for i in range(start, end):
            if text[i] == ' ' and self._ignore_space:
                continue
            if text[i] not in current_dict:
                if index == -1:
                    return start+1, 0, ''
                else:
                    return index+1, index+1-start, entity_type
            current_dict = current_dict[text[i]]
            if self._keyword_flag in current_dict:
                index = i
                entity_type = current_dict[self._keyword_flag]
        if index != -1:
            return index+1, index+1-start, entity_type
        return start+1, 0, ''

    def extract_keywords(self, text):
        """
        抽取text中存在的关键词

        Args:
            text (str): text

        Returns:
            keywords (list): list of  keywords and their positions

        Examples:
            >>> keyword_processer = KeywordProcesser()
            >>> keyword_dict = {'苏州': 'GPE', '苏大': 'ORG', '苏州大学': 'ORG'}
            >>> keyword_processer.add_keyword_from_dict(keyword_dict)
            >>> text = '我住在江苏省苏州市苏州大学333号,苏州大的小明'
            >>> keywords = keyword_processer.extract_keywords(text)
            >>> # [[6, 8, 'GPE'], [9, 13, 'ORG'], [18, 20, 'GPE']]
        """
        keywords = []

        end, text_len = 0, len(text)
        while end < text_len:
            end, entity_len, entity_type = self._match_text(text, end, text_len)
            if entity_type:
                keywords.append([end-entity_len, end, entity_type])
        return keywords

    def extract_keywords_from_list(self, words):
        """
        从词序列中抽取关键词

        Args:
            words: list of str, 词序列

        Returns:
            keywords (list): list of keywords and their positions
        """
        keywords = []
        for i, word in enumerate(words):
            if self.contain_keyword(word):
                keywords.append([word, i])
        return keywords

    def extract_keywords_from_list_yield(self, words):
        """
        从词序列中抽取关键词

        Args:
            words: list of str, 词序列

        yield:
            [word, i]: keyword and its positions
        """
        for i, word in enumerate(words):
            if self.contain_keyword(word):
                yield [word, i]

    def extract_keywords_yield(self, text):
        """
        抽取text中存在的关键词

        Args:
            text (str): text
        """
        end, text_len = 0, len(text)
        while end < text_len:
            end, entity_len, entity_type = self._match_text(text, end, text_len)
            if entity_type:
                yield([end-entity_len, end, entity_type])

    def get_keyword_type(self, keyword):
        """
        获取keyword所对应的类型;若不存在，则返回None

        Args:
            keyword (str): keyword

        Returns:
            keyword_type (str): keyword type；若不存在，则返回None

        Examples:
            >>> keyword_processer = KeywordProcesser()
            >>> keyword_dict = {'苏州': 'GPE', '北京': 'GPE'}
            >>> keyword_processer.add_keyword_from_dict(keyword_dict)
            >>> keyword_processer.get_keyword_type('北京')
            >>> # 'GPE'
        """
        current_dict = self.keyword_trie_dict
        for char in keyword:
            if char not in current_dict:
                return None
            current_dict = current_dict[char]
        if self._keyword_flag not in current_dict:
            return None
        return current_dict[self._keyword_flag]

    def contain_keyword(self, keyword):
        """
        判断keyword是否存在于trie tree中

        Args:
            keyword (str): keyword

        Returns:
            bool

        Examples:
            >>> keyword_processer = KeywordProcesser()
            >>> keyword_dict = {'苏州': 'GPE', '北京': 'GPE'}
            >>> keyword_processer.add_keyword_from_dict(keyword_dict)
            >>> keyword_processer.contain_keyword('北京')
            >>> # True
            >>> keyword_processer.contain_keyword('北京大学')
            >>> # False
        """
        current_dict = self.keyword_trie_dict
        for char in keyword:
            if char not in current_dict:
                return False
            current_dict = current_dict[char]
        if self._keyword_flag not in current_dict:
            return False
        return True

    def get_keywords(self, keyword_part='', current_dict=None):
        """
        获取所有的keywords

        Returns:
            keywords: list
        """
        keywords = dict()
        if current_dict is None:
            current_dict = self.keyword_trie_dict
        for char in current_dict:
            if char == self._keyword_flag:
                keywords[keyword_part] = current_dict[self._keyword_flag]
            else:
                keywords_ = self.get_keywords(keyword_part+char, current_dict[char])
                keywords.update(keywords_)
        return keywords

    def remove_keywords_in_words(self, words):
        """
        从单词序列中删除关键词

        Args:
            words: list of word, 词序列

        Returns:
            words: list of word, 删除关键词之后的词序列
        """
        words_ = []
        for word in words:
            if self.contain_keyword(word):
                continue
            words_.append(word)
        return words_

    def remove_keywords_in_text(self, text, token_wise=False):
        """
        从句子中删除关键词

        Args:
            text (str): 从句子中删除关键词
            token_wise (bool): 是否以token为单位进行匹配，若是，
                则将句子以空格切成若干token，然后以token为单位进行匹配；
                否则，以字符为单位进行匹配。

        Returns:
            text (str): 删除关键词之后的句子
        """
        if token_wise:  # 以token为单位
            return ' '.join(remove_keyword_in_words(sentence.split(' ')))
        # 以字符为单位
        text_ = ''
        start, end, text_len = 0, 0, len(text)
        while end < text_len:
            end, entity_len, entity_type = self._match_text(text, end, text_len)
            if not entity_type:
                text_ += text[start:end]
            start = end
        return text_

    def set_ignore_space(self, ignore_space):
        """
        Args:
            ignore_space: bool
        """
        self._ignore_space = ignore_space


def kw_match_dic():
    result = {}
    with open('taboo.txt', 'r') as taboo:
        for line in taboo:
            line = line.strip()
            if line:
                result[line.split(':')[0].strip()] = line.split(':')[1].strip()
                # print(result)
    return result


def demo(msg):
    keyword_dict = kw_match_dic()
    # keyword_dict = {'毒品': 'GPE', '数据': 'ORG', '黑产': 'GPE', '盗窃': 'ORG'}
    keyword_processer = KeywordProcesser()
    keyword_processer.add_keyword_from_dict(keyword_dict)
    print('keyword_count: ' + str(keyword_processer.keyword_count))
    # print('all_keywords:')
    # print(keyword_processer.get_keywords())
    text = msg
    for kw_match in keyword_processer.extract_keywords_yield(text):
        print('keyword_position: ' + str(kw_match))
        return kw_match


def demo2():
    keyword_dict = {'a-b': 'a-b'}
    keyword_processer = KeywordProcesser(True)
    keyword_processer.add_keyword_from_dict(keyword_dict)
    print(keyword_processer.keyword_count)
    text = 'xxxa -  bxxx'
    for item in keyword_processer.extract_keywords_yield(text):
        print(item)


def demo3():
    keyword_dict = {'江苏省': 'GPE', '苏大': 'ORG', '北京': 'GPE', '苏州大学': 'ORG',
                    '苏有朋': 'PER', '苏有月': 'PER'}
    keyword_processer = KeywordProcesser()
    keyword_processer.add_keyword_from_dict(keyword_dict)
    print(keyword_processer.keyword_count)
    words = ['江苏省', '苏州市', '沧浪区', '干将东路', '333号', '苏州大学', '本部', '。']
    keywords = keyword_processer.extract_keywords_from_list(words)
    print(keywords)


def demo_delete_stopwords():
    """
    测试删除通用词
    """
    stopwords = ['、', '，', '。', '的', '对', '和', '这个', '一切']
    sentence = '这个时间落伍的计时机无意中对人生包涵的讽刺和感伤，深于一切语言、一切啼笑。'
    print(sentence)
    keyword_processer = KeywordProcesser(stopwords)
    sentence = keyword_processer.remove_keywords_in_text(sentence)
    print(sentence)

    keyword_processer = KeywordProcesser(stopwords)
    words = ['这个', '时间', '落伍', '的', '计时机', '无意', '中', '对', '人生', '包涵',
             '的', '讽刺', '和', '感伤', '，', '深于', '一切', '语言', '、', '一切', '啼笑', '。']
    print(words)
    words = keyword_processer.remove_keywords_in_words(words)
    print(''.join(words))


# if __name__ == '__main__':
#     demo()