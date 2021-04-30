
from pymongo import MongoClient

import nltk
# nltk.download()
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords

from wordcloud import WordCloud
import matplotlib.pyplot as plt

from nltk.sentiment.vader import SentimentIntensityAnalyzer


class Tokens:
    def __init__(self):

        # Mongodb connectionSe
        self.conn = MongoClient('mongodb://root:root@127.0.0.1:27017')
        # Mongodb database and repository
        db = self.conn.Twitter
        # Collections
        self.barcelona = db.Barcelona  # Platforms
        self.text = ""
        self.all_twitts = []

    def tokenizacion(self):

        # Sentence tokenization
        text_tokenizacion = sent_tokenize(self.text)

        # Word tokenization
        self.word_tokenizacion = word_tokenize(self.text)
        print(f"Sentence Tokenization: {text_tokenizacion}")
        print(f"Word Tokenization: {self.word_tokenizacion}")

    def frequency(self):
        self.freq_distribution = FreqDist(self.word_tokenizacion)
        freq_results = []
        for word in self.text_sin_symbolos:
            freq_count = word, self.freq_distribution.get(word)
            freq_results.append(freq_count)
        print(f"Frequency: {freq_results}")

    def stopwords(self):
        # Recoger las palabras del set del corpus de nltk
        stop_words = set(stopwords.words("spanish"))

        # Para cada palabra comprueba si está en la lista de "stopwords"
        self.text_limpio = []

        for word in self.word_tokenizacion:
            if word not in stop_words:
                self.text_limpio.append(word)

        # Vamos a limpiar los carácteres especiales y espacios de los datos porque no nos aportan información
        # Quitaremos símnolos de "@", "!", """, ":", "(, ")", "RT", ","

        self.text_sin_symbolos = []
        self.text_sin_emojis = []
        simbolos = ["@", "!", ":", "(", ")", "RT", ","]

        # Si no es uno de los símbolos, inserta el texto sin emojis
        for word in self.text_limpio:
            if word not in simbolos:
                self.text_sin_symbolos.append(word)
                # self.text_sin_emojis.append(emoji.get_emoji_regexp().sub(u'', word))
        self.all_twitts.append(self.text_sin_symbolos)
        print(f"Stopwords: {self.text_limpio}")
        print(f"Text without symbols: {self.text_sin_symbolos}")

    def word_cloud(self):

        # Generar el gráfico
        # Hemos cogido el listado de palabras generado antes self.text_limpio
        wordcloud = WordCloud(width=800, height=800,
                              background_color='white',
                              stopwords=self.text_sin_symbolos, max_words=40)

        wordcloud.generate(self.text)

        # Visualizarlo
        plt.imshow(wordcloud, interpolation='bilinear')  # Mostrar el gráfico
        plt.axis('off')  # Quitar ejes
        plt.show()  # mostrar

    def dist_probabilidad(self):
        self.freq_distribution.plot(10, cumulative=False)
        plt.show()

    def sentimental_analysis(self):
        sia = SentimentIntensityAnalyzer()
        self.polarity = sia.polarity_scores(self.text)
        print(self.polarity)

    def bar(self):
        eje_x = list(self.polarity.keys())
        valores = list(self.polarity.values())

        plt.bar(eje_x, valores)
        plt.xlabel("Tipos de sentimientos sentimientos")
        plt.ylabel("Polaridad de los sentimientos")
        plt.ylabel("Sentimental analysis")
        plt.show()

    def start(self):
        for i in range(self.barcelona.estimated_document_count()):
            tweet1 = self.barcelona.find()[i]
            self.text = tweet1['text']
            # Text mining
            self.tokenizacion()
            self.stopwords()
            self.frequency()
            print()

        # Visualización de datos
        print(self.all_twitts)
        self.word_cloud()
        self.dist_probabilidad()
        # Sentimental analysis
        # tokens.sentimental_analysis()
        # tokens.bar()



if __name__ == "__main__":
    tokens = Tokens()
    tokens.start()
