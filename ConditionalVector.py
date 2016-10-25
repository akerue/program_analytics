# _*_coding:utf-8_*_


# NLTKの中にConditionalfreqdistというライブラリが用意されているが
# とりあえず自作してみる
class ConditionalVector:

    def __init__(self, bag_of_ngrams):
        self.N = len(bag_of_ngrams[0])
        self.freq_vec = {}
        self.num_of_ngrams = len(bag_of_ngrams)

        for ngram in bag_of_ngrams:
            if ngram[:-1] in self.freq_vec:
                if ngram[-1] in self.freq_vec[ngram[:-1]]:
                    self.freq_vec[ngram[:-1]][ngram[-1]] += 1
                else:
                    self.freq_vec[ngram[:-1]][ngram[-1]] = 1
            else:
                self.freq_vec[ngram[:-1]] = {}
                self.freq_vec[ngram[:-1]][ngram[-1]] = 1

        self.prob_vec = {}
        for pre_words, post_word_dict in self.freq_vec.items():
            for post_word, freq in post_word_dict.items():
                if pre_words in self.prob_vec:
                    self.prob_vec[pre_words][post_word] = float(freq)/self.num_of_ngrams
                else:
                    self.prob_vec[pre_words] = {}
                    self.prob_vec[pre_words][post_word] = float(freq)/self.num_of_ngrams

    def max(self, condition):
        dic = self.freq_vec[condition]
        return dic.keys()[dic.values().index(max(dic.values()))]

    def freq(self, next_word, *condition):
        try:
            return self.freq_vec[condition[0]][next_word]
        except KeyError:
            return 0

    def prob(self, next_word, *condition):
        try:
            return self.prob_vec[condition[0]][next_word]
        except KeyError:
            return 0.0
