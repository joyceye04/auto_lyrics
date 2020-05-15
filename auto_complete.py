import jieba
import collections, pickle
import random


def ch_split(sentence):
    return list(jieba.cut(sentence, cut_all=False))


def get_chunks(tokens, chunk_size):
    chunk_size = min(chunk_size, len(tokens))
    for chunk in range(2, chunk_size+1):
        for i in range(0, len(tokens) - chunk + 1):
            yield tokens[i:i+chunk]


class AutoCompleteModel:
    
    def __init__(self, chunk_size):
        self.single_words_pool = dict()
        self.tuple_words_pool = dict()
        self.start_words_pool = set()
        self.chunk_size = chunk_size
        
    def build_model(self, data, incremental=False):
        words_list = []
        sentence_list = []

        if not incremental:
            self.start_words_pool = set()

        for sentence in data.split("\n"):
            x = ch_split(sentence)
            if x:
                self.start_words_pool.add(x[0])
            words_list += x
            sentence_list.append(x)

        if incremental:
            clc = collections.Counter(words_list)
            for k in clc:
                self.single_words_pool[k] = self.single_words_pool.get(k, 0) + clc[k]
        else:
            self.single_words_pool.update(collections.Counter(words_list))

        word_tuples = []
        for sentence in sentence_list:
            word_tuples += get_chunks(sentence, self.chunk_size)

        if incremental:
            for items in word_tuples:
                if items[0] not in self.tuple_words_pool:
                    self.tuple_words_pool[items[0]] = collections.Counter()
                    for offset in range(2, self.chunk_size+1):
                        self.tuple_words_pool[items[0]].update(["".join(items[1:offset])])
                else:
                    for offset in range(2, self.chunk_size+1):
                        key2 = " ".join(items[1:offset])
                        self.tuple_words_pool[items[0]][key2] = self.tuple_words_pool[items[0]].get(key2, 0) + 1
        else:
            self.tuple_words_pool.update({items[0]: collections.Counter() for items in word_tuples})

            for items in word_tuples:
                try:
                    for offset in range(2, self.chunk_size+1):
                        self.tuple_words_pool[items[0]].update([" ".join(items[1:offset])])
                except Exception as err:
                    print("error in building tuple words pool: ", err)

    def compress_model(self, compress_limit):
        print("compressing data")
        selected = []
        for key, sub in self.tuple_words_pool.items():
            for k2 in sub:
                if sub[k2] < compress_limit:
                    selected.append((key, k2))
        for k1, to_rm in selected:
            del self.tuple_words_pool[k1][to_rm]

        selected = []
        for key in self.single_words_pool:
            if self.single_words_pool[key] < compress_limit:
                selected.append(key)

        for to_rm in selected:
            self.single_words_pool.pop(to_rm)
    
    def save_model(self, model_path="model.pkl"):

        pickle.dump({'start_words_pool': self.start_words_pool,
                     'single_words_pool': self.single_words_pool,
                     'tuple_words_pool': self.tuple_words_pool},
                        open(model_path, 'wb'), protocol=2)

        print("successfully saved model to:", model_path)
    
    def load_model(self, model_path):
        
        models = pickle.load(open(model_path, 'rb'))
        self.single_words_pool = models['single_words_pool']
        self.tuple_words_pool = models['tuple_words_pool']
        self.start_words_pool = models["start_words_pool"]
        print("successfully loaded model from: {}".format(model_path))
    
    def get_single_words_pool(self):
        return self.single_words_pool

    def get_tuple_words_pool(self):
        return self.tuple_words_pool

    def generate_random_word(self):
        return random.sample(self.single_words_pool.keys(), 1)[0]

    def generate_start_word(self):
        return random.sample(self.start_words_pool, 1)[0]

    def generate_next_word(self, prev_word):
        """ generate next word by given one prev_word"""
        if prev_word in self.tuple_words_pool:
            # print("from pool")
            next_word = random.sample(self.tuple_words_pool[prev_word].keys(), 1)[0]
        else:
            # print("random next")
            next_word = self.generate_random_word()[0]
        return next_word

    def generate_one_sentence(self, limit_word_size):
        """ generate one sentence given by limit_word_size of words"""
        start = self.generate_start_word()
        result = [start]
        self._dfs(start, 0, result, limit_size=limit_word_size)
        return "".join(result)

    def generate_sentences(self, num_of_sentence, limit_word_size):
        """ generate N(num_of_sentence) sentences """
        res = []
        for _ in range(num_of_sentence):
            res.append(self.generate_one_sentence(limit_word_size))
        return "\n".join(res)

    def _dfs(self, prev, depth, re, limit_size):
        if depth > limit_size:
            return
        next_ = self.generate_next_word(prev)
        re.append(next_)
        self._dfs(next_, depth+1, re, limit_size)
