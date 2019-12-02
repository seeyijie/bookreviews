# 50.043 Database Project

## Automation script
The automation script is located in `boto3/master.sh`. It launches 4 EC2 instances and installs mysql, mongodb, flask and react on them. Text files and shell script files will be generated on your local machine. After deployment, follow the link generated in the command line. This will take you to our home page. Enjoy!


**NOTE:** 
* Please make sure you have a good internet connection when you try and run the automation scripts.
* if you see the warning `ssh connection refused`, let the script continue to run. It should eventually add the IP address of the particular server into your `~/.ssh/known_hosts` file.

### Prerequisite python3 libraries
* boto3
* fire
    * installed by `pip3 install fire`

### Other dependencies
* openssh-server
* openssh-client

### Expected output
``` 
******** mongodb server info ********
new instance: i-0fa186cd7f0b2cf7e
3.17.147.142
50043-keypair
2019-12-01 08:41:58+00:00

******** mysql server info ********
new instance: i-08c8538f85bc6fdd8
13.58.110.71
50043-keypair
2019-12-01 08:42:31+00:00

******** flask server info ********
new instance: i-0d1bfb6d1616d1551
3.15.160.61
50043-keypair
2019-12-01 08:43:04+00:00

******** react server info ********
new instance: i-0520729e7b669ed40
3.15.154.165
50043-keypair
2019-12-01 08:43:37+00:00
Server deployment done. Checking status of mysql.
Checking server status: (NOTE: ignore warnings for connection refused)
Warning: Permanently added '13.58.110.71' (ECDSA) to the list of known hosts.
```

## General Instructions for Group members (How to run):
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

## Quality of life improvements
* [SSH Keys and Github](https://dev.to/maedahbatool/generating-a-new-ssh-key-and-adding-it-to-github-137j)

## React (How to run)
* Prerequisites:
   * Install `yarn`. If yarn is not working, try upgrading NodeJS to the latest version.
   * Go to `/bookreviews/react-end` and run `yarn install` to install react dependencies from the `package.json` file.
* Run`yarn start` and go to `localhost:3000`

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
* Every route in flask needs to call logger.logrequest(request, response) just before each return statement
* All requests and their responses will be logged onto /log

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


#### 2. Backend Queries:
endpt:localhost:5000/api/addbook
</br>body:
```
{"asin":"969627171717","salesRank":"hoho","title":
	"meme stuff","categories":["ha","aa"],"description":"blabla", "price":12, "related":{"also_bought":["B123444","1231233"],"also_viewed":["B233321321"],"bought_together":["Be12321"]},"imUrl":"https://urlme.me/success/typed_a_url/made_a_meme.jpg?source=www"
}
```

response: 
```
{
    "added": "true"
}
{
    "added": "false"
}
```
endpt: localhost:5000/api/addreview
body:
```
{
    "summary":"review",
    "asin":"B000ZC8DPM",
    "reviewerName":"myname",
    "reviewerID":"myID",
    "reviewText":"this is a review",
}
```
response: 
```
{
    "added": "true"
}
{
    "added": "false"
}
```
book detail endpoint: localhost:5000/api/books/1603420304

response:
```{
    "book_metadata": {
        "asin": "1603420304",
        "categories": [
            [
                "Books",
                "Cookbooks, Food & Wine",
                "Quick & Easy"
            ],
            [
                "Books",
                "Cookbooks, Food & Wine",
                "Special Diet"
            ],
            [
                "Books",
                "Cookbooks, Food & Wine",
                "Vegetarian & Vegan",
                "Non-Vegan Vegetarian"
            ],
            [
                "Kindle Store",
                "Kindle eBooks",
                "Cookbooks, Food & Wine",
                "Quick & Easy"
            ],
            [
                "Kindle Store",
                "Kindle eBooks",
                "Cookbooks, Food & Wine",
                "Special Diet",
                "Healthy"
            ],
            [
                "Kindle Store",
                "Kindle eBooks",
                "Cookbooks, Food & Wine",
                "Vegetables & Vegetarian"
            ]
        ],
        "description": "In less time and for less money than it takes to order pizza, you can make it yourself!Three harried but heatlh-conscious college students compiled and tested this collection of more than 200 tasty, hearty, inexpensive recipes anyone can cook -- yes, anyone!Whether you're short on cash, fearful of fat, counting your calories, or just miss home cooking, The Healthy College Cookbook offers everything you need to make good food yourself.",
        "imUrl": "http://ecx.images-amazon.com/images/I/51IEqPrF%2B9L._BO2,204,203,200_PIsitb-sticker-v3-big,TopRight,0,-55_SX278_SY278_PIkin4,BottomRight,1,22_AA300_SH20_OU01_.jpg",
        "price": 7.69,
        "related": {
            "also_viewed": [
                "B001OLRKLQ",
                "B004J35JIC",
                "B00505UP8M",
                "B004GTLKEQ",
                "B005KWMS8U",
                "B00BS03TYU",
                "B001MT5NXW",
                "B00A86JE3K",
                "B00D694Y9U",
                "B00DSVUVXY",
            ],
            "buy_after_viewing": [
                "B004J35JIC",
                "B0089LOJH2"
            ]
        },
        "salesRank": null,
        "title": "classic and with 300 the healthy quick college easy cookbook"
    },
    "related_url": {
        "also_viewed": [
            [
                "B0041KKLNQ",
                "http://ecx.images-amazon.com/images/I/51YnsnUU0nL._BO2,204,203,200_PIsitb-sticker-v3-big,TopRight,0,-55_SX278_SY278_PIkin4,BottomRight,1,22_AA300_SH20_OU01_.jpg"
            ],
            [
                "B008161J1O",
                "http://ecx.images-amazon.com/images/I/51-uyKRenVL._BO2,204,203,200_PIsitb-sticker-v3-big,TopRight,0,-55_SX278_SY278_PIkin4,BottomRight,1,22_AA300_SH20_OU01_.jpg"
            ],
            [
                "B008EN3W6Y",
                "http://ecx.images-amazon.com/images/I/51NhzCPoRBL._BO2,204,203,200_PIsitb-sticker-v3-big,TopRight,0,-55_SX278_SY278_PIkin4,BottomRight,1,22_AA300_SH20_OU01_.jpg"
            ],
            [
                "B00C5W32QK",
                "http://ecx.images-amazon.com/images/I/51y6WX3JPoL._BO2,204,203,200_PIsitb-sticker-v3-big,TopRight,0,-55_SX278_SY278_PIkin4,BottomRight,1,22_AA300_SH20_OU01_.jpg"
            ],
            [
                "B00C89GS1Q",
                "http://ecx.images-amazon.com/images/I/51NScvtwPzL._BO2,204,203,200_PIsitb-sticker-v3-big,TopRight,0,-55_SX278_SY278_PIkin4,BottomRight,1,22_AA300_SH20_OU01_.jpg"
            ],
            [
                "B00CTVOVD0",
                "http://ecx.images-amazon.com/images/I/51PMpMZJ7ML._BO2,204,203,200_PIsitb-sticker-v3-big,TopRight,0,-55_SX278_SY278_PIkin4,BottomRight,1,22_AA300_SH20_OU01_.jpg"
            ],
            [
                "B00D694Y9U",
                "http://ecx.images-amazon.com/images/I/519LrNNNw4L._BO2,204,203,200_PIsitb-sticker-v3-big,TopRight,0,-55_SX278_SY278_PIkin4,BottomRight,1,22_AA300_SH20_OU01_.jpg"
            ],
            [
                "B00DSVUVXY",
                "http://ecx.images-amazon.com/images/I/51nLWH0P-fL._BO2,204,203,200_PIsitb-sticker-v3-big,TopRight,0,-55_SX278_SY278_PIkin4,BottomRight,1,22_AA300_SH20_OU01_.jpg"
            ],
            [
                "B00ET594CC",
                "http://ecx.images-amazon.com/images/I/51f55uR2HhL._BO2,204,203,200_PIsitb-sticker-v3-big,TopRight,0,-55_SX278_SY278_PIkin4,BottomRight,1,22_AA300_SH20_OU01_.jpg"
            ],
            [
                "B00HY0KTPK",
                "http://ecx.images-amazon.com/images/I/51LY8qZY9vL._BO2,204,203,200_PIsitb-sticker-v3-big,TopRight,0,-55_SX278_SY278_PIkin4,BottomRight,1,22_AA300_SH20_OU01_.jpg"
            ]
        ],
        "buy_after_viewing": []
    }
}
```

book reviews endpoint: localhost:5000/api/books/B000F83SZQ/reviews

response:
```
{
    "reviews": [
        {
            "asin": "B000F83SZQ",
            "helpful": "[1, 1]",
            "id": 7,
            "overall": 4,
            "reviewText": "Never heard of Amy Brewster. But I don't need to like Amy Brewster to like this book. Actually, Amy Brewster is a side kick in this story, who added mystery to the story not the one resolved it. The story brings back the old times, simple life, simple peo",
            "reviewTime": "2014-03-22",
            "reviewerID": "A3DE6XGZ2EPADS",
            "reviewerName": "WPY",
            "summary": "Enjoyable reading and reminding the old times",
            "unixReviewTime": 1395446400
        },
        {
            "asin": "B000F83SZQ",
            "helpful": "[0, 0]",
            "id": 6,
            "overall": 4,
            "reviewText": "I enjoyed this one tho I'm not sure why it's called An Amy Brewster Mystery as she's not in it very much. It was clean, well written and the characters well drawn.",
            "reviewTime": "2014-06-10",
            "reviewerID": "A2HSAKHC3IBRE6",
            "reviewerName": "Wolfmist",
            "summary": "Nice old fashioned story",
            "unixReviewTime": 1402358400
        },
	...
    ]
}
```
