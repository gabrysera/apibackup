from nltk.corpus import stopwords
import string

class CleanStrings:

    def clean_word(text):
        stopwd = stopwords.words('italian')
        text = ''.join([word for word in text if word not in string.punctuation])
        text = text.lower()
        text = ' '.join([word for word in text.split() if word not in stopwd])
        return text