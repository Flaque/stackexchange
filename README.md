# stackexchange
A data science project to answer the question: "How do you write a good answer to a question?"

## Setup

### Python Installs
1. Install Spacy:
```pip install -U spacy ```

2. Install the Spacy English Language Model:
```python -m spacy.en.download all```

### Setting up XML files
1. Extract as many stackexchanges as you want [from this archive](https://archive.org/details/stackexchange). Put the `xyz.stackexchange.com` folders into a single folder and call it
what you want.
2. In `populate_database.py`, change `DATA_FOLDER` to be your filename.

### Database
1. Setup a mysql instance with a database called `stackexchange`.
2. Edit `toMySQL.py` variables `host`, `user`, and `database` near the top of
the file to represent your database credentials.
3. Run the `createDatabase.sql` file to create the tables in your database. If you're using something like SequelPro (pancakes), you can press `cmd-shift-i` to import an sql file.
4. If you have all your XML and database stuff setup correctly, you should be able to run `python populate_database.py` and it will fill
your database with the extracted features.
