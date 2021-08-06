import nltk
from nltk import FreqDist

# Get the Gutenberg book for testing 
nltk.download('gutenberg')
from nltk.corpus import gutenberg

# Get the common english words
nltk.download('stopwords')
from nltk.corpus import stopwords

from flask import Flask
app = Flask(__name__)

@app.route("/")
def count_words():
    # Define the stopword set
    stopWords = set(stopwords.words('english'))

    # load the tokens from Sense and Sensibility, 
    # and then create a list of lower case words if they are not punctuation.
    tokens = gutenberg.words('austen-sense.txt')
    tokens = [word.lower() for word in tokens if word.isalpha()]
    tokens = [word for word in tokens if word not in stopWords]

    # Create a frequency distribution using the extracted tokens. 
    # From the frequency distribution extract the most common 500 words.
    fdist = FreqDist(tokens)
    common = fdist.most_common(500)

    '''
    The most common word data structure is a sequence 
    with each entry being a tuple of the word and its frequency. 
    To be able to create the word output 
    we need to extract the words from the dictionary into a list and sort them.
    '''
    words = []
    for word, frequency in common:
        words.append(word)
    words.sort()

    # frequency of the most common word for formatting the font size and colour of the HTML output.
    highCount = common[0][1]

    html = """
    <html><head><title>Words count</title></head>
        <body><h1>Most Common Words in Sense and Sensibility</h1>
    """

    
    for word in words:

        # Calculate the font size
        size = str(int(15 + fdist[word] / float(highCount) * 150))
        colour = str(hex(int(0.8 * fdist[word] / \
                        float(highCount) * 256**3)))
        colour = colour[-(len(colour) - 2):]
        while len(colour) < 6:
            colour = "0" + colour
        
        # Add the formatted words    
        html += f"<span style=\"font-size: {size}px; color: #{colour}\">{word}</span>\n"
    
    html += "</body></html>"

    return html

if __name__ == "__main__":
    app.run()
