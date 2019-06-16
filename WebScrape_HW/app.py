from flask import Flask, render_template, redirect
import pymongo
import mars_scrape

# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.mars_db


# Set route
@app.route('/')
def index():
    # Store the entire team collection in a list
    mars_data = db.items.find_one()
    print(mars_data)

    # Return the template with the teams list passed in
    return render_template('index.html', mars_data=mars_data)

@app.route('/mars_scrape')
def scraper():
    mars_data = db.items.find_one()
    mars_scrape_data = mars_scrape.mars_scrape()
    mars_data.update(mars_scrape_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
