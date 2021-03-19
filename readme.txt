INSTRUCTIONS

Make sure you have python3, if not please run on Mac or required command for other OS: 
brew install python3

Create a virtual environment. Run the following command
python3 -m venv guild_env

Activate the virtual environment:
Source guild_env/bin/activate
pip install flask
A sqlite DB is placed inside the project guild_education/api
The name of the DB is messages.db
To access the DB please use command: sqlite3 messages.db

I have only created one table inside the DB called messages which serves our purpose. See schema below. 
We are going to use epoch timestamp for message sent time.
CREATE TABLE MESSAGES(
   SENDER_ID INTEGER  NOT NULL,
   RECIPIENT_ID INTEGER NOT NULL,
   MESSAGE   TEXT NOT NULL,
   DATETIME  INTEGER  NOT NULL 
);

All the api code is in api.py and some helper functions are located in utils.py. I have used "?" Instead of string format or replacements in the queries to prevent sql injection

To run the server:

cd /guild_education/api
python api.py

You will see a server running on http://127.0.0.1:5000/

APIs
----


Send a message:
---------------

On your terminal 

curl "http://127.0.0.1:5000/api/send/" -H "Content-Type: application/json" --data  '{"sender_id":"1","recipient_id":"3","message":"Ho ho ho" }' -X POST

This is a post call

If using browser please send post params using postman

Recipient and sender ids cannot be the same else a 400 error is thrown
If successful, a json with message success will be returned


All messages from all senders:
------------------------------

On your terminal 

curl "http://127.0.0.1:5000/api/messages/all?limit=true" 

curl "http://127.0.0.1:5000/api/messages/all?thirty_days=true" 

Or directly paste the url in the browser

This is a get call 

You either have to give limit or thirty_days as request param. The value can be set to anything. 
If both are given, limit will be used. If none are given a 400 error will be thrown with an error message
If successful, a json with list of all required messages will be returned 




All messages from a sender to a recipient:
-------------------------------------------

curl "http://127.0.0.1:5000/api/messages/?recipient_id=2&sender_id=1&limit=true" 

curl "http://127.0.0.1:5000/api/messages/?recipient_id=2&sender_id=1&thirty_days=true" 


Or directly paste the url in the browser

You either have to give limit or thirty_days as request param. The value can be set to anything. 
If both are given, limit will be used. If none are given a 400 error will be thrown with an error message
If recipient_id or sender_id or message is not sent. 400 error will be thrown
If successful, a json with list of all required messages will be returned.


