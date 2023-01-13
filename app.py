from flask import Flask , url_for, render_template,request
import requests
import bs4
import re

app = Flask(__name__)
url = "https://en.wikipedia.org/wiki/global warming"

response = requests.get(url)
soup = bs4.BeautifulSoup(response.text, "html.parser")

# Scraping the page title
page_title = soup.find("h1", class_="firstHeading").text

# Scraping all the paragraphs
text = " "
for p in soup.find_all("p"):
    text += p.text
#cleaned the text
cleaned_text = re.sub("[^a-zA-Z-0-9]"," ",text)


if __name__ == "__main__":
    app.run(debug=True)