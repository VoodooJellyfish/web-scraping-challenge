from flask import Flask, render_template, redirect
from flask_pymongo import pymongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# db = client.mars_db
# db.clean_collection.drop()
# clean_collection = db.clean_collection
# mars_data = scrape_mars.scrape()
# clean_collection.insert_one(mars_data)

# results = clean_collection.find()
# for result in results:
#     print(result)

@app.route("/scrape")
def scraper():
    db = client.mars_db
    db.clean_collection.drop()
    clean_collection = db.clean_collection
    mars_data = scrape_mars.scrape()
    clean_collection.insert_one(mars_data)
    db = mars_data
    #return redirect("/", code=302)
    return render_template("index.html", db=db) 

# @app.route("/scrape")
# def scraper():
#     db = client.mars_db
#     db.clean_collection.drop()
#     clean_collection = db.clean_collection
#     mars_data = scrape_mars.scrape()
#     clean_collection.insert_one(mars_data)
#     db = mars_data
#     #return redirect("/", code=302)
#     return render_template("index.html", db=db) 

if __name__ == "__main__":
    app.run(debug=True)