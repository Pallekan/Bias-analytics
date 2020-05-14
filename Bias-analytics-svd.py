import bs4
import urllib.request
import urllib
import json
from io import StringIO
from html.parser import HTMLParser
import nltk.data
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#returns string
def textExtractSVD(url):
    try:
        urllib.request.urlopen(url).read().decode('utf-8', 'ignore')
    except:
        return("Dålig Länk")
 
    
    
    webpage=(urllib.request.urlopen(url).read().decode('utf-8', 'ignore'))
    #webpage.add_header()
    soup = bs4.BeautifulSoup(webpage,"html5lib")
    article_text = soup.find_all('div',class_="ArticleLayout-container")
    finished_text = []
    i=0
    for x in article_text:
        finished_text.append(str(x.find_all("p")))
        finished_text[i] = finished_text[i].replace(",","")
       # finished_text[i] = finished_text[i].replace(",","")
        i=i+1
    finished_text = "".join(finished_text)
    finished_text = finished_text.replace("[", " ")
    finished_text = finished_text.replace("]", " ")
    
    return(finished_text)


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def get_all_svd(keywords):
    file = open("data.txt", "r")
    articels = []
    tmparticle = ""
    visibility_bias = []
    for line in file:
        tmparticle = textExtractSVD(line)
        tmparticle = strip_tags(tmparticle)
        for word in keywords:
            if(word in tmparticle):
                articels.append(tmparticle)
                break
            else:
                continue
        #print(line)
    

    file.close()
    return(articels)

def make_sentences(text):
    
    tokenizer = nltk.data.load('tokenizers/punkt/swedish.pickle')
    return (tokenizer.tokenize(text))

def get_sentiment(sentences):
    
    analyzer = SentimentIntensityAnalyzer()
    total_comp = 0
    divider = 0
    for sentence in sentences:
        vs = analyzer.polarity_scores(sentence)
        total_comp = total_comp + vs['compound']
        print(vs['compound'])
        if(vs['compound'] != 0):
            divider = divider+1
    print("total comp = " ,total_comp)
    print("divider = ", divider)
    average_compound = total_comp/divider
    return average_compound

def get_visibility(words, keywords):
    number_of_mentions = []

    for each in keywords:
        number_of_mentions.append(words.count(each))

    return(number_of_mentions)

def get_keyword_count(articles, keyword):
    wordcount = []

    for article in articles:    
        for word in keyword:
            if(word in article):
                wordcount.append(word)
    return wordcount
keywords = ["Centerpartiet","centerpartiet", "Annie Lööf", "Kristdemokraterna",
            "kristdemokraterna", "Ebba Busch","Liberalerna", "liberalerna",
            "Jan Björklund", "Miljöpartiet", "miljöpartiet",
            "Språkrör","språkrör", "Isabella Lövin", "Gustav Fridolin"
            "Moderaterna", "moderaterna", "Ulf Kristersson", "Socialdemokraterna"
            ,"socialdemokraterna", "Stefan Löfven"
            , "Sverigedemokraterna", "sverigedemokraterna"," Jimmie Åkesson",
            "Vänsterpartiet", "vänsterpartiet","Jonas Sjöstedt"]

articels = (get_all_svd(keywords))

all_sentiments = []
for each in articels:
    
    sentences = make_sentences(each)
    all_sentiments.append(get_sentiment(sentences))

print(all_sentiments)
average_sentimentbias = sum(all_sentiments)/len(all_sentiments)
all_sentiments = list(filter((0).__ne__, all_sentiments))

print("all sent = ",all_sentiments)
visibility_bias = get_keyword_count(articels, keywords)
number_of_mentions = get_visibility(visibility_bias, keywords)
print(visibility_bias)
print(number_of_mentions)
print("antal artiklar = ",len(articels))
print("average sentiment bias = ", average_sentimentbias)


#data = {}
#data['data'] = []
#data['data'].append({
 #   'text': articels[0],
 #   'sentiment' : average_compound
#})

#with open('sentiment.txt', 'w') as outfile:
 #   json.dump(data, outfile)











#Code for dumping
#data = {}
#data['text'] = []
#data['text'].append({
 #   'text' : soup.get_text(),
  #  'website': "SVD"
#})

#with open('data.txt', 'w') as outfile:
 #   json.dump(data, outfile)

#with open('test.csv', mode='w') as employee_file:
 #       test_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  #      test_writer.writerow(soup.get_text())


