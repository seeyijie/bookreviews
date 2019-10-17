# Database Project

## Instructions (How to run):
* Download MySQL and create a database with name "50043_DB"
* Create a new user and give it admin permission
* Run `export MYSQL_USER=<USER>` to set environment variables
* Run `export MYSQL_PASSWORD=<PASSWORD>` to set environment variables
* Run `export FLASK_APP=manage.py` to point the entry of "flask run" to manage.py (factory init method)
* Run `flask db init` and then `flask db migrate`. **Important:** if you have issues running these commands, check the following subpoints 
    * make sure to run `pip install -r requirements.txt` to get the `flask-migrate` library which enables the flask db commands.
    * Make sure a database named 50043_DB exists in your local mysql environment, and users defined in the environment variables have full permissions to a database named `50043_DB`.
* Verify the new .py file in the migrations/versions and check if the upgrades are correct.
* Run `flask db upgrade` to apply the migration
* Run `flask run` and go to `127.0.0.1:5000/register`

## Automation scripts
* `start_init.sh`(run this):
    * this script installs dos2unix and converts `initialize.sh` to be able to run on WSL
    * to run, do `sudo ./start_init.sh`
* `initialize.sh` (do not need to run this): 
    * to run, do `sudo ./initialize.sh` and enter your password.
    * this script checks if you have a database named `50043_DB` and a user named `'50043_DB'@'localhost'`. If not, the script creates the database and user. The script will also give the user full permissions to the `50043_DB` database. After which, the script runs `initialize.sql` with the generated user credentials. `initialize.sql` imports the contents from `kindle_reviews.csv` into a table called `reviews` inside the `50043_DB` database.

## Quality of life improvements
* [SSH Keys and Github](https://dev.to/maedahbatool/generating-a-new-ssh-key-and-adding-it-to-github-137j)

## MySQL
* If required, start server using:
* sudo service mysql start

## MongoDB
* default location to view log files from mongodb: `/var/log/mongodb/mongodb.log`
* start mongod as a background process (allows you to use mongodb command line interface): `sudo service mongodb start`

### Database commands
* create DB: `use <db_name>`
* show databases: `show databases` (database with no collections not shown)

### Collections commands
* show collections for current db: `show collections`
* create collection: 
    * `db.createCollection('<collection_name>')`
    * `db.<collection_name>.insert({<json_object>})`
* list objects in a collection: `db.<collection_name>.find()`

### PyMongo material
* [Introduction to mongodb and python](https://realpython.com/introduction-to-mongodb-and-python/)

### Web Server Logging
* Logging is automatically done every 5 seconds, and stored in models/bookreviews.log

### Data analytics with Pandas and Apache Spark
* Amazon Kindle Reviews Dataset
    * Pandas + Scikit-Learn
        * Pearson correlation: price vs review length
        * TF-IDF 
            * Review sentiment analysis
            * Find similar reviews
            * Extract review keywords
    * Apache Spark
        * Install and setup
        * Raw csv/json -> Spark DataFrames
        * Run SQL queries from python
        
* [Colab Notebook](https://colab.research.google.com/drive/1j9WC5OVgnXZ1-h82Yk6B4BRYtKCJxYTp)

## FAQs:
#### 1. MySQL seem to have issues for me after git pulling. What happened?

If you just ran the code, you need to set the environment variables.
Look at the instructions again for the set up. 

If it is still not working, the column tables may have changed.
Delete the .py files in migrations/versions and rerun MySQL migration 
set up again
