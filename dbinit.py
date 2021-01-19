import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
            """
            CREATE TABLE IF NOT EXISTS Users (
            UserID SERIAL PRIMARY KEY,
            Name VARCHAR(40) NOT NULL,
            Surname VARCHAR(40) NOT NULL,
            Email VARCHAR(80) NOT NULL UNIQUE,
            Password VARCHAR(100) NOT NULL,
            Register_Time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            Photo VARCHAR(255),
            City VARCHAR(80) NOT NULL,
            Account NUMERIC DEFAULT 0.0
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS Types (
            TypeID SERIAL PRIMARY KEY,
            Type VARCHAR(120) NOT NULL,
            Max_Pr INTEGER NOT NULL CHECK (Max_Pr > 0),
            Min_Pr INTEGER DEFAULT 0
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS Brands (
            Br_ID SERIAL PRIMARY KEY,
            TypeID INTEGER REFERENCES Types (TypeID),
            Br_Name VARCHAR(255) NOT NULL,
            Email VARCHAR(80),
            Address VARCHAR(80),
            TELEPHONE VARCHAR(15) NOT NULL UNIQUE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS Requests (
            Req_ID SERIAL PRIMARY KEY,
            UserID INTEGER REFERENCES Users (UserID),
            Req_Time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            Br_ID INTEGER REFERENCES Brands (Br_ID),
            Req_Name VARCHAR(120) NOT NULL,
            Amount NUMERIC NOT NULL CHECK (Amount > 0),
            Report INTEGER DEFAULT 0,
            IS_Paid BOOLEAN DEFAULT '0',
            Code VARCHAR(40)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS Donations (
            Donor_ID SERIAL PRIMARY KEY,
            UserID INTEGER REFERENCES Users (UserID),
            Dnt_Time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            Req_ID INTEGER REFERENCES Requests (Req_ID),
            D_Note TEXT
            )
            """
]

def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = "postgres://vahbelka:oXTNFzp-WxAaS-pvu50bh9dhGxBp4kjl@otto.db.elephantsql.com:5432/vahbelka"
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)