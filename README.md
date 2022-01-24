# jasmine
The aim of this project is to obtain a trend on the bitcoin price using the various tweets on the subject. 
To do this, you need to have access to the tweeter APIs and put the keys and tokens in the file src/services/credentials.py

To retrieve the tweets for the test set we cannot use the api and the search_full_archive functionality directly as it is paid for and highly limited.
In a first step we will try to retrieve the most influential users in the bitcoin sector. 
Then we will retrieve the timeline of the users, the twitter api limits us to 3000 items including tweets, rt and quote.