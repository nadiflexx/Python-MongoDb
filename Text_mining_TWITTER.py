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
        self.football = db.Futbol
        # Important variables to manipulate
        self.text = ""
        self.language = ""
        self.all_tweets_text = ""
        self.all_tweets_text_array = []

    def tokenization(self):
        # Sentence tokenization
        text_tokenization = sent_tokenize(self.text)

        # Word tokenization
        self.word_tokenization = word_tokenize(self.text)

        # Print tokenization about one text
        print(f"Sentence Tokenization: {text_tokenization}")
        print(f"Word Tokenization: {self.word_tokenization}")

    def stopwords(self):
        # Pick up the stopwords of the set of the nltk corpus
        self.stop_words = set(stopwords.words("spanish"))

        # For each word it checks if it is in the list of "stopwords"
        self.text_without_stopwords = []

        for word in self.word_tokenization:
            if word not in self.stop_words:
                self.text_without_stopwords.append(word)

        # To clean the special characters that doesn't provide any useful information we need to add them into an array

        symbols = ["@", "!", ":", "(", ")", "RT", ",", "https", ".", "?", "#", "|", " ", "", "...", "..", "“", "``",
                   "]", "[", "....", "…", "''", "-"]

        # This variable is where we are going to store all the clean text
        self.text_without_emojis = []

        # If the word of the text is not a symbol we will append it to the clean text array.
        for word in self.text_without_stopwords:
            if word not in symbols and word.find("//t.co/") and word.find("//t.co…"):
                self.text_without_emojis.append(emoji.get_emoji_regexp().sub(r'', word))

        # Also we need to add the clean text into variables that we are going to use in the WordCloud and Probability
        for text in self.text_without_emojis:
            if text != "":
                self.all_tweets_text += text.lower() + " "
                self.all_tweets_text_array.append(text.lower())

        # Print the text without stopwords and without symbols
        print(f"Stopwords: {self.text_without_stopwords}")
        print(f"Text without emojis and symbols: {self.text_without_emojis}")

    def frequency(self):
        # Call frequency distribution function passing word tokenization by parameter
        self.freq_distribution = FreqDist(self.word_tokenization)
        freq_results = []

        # Loop through all the word from the text without emojis and add the word and the number of times that is
        # repeated inside freq_result array. Then prints the information of each word.
        for word in self.text_without_emojis:
            freq_count = word, self.freq_distribution.get(word)
            freq_results.append(freq_count)
        print(f"Frequency: {freq_results}")

    def word_cloud(self):
        # To create a WordCloud graphic we need to specify the size of the graphic, the text that we are going to use
        # (String of all words) and other parameters like the number of words that you want to show or the background
        # color.
        word_cloud = WordCloud(width=800, height=800,
                               background_color='purple',
                               max_words=40).generate(self.all_tweets_text)
        # Here we call some functions to show the graphic
        plt.imshow(word_cloud, interpolation='bilinear')
        # Disable axis
        plt.axis('off')
        # Set title with a box.
        plt.title("WORD CLOUD",
                  bbox={'facecolor': '0.8', 'pad': 5})
        # Show the graphic
        plt.show()

    def dist_probability(self):
        # Call frequency distribution function passing all clean words in a array.
        freq_distribution_probability = FreqDist(self.all_tweets_text_array)
        # Set a title to the graphic
        plt.title("PROBABILITY",
                  bbox={'facecolor': '0.8', 'pad': 5})
        # Calls plot function to set the number of words to show.
        freq_distribution_probability.plot(10, cumulative=False)
        plt.tight_layout()
        # Shows the graphic
        plt.show()

    def sentimental_analysis(self):
        # Here I pick an actual notice from BBC because sentimental analysis only works in English language.
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
        # Store sentimental analysis analyzer in a variable
        sia = SentimentIntensityAnalyzer()
        # Save the results in the variable polarity.
        self.polarity = sia.polarity_scores(english_text)
        # Prints the results.
        print(f"Sentimental analysis polarity: {self.polarity}")

    def bar(self):
        # To show the sentimental analysis first of all we need to set up all the axis names and values
        eje_x = list(("negative", "neutral", "positive", "compound"))
        polarity1 = self.polarity['neg']*100
        polarity2 = self.polarity['neu']*100
        polarity3 = self.polarity['pos']*100
        polarity4 = self.polarity['compound']*100
        values = [polarity1, polarity2, polarity3, polarity4]

        plt.bar(eje_x, values)
        plt.xlabel("Types of feelings")
        plt.ylabel("Feelings polarity (%)")
        plt.title("SENTIMENTAL ANALYSIS",
                  bbox={'facecolor': '0.8', 'pad': 5})
        # When all is set up we show the graphic
        plt.show()

    def pie_chart(self):
        # Extra graphic pie.
        # In this graphic I use all the languages of the 50 tweets between 16:24:00 and 16:25:00
        labels = 'Spanish', 'Italy', 'Turkish'
        # Here I separate in words all the languages
        language_tokenization = word_tokenize(self.language)
        # Then I count all the times one languages is repeated and store it in a variable
        size1 = language_tokenization.count("es")
        size2 = language_tokenization.count("it")
        size3 = language_tokenization.count("tr")
        # After that I save all the variables in an array variable because this graphic needs an array to
        # understand the values.
        sizes = [size1, size2, size3]

        fig1, ax1 = plt.subplots()
        # Here we set up the graphic passing the necessary variables (Labels and values)
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        # Equal aspect ratio ensures that pie is drawn as a circle.
        ax1.axis('equal')
        plt.title("Language tweets between 16:24:00 and 16:25:00 10 of May",
                  bbox={'facecolor': '0.8', 'pad': 5})
        # Shows the graphic
        plt.show()

    def sentimental_analysis_alternative(self):
        # Here I create an alternative sentimental analysis graphic.
        # As the pie graphic we need to set up all the values and the label name.
        labels = ["Polarities"]

        polarity1 = self.polarity['neg']
        polarity2 = self.polarity['pos']
        polarity3 = self.polarity['neu']
        polarity4 = self.polarity['compound']
        width = 0.1

        fig, ax = plt.subplots()
        # Then we have to put one value on top of the other thanks to the bottom attribute where we can specify which
        # one will be below.
        ax.bar(labels, polarity1, width, label='positive')
        ax.bar(labels, polarity2, width, bottom=polarity1,
               label='positive')
        ax.bar(labels, polarity3, width, bottom=polarity2,
               label='neutral')
        ax.bar(labels, polarity4, width, bottom=polarity3,
               label='compound')
        ax.legend()
        # Show the graphic
        plt.show()

    def start(self):
        # Loops through all the tweets stored in the database
        for i in range(self.football.estimated_document_count()):
            # Finds one tweet
            tweet1 = self.football.find()[i]
            # Saves the text of a tweet.
            self.text = tweet1['text']
            # Add the language of the tweet in a String format.
            self.language += tweet1['lang'] + " "

            # For each tweet we are going to call the Text Mining functions
            self.tokenization()
            self.stopwords()
            self.frequency()
            print()

        # After all tweets are analyzed, we call graphic functions.
        # Also we print all the clean words in String and Array format (That's because we We need them so that the
        # graphics can interpret them)
        print(f"All clean words: {self.all_tweets_text}")
        self.word_cloud()
        print(f"All clean words array: {self.all_tweets_text_array}")
        self.dist_probability()
        tokens.sentimental_analysis()
        tokens.bar()

        # Extra graphics
        tokens.pie_chart()
        tokens.sentimental_analysis_alternative()


if __name__ == "__main__":
    # Calls tokens class
    tokens = Tokens()
    # Calls function start
    tokens.start()
