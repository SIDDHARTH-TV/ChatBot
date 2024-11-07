from newspaper import Article
import random
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')
import googlesearch
import re


nltk.download('punkt',quiet=True)

print("Bot:- Hey there..! I am virtual Bot..I will answer your queries for a while..;)")
print("Bot:- Before we begin..May I know your good name..?")
client_name=input()
if 'my name is' in client_name:
  client_name=client_name.replace('my name is','')
elif "i'm" in client_name:
  client_name=client_name.replace("i'm","")
elif "i am"  in client_name:
  client_name=client_name.replace('i am','')

print("Bot:- Hi "+client_name+"..!Nice to see you..How may i help you..?")

def index_sort(list_var):
  length = len(list_var)
  list_index = list(range(0, length))

  x = list_var
  for i in range(length):
    for j in range(length):
      if x[list_index[i]] > x[list_index[j]]:
        temp = list_index[i]
        list_index[i] = list_index[j]
        list_index[j] = temp

  return list_index

def get_data(user_input):
  dataInfo=googlesearch.search(user_input)
  any_data=random.choice(dataInfo)
  article = Article(any_data)
  article.download()
  article.parse()
  article.nlp()
  saerched_data = article.text
  text_data=saerched_data
  sentence2_list=nltk.sent_tokenize(text_data)
  user_input = user_input.lower()
  sentence2_list.append(user_input)
  bot_response = ''
  cm = CountVectorizer().fit_transform(sentence2_list)
  similarity_scores = cosine_similarity(cm[-1], cm)
  similarity_scores_list = similarity_scores.flatten()
  index = index_sort(similarity_scores_list)
  index = index[1:]
  response_flag = 0
  j = 0
  for i in range(len(index)):
    if similarity_scores_list[index[i]] > 0.0:
      bot_response = bot_response + ' ' + sentence2_list[index[i]]
      response_flag = 1
      j = j + 1
    if j > 2:
      break
  if response_flag == 0:
    bot_response = bot_response + " " + " Sorry..! can you please try it back.."
  sentence2_list.remove(user_input)
  bot_response=re.sub("[\(\[].*?[\)\]]", "",bot_response)
  print(bot_response)
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
      return print("Bot:-"+random.choice(leaving_greeting_by_bot))

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
        get_data(user_input)
  except:
    get_data(user_input)
