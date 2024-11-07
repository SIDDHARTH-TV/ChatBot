import random
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
import bs4 as BeautifulSoup
import urllib.request
import re

def fetch_data(user_input):
   # fetching the content from the URL
   user_input=re.sub(r' ', '_', str(user_input))
   fetched_data = urllib.request.urlopen('https://en.wikipedia.org/wiki/'+user_input)
   article_read = fetched_data.read()
   # parsing the URL content and storing in a variable
   article_parsed = BeautifulSoup.BeautifulSoup(article_read, 'html.parser')

   # returning <p> tags
   paragraphs = article_parsed.find_all('p')

   article_content = ''

   # looping through the paragraphs and adding them to the variable
   for p in paragraphs:
      article_content += p.text
   return article_content

def _create_dictionary_table(text_string) -> dict:
    # removing stop words
    stop_words = set(stopwords.words("english"))

    words = word_tokenize(text_string)

    # reducing words to their root form
    stem = PorterStemmer()

    # creating dictionary for the word frequency table
    frequency_table = dict()
    for wd in words:
        wd = stem.stem(wd)
        if wd in stop_words:
            continue
        if wd in frequency_table:
            frequency_table[wd] += 1
        else:
            frequency_table[wd] = 1

    return frequency_table


def _calculate_sentence_scores(sentences, frequency_table) -> dict:
    # algorithm for scoring a sentence by its words
    sentence_weight = dict()

    for sentence in sentences:
        sentence_wordcount = (len(word_tokenize(sentence)))
        sentence_wordcount_without_stop_words = 0
        for word_weight in frequency_table:
            if word_weight in sentence.lower():
                sentence_wordcount_without_stop_words += 1
                if sentence[:7] in sentence_weight:
                    sentence_weight[sentence[:7]] += frequency_table[word_weight]
                else:
                    sentence_weight[sentence[:7]] = frequency_table[word_weight]

        sentence_weight[sentence[:7]] = sentence_weight[sentence[:7]] / sentence_wordcount_without_stop_words

    return sentence_weight


def _calculate_average_score(sentence_weight) -> int:
    # calculating the average score for the sentences
    sum_values = 0
    for entry in sentence_weight:
        sum_values += sentence_weight[entry]

    # getting sentence average value from source text
    average_score = (sum_values / len(sentence_weight))

    return average_score


def _get_article_summary(sentences, sentence_weight, threshold):
    sentence_counter = 0
    article_summary = ''

    for sentence in sentences:
        if sentence[:7] in sentence_weight and sentence_weight[sentence[:7]] >= (threshold):
            article_summary += " " + sentence
            sentence_counter += 1

    return article_summary


def _run_article_summary(article):
    # creating a dictionary for the word frequency table
    frequency_table = _create_dictionary_table(article)

    # tokenizing the sentences
    sentences = sent_tokenize(article)

    # algorithm for scoring a sentence by its words
    sentence_scores = _calculate_sentence_scores(sentences, frequency_table)

    # getting the threshold
    threshold = _calculate_average_score(sentence_scores)

    # producing the summary
    article_summary = _get_article_summary(sentences, sentence_scores, 1.5 * threshold)

    article_summary=re.sub(r'\[[0-9]*\]',' ', str(article_summary))
    article_summary = re.sub(r'\s+',' ',str(article_summary))

    article_summary = re.sub(r'[^a-zA-Z]', ' ', str(article_summary))
    article_summary = re.sub(r'\s+', ' ', str(article_summary))


    return article_summary


print("Meow:- Hey there..! I am virtual Bot..I will answer your queries for a while..;)")
print("Meow:- Before we begin..May I know your good name..?")
client_name=input()
if 'my name is' in client_name:
  client_name=client_name.replace('my name is','')
elif "i'm" in client_name:
  client_name=client_name.replace("i'm","")
elif "i am"  in client_name:
  client_name=client_name.replace('i am','')

print("Meow:- Hi "+client_name+"..!Nice to see you..How may i help you..?")

def greetings(input):
  greetings_by_bot = ['Hey..!'+client_name+'..!', 'Hi..!'+client_name+'..!', 'Hello..!'+client_name+'..!', 'Hola..!'+client_name+'..!']
  greetings_by_user = ['hello', 'hola', 'hey', 'hi','Hi','Hola','Hey','HELLO','HI','HOLA']

  for word in input.split():
    if word in greetings_by_user:
      return random.choice(greetings_by_bot)

def leaving_greeting(input):
  leaving_greeting_by_bot=["Ok bye "+client_name,"Bye "+client_name]
  leaving_greeting_by_user=["Ok bye","ok bye","OK bye","thank you bye","Bye","bye","Thank You Bye","BYE"]

  for word in input.split():
    if word in leaving_greeting_by_user:
      return print("Meow:-"+random.choice(leaving_greeting_by_bot))

leaving_greeting_by_user = ["Ok bye","ok bye", "thank you bye", "Bye", "bye", "Thank You Bye", "BYE"]

while (True):
  try:
    user_input=input()
    if user_input in leaving_greeting_by_user:
      leaving_greeting(user_input)
      break
    else:
      if greetings(user_input) != None:
        print(greetings(user_input))
      else:
        text_data=fetch_data(user_input)
        summary_results = _run_article_summary(text_data)
        # print(summary_results)
        line_length = 170
        lines = [summary_results[i:i + line_length] + '\n' for i in range(0, len(summary_results), line_length)]
        finalOutput = ''.join(lines)
        print(finalOutput[0:1010])

  except:
      text_data = fetch_data(user_input)
      summary_results = _run_article_summary(text_data)
      # print(summary_results)
      line_length = 170
      lines = [summary_results[i:i + line_length] + '\n' for i in range(0, len(summary_results), line_length)]
      finalOutput=''.join(lines)
      print(finalOutput[0:1010])

