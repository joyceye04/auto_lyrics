import jieba
import collections, pickle


def ch_split(sentence):
    return list(jieba.cut(sentence, cut_all=False))


def get_chunks(tokens, chunk_size):
    chunk_size = min(chunk_size, len(tokens))
    for chunk in range(2, chunk_size+1):
        for i in range(0, len(tokens) - chunk + 1):
            yield tokens[i:i+chunk]


class AutoCompleteModel:
    
    def __init__(self):
        self.single_words_model = dict()
        self.tuple_words_model = dict()
        self.chunk_size = 2
        
    def build_model(self, data):
        words_list = []
        sentence_list = []
        for sentence in data.split("\n"):
            x = ch_split(sentence)
            words_list += x
            sentence_list.append(x)

        self.single_words_model.update(collections.Counter(words_list))

        word_tuples = []
        for sentence in sentence_list:
            word_tuples += get_chunks(sentence, self.chunk_size)

        self.tuple_words_model.update({items[0]: collections.Counter() for items in word_tuples})

        for tup in word_tuples:
            try:
                for offset in range(2, self.chunk_size + 1):
                    self.tuple_words_model[tup[0]].update([" ".join(tup[1:offset])])
            except:
                print("error in word tuples")
        print(self.single_words_model)
        print(self.tuple_words_model)
        
    
    def compress_model(self, compress_bound):
        print("compressing model")
        selected = []
        for key, sub in self.tuple_words_model.items():
            for k2 in sub:
                if sub[k2] < compress_bound:
                    selected.append((key, k2))
        for k1, to_rm in selected:
            del self.tuple_words_model[k1][to_rm]

        selected = []
        for key in self.words_model:
            if self.words_model[key] < compress_bound:
                selected.append(key)

        for to_rm in selected:
            self.words_model.pop(to_rm)
    
    def save_model(self, model_path="model.pkl"):
        
        print("saving to:", model_path)

        pickle.dump({'single_words_model': self.single_words_model, 'tuple_words_model': self.tuple_words_model},
                        open(model_path, 'wb'), protocol=2)
    
    def load_model(self, model_path):
        
        models = pickle.load(open(model_path,'rb'))
        self.single_words_model = models['single_words_model']
        self.tuple_words_model = models['tuple_words_model']

        print("successfully loaded: {}".format(model_path))
    
    def get_single_words_model(self):
        pass

    def get_tuple_words_model(self):
        pass

