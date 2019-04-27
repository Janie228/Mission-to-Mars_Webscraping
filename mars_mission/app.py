import os
from flask import Flask, render_template, redirect, url_for
# from flask_pymongo import PyMongo
from pymongo import MongoClient
import Scraper as scp

# Initialize flask & mongodb 
app = Flask(__name__)
# local mongo
# db = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
# AWS Mongo Atlas
client = MongoClient("mongodb+srv://admin:admin123@janie-test-vcn3t.mongodb.net/test?retryWrites=true")
db = client.mars_app

# Default home page rendering html & data pass to it
@app.route('/')
def index():
    mars_data = db.mars.find_one()
    return render_template('index.html', mars = mars_data)

# When button was clicked on the home page, this will 
# call the scrape function to get the updates
@app.route('/scrape')
def scrape():
    print("scraping function")
    # Call scrape function and get data return from it
    mars = db.mars
    data = scp.scrape_mars()

    # Update mongodb with new data
    mars.update(
        {},
        data,
        upsert=True
    )

    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
