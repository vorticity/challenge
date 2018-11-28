Prerequisites
=============
- export MONGO_URI=...
- virtualenv ve
- source ve/bin/activate
- pip install -r requirements.txt

Scraper Instructions
====================
- cd insentia
- scrapy crawl insentia

API Instructions
================
- python application.py

Example Search Queries
======================
- http://127.0.0.1:5000/api/challenge-v1/search?include=hug&exclude=cheese
- http://127.0.0.1:5000/api/challenge-v1/search?include=hug
- http://127.0.0.1:5000/api/challenge-v1/search?include=isentia&exclude=zuckerberg+females

Swagger URL
===========
- http://127.0.0.1:5000

API Limitations
===============
- Currently using mongodb text indexing feature for keyword search
- Currently flattening results of mongodb cursor to a list
- Search terms are AND not OR

Future Work
===========
- SSL connection to database
- Sorting search results by relevance (textScore)
- Support pagination in search endpoint
- Unit & integration tests
- Logging