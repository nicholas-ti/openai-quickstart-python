import os
import requests
import openai
from flask import Flask, redirect, render_template, request, url_for
from bs4 import BeautifulSoup

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")




@app.route("/", methods=("GET", "POST"))
def index():
    article_url = request.args.get("article")
    if article_url:
        response = requests.get(article_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        elem_found = soup.find('article') # Find element
        if elem_found:
            text = elem_found.text
            with open('article.txt', 'w') as f:
                f.write(text)

    if request.method == "POST":
        print('POST:')
        with open('article.txt', 'r') as f:
            text = f.read() 
        question = request.form["question"]
        print(text)
        print(question)
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(text, question),
            temperature=0.6,
        )
        print('OPEN AI RESPONSE:')
        print(response)
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")

    return render_template("index.html", result=result, article_url=article_url)


def generate_prompt(article_text, question):
    return """You will be given the text for a news article, and your task is to answer a question about the article.
Be mindful that the text was obtained through web scraping, 
so there will probably be some cluttered information at the beginning and at the end of the text.

Here is the scraped article:

{}

Here is the question:
{}
""".format(
        article_text,
        question
    )
