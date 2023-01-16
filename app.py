from flask import Flask , url_for, render_template,request
import requests
import bs4
import re
import wikipedia
import spacy
import warnings
warnings.filterwarnings('ignore')
nlp = spacy.load("en_core_web_sm")
app = Flask(__name__)

@app.route('/')
def Home():
    return render_template('home.html')

@app.route('/result',methods=['GET','POST'])
def result():
    if request.method == 'POST':
        try:
            page_url = str(request.form['page_url'])
            # code for full linc
            if page_url.startswith('http'):
                response = requests.get(page_url)
                soup = bs4.BeautifulSoup(response.text, "html.parser")
                sumary = wikipedia.summary(page_url[30:])

            # code for half linc
            else:
                base_url = "https://en.wikipedia.org/wiki/"
                sumary = wikipedia.summary(page_url)
                page_url = base_url+page_url
                response = requests.get(page_url)
                soup = bs4.BeautifulSoup(response.text,"html.parser")
                sumary = wikipedia.summary(page_url[30:])      

        except:
            return render_template('error.html')
        else:
            

            # Scraping the page title
            page_title = soup.find("h1", class_="firstHeading").text

            # Scraping all the paragraphs
            text = " "
            for p in soup.find_all("p"):
                text += p.text
            #cleaned the text
            cleaned_text = re.sub("[^a-zA-Z-0-9]"," ",text)
            doc = nlp(text)
            named_entity = []
            for ent in doc.ents:
                entity = ent.text,ent.start_char,ent.end_char,ent.label_
                named_entity.append(entity)
            return render_template('result.html',page_title=page_title,cleaned_text = cleaned_text,
                sumary = sumary,
                named_entity = named_entity)

if __name__ == "__main__":
    app.run(debug=True)