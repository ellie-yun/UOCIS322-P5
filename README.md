# UOCIS322 - Project 5 #
> **Author: Ellie Yun, yyun@uoregon.edu**

Brevet time calculator with AJAX and MongoDB!

## Overview

Connect a Flask app to MongoDB, and then store control times from Project 4 in the database by clicking the `Submit` button and display the most recent stored submit result by clicking the `Display` button in the ACP calculator page.


## How to run the application?

1. Select the brevet distance and beginning data & time in the ACP calculator page.

2. Type in a number on either `Miles` or `Km` for each row. You will be able to type in total 20 rows.

3. Click one of the following buttons:
    - Upon clicking the `Submit` button, the control times should be inserted into a MongoDB database.    
        `Note: Every time the button is clicked, the data stored in the database will be cleared so that the database can contain the most recent submission of the control times.`
        
        `Note: Need to fill in at least one row in order to press the submit button.`
        
    - Upon clicking the `Display` button, the entries from the database should be displayed in a new page.
        
        `Note: If you click the Display button before submitting any control times, the redirected page will point it out and ask you to go back and submit something.`

## Test

An automated `nose` test suite with some test cases for the time calculator and for DB insertion and retrieval.

For the purpose of unit testing, the operations of database are implemented separately on `db.py`. `Mongodb` class will be used to create a connection to the database, setting the database, inserting the row, retrieving all the rows in the collection, and deleting all the rows in the collection.

## Credits

Michal Young, Ram Durairajan, Steven Walton, Joe Istas.
