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
        self.football = db.Futbol  # Platforms
        self.text = ""
        self.language = ""
        self.all_tweets_text = ""
        self.all_tweets_text_array = []

    def tokenization(self):
        # Sentence tokenization
        text_tokenization = sent_tokenize(self.text)

        # Word tokenization
        self.word_tokenizacion = word_tokenize(self.text)
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

        symbols = ["@", "!", ":", "(", ")", "RT", ",", "https", ".", "?", "#", "|", " ", "", "...", "..", "“", "``",
                   "]", "[", "....", "…", "''", "-"]

        # Si no es uno de los símbolos, inserta el texto sin emojis
        for word in self.text_limpio:
            if word not in symbols and word.find("//t.co/") and word.find("//t.co…"):
                self.text_without_emojis.append(emoji.get_emoji_regexp().sub(r'', word))

        for text in self.text_without_emojis:
            if text != "":
                self.all_tweets_text += text.lower() + " "
                self.all_tweets_text_array.append(text.lower())

        print(f"Stopwords: {self.text_limpio}")
        print(f"Text without emojis and symbols: {self.text_without_emojis}")

    def word_cloud(self):

        # Generar el gráfico
        # Hemos cogido el listado de palabras generado antes self.text_limpio
        word_cloud = WordCloud(width=800, height=800,
                               background_color='purple',
                               max_words=40).generate(self.all_tweets_text)
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
        plt.tight_layout()
        plt.show()

    def sentimental_analysis(self):
        english_text = "The Israeli actress and former Miss Israel posted: 'Israel deserves to live as a free and " \
                       "safe nation, adding: Our neighbours deserve the same. The comments attracted thousands of " \
                       "replies - now switched off - leading to her name trending on Twitter. In her youth, " \
                       "Gadot completed two years of mandatory military service. 'My heart breaks,' the 36-year-old " \
                       "posted online. 'My country is at war. I worry for my family, my friends. I worry for my " \
                       "people. This is a vicious cycle that has been going on for far too long. 'I pray for the " \
                       "victims and their families. I pray for this unimaginable hostility to end, I pray for our " \
                       "leaders to find the solution so we could live side by side in peace. I pray for better days.'" \
                       "While some high-profile people, including US politician Ted Cruz, praised Gadot for her " \
                       "remarks, many others reacted angrily. She was criticised by supporters of the Palestinian " \
                       "cause, who pointed to her service in the Israeli military'. "
        sia = SentimentIntensityAnalyzer()
        self.polarity = sia.polarity_scores(english_text)
        print(f"Sentimental analysis polarity: {self.polarity}")

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
        labels = 'Spanish', 'Italy', 'Turkish'
        language_tokenization = word_tokenize(self.language)
        size1 = language_tokenization.count("es")
        size2 = language_tokenization.count("it")
        size3 = language_tokenization.count("tr")
        sizes = [size1, size2, size3]

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title("Language tweets between 16:24:00 and 16:25:00 10 of May",
                  bbox={'facecolor': '0.8', 'pad': 5})
        plt.show()

    def sentimental_analysis_alternative(self):
        labels = self.polarity.keys()
        polarity1 = self.polarity['neg']
        polarity2 = self.polarity['neu']
        polarity3 = self.polarity['pos']
        polarity4 = self.polarity['compound']

        labels = ["Polarities"]
        width = 60                                                                    # the width of the bars: can also be len(x) sequence

        fig, ax = plt.subplots()

        ax.bar(labels, polarity1, width, yerr=polarity1, label='negative')
        ax.bar(labels, polarity2, width, yerr=polarity2, bottom=polarity1,
               label='neutral')
        ax.bar(labels, polarity3, width, yerr=polarity3, bottom=polarity2,
               label='positive')
        ax.bar(labels, polarity4, width, yerr=polarity4, bottom=polarity3,
               label='compound')
        ax.legend()

        plt.show()

    def start(self):
        for i in range(self.football.estimated_document_count()):
            tweet1 = self.football.find()[i]
            self.text = tweet1['text']
            self.language += tweet1['lang'] + " "
            # Text mining
            self.tokenization()
            self.stopwords()
            self.frequency()
            print()

        # Visualización de datos
        print(f"All clean words: {self.all_tweets_text}")
        self.word_cloud()
        print(f"All clean words array: {self.all_tweets_text_array}")
        self.dist_probability()

        # Sentimental analysis
        tokens.sentimental_analysis()
        tokens.bar()

        # Extra graphic
        tokens.pie_chart()
        tokens.sentimental_analysis_alternative()


if __name__ == "__main__":
    tokens = Tokens()
    tokens.start()
