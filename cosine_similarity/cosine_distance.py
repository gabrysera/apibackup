from clean_string import CleanStrings
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

class Cosine_distance:

    def get_vectorized_word(self, dictionary, word):
        cleaned_words = []
        for n in dictionary:
            cleaned_words.append(str(CleanStrings.clean_word(n)))
        cleaned_words.append(str(CleanStrings.clean_word(word)))
        vecto = CountVectorizer()
        vectorizer = vecto.fit_transform(cleaned_words)
        vectors = vectorizer.toarray()

        csim = cosine_similarity(vectors)

        c = 0.0
        index = 0
        for i in range(0,len(csim[0])-2):
            z = csim[len(csim)-1][i]
            if z >= c or z >= 1:
                c = z
                index = i
        
        return {
            'item' : dictionary[index],
            'index' : index,
            'similarity' : c
        }
