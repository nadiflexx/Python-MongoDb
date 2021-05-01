import emoji
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# nltk.download()
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from pymongo import MongoClient
from wordcloud import WordCloud


class Tokens:
    def __init__(self):

        # Mongodb connection
        self.conn = MongoClient('mongodb://root:root@127.0.0.1:27017')
        # Mongodb database and repository
        db = self.conn.Twitter
        # Collections
        self.barcelona = db.Barcelona  # Platforms
        self.text = ""
        self.activity = ""
        self.all_tweets_activity = []
        self.all_tweets_text = ""
        self.all_tweets_text_array = []

    def tokenization(self):
        # Sentence tokenization
        text_tokenization = sent_tokenize(self.text)

        # Word tokenization
        self.word_tokenizacion = word_tokenize(self.text)
        self.all_tweets_activity.append(word_tokenize(self.activity)[3][3:-3])
        print(f"Sentence Tokenization: {text_tokenization}")
        print(f"Word Tokenization: {self.word_tokenizacion}")

    def frequency(self):

        self.freq_distribution = FreqDist(self.word_tokenizacion)
        freq_results = []
        for word in self.text_without_emojis:
            freq_count = word, self.freq_distribution.get(word)
            freq_results.append(freq_count)
        print(f"Frequency: {freq_results}")

    def stopwords(self):

        # Recoger las palabras del set del corpus de nltk
        self.stop_words = set(stopwords.words("spanish"))

        # Para cada palabra comprueba si está en la lista de "stopwords"
        self.text_limpio = []

        for word in self.word_tokenizacion:
            if word not in self.stop_words:
                self.text_limpio.append(word)

        # Vamos a limpiar los carácteres especiales y espacios de los datos porque no nos aportan información
        # Quitaremos símnolos de "@", "!", """, ":", "(, ")", "RT", ","

        self.text_without_emojis = []

        symbols = ["@", "!", ":", "(", ")", "RT", ",", "https", ".", "?", "#", "|"]

        # Si no es uno de los símbolos, inserta el texto sin emojis
        for word in self.text_limpio:
            if word not in symbols and word.find("//t.co/"):
                self.text_without_emojis.append(emoji.get_emoji_regexp().sub(u'', word))

        for text in self.text_without_emojis:
            self.all_tweets_text += text.lower() + " "
            self.all_tweets_text_array.append(text)

        print(f"Stopwords: {self.text_limpio}")
        print(f"Text without emojis and symbols: {self.text_without_emojis}")

    def word_cloud(self):

        # Generar el gráfico
        # Hemos cogido el listado de palabras generado antes self.text_limpio
        word_cloud = WordCloud(width=800, height=800,
                               background_color='purple',
                               stopwords=self.all_tweets_text, max_words=40).generate(self.all_tweets_text)
        # Visualizarlo
        plt.imshow(word_cloud, interpolation='bilinear')  # Mostrar el gráfico
        plt.axis('off')  # Quitar ejes
        plt.title("WORD CLOUD",
                  bbox={'facecolor': '0.8', 'pad': 5})
        plt.show()  # mostrar

    def dist_probability(self):
        freq_distribution_probability = FreqDist(self.all_tweets_text_array)
        plt.title("PROBABILITY",
                  bbox={'facecolor': '0.8', 'pad': 5})

        freq_distribution_probability.plot(10, cumulative=False)
        plt.show()

    def sentimental_analysis(self):
        sia = SentimentIntensityAnalyzer()
        self.polarity = sia.polarity_scores(self.all_tweets_text)

    def bar(self):
        eje_x = list(("negative", "neutral", "positive", "compound"))
        values = list(self.polarity.values())

        plt.bar(eje_x, values)
        plt.xlabel("Tipos de sentimientos")
        plt.ylabel("Polaridad de los sentimientos")
        plt.title("SENTIMENTAL ANALYSIS",
                  bbox={'facecolor': '0.8', 'pad': 5})
        plt.show()

    def pie_chart(self):
        labels = '13 - 20 minutes', '21- 30 minutes', '31-39 minutes'

        size1 = self.count_size_activity(20, 13)
        size2 = self.count_size_activity(30, 21)
        size3 = self.count_size_activity(39, 31)
        sizes = [size1, size2, size3]

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title("Activity between 13:13:00 and 13:39:00 public tweets",
                  bbox={'facecolor': '0.8', 'pad': 5})
        plt.show()

    def count_size_activity(self, counter, i):
        start = i
        size = 0
        while start <= counter:
            size += self.all_tweets_activity.count(f"{counter}")
            start += 1
        return size

    def start(self):
        for i in range(self.barcelona.estimated_document_count()):
            tweet1 = self.barcelona.find()[i]
            self.text = tweet1['text']
            self.activity = tweet1['created_at']
            # Text mining
            self.tokenization()
            self.stopwords()
            self.frequency()
            print()

        # Visualización de datos
        print(f"All clean words: {self.all_tweets_text}")
        self.word_cloud()
        self.dist_probability()

        # Sentimental analysis
        tokens.sentimental_analysis()
        tokens.bar()
        # print(self.all_tweets_activity)
        tokens.pie_chart()


if __name__ == "__main__":
    tokens = Tokens()
    tokens.start()
