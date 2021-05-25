#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
import sys
import pandas as pd
import psycopg2

params_dic = {
    "database" : "dataset_lda", 
    "user" : "postgres", 
    "password" : "masukcepetP19", 
    "host" : "127.0.0.1", 
    "port" : "5432"}

path_data = 'C:/Users/Zukkiii_/Youtube Comments Mining/Data/'

class connection:
    def connect(params_dic):
            con = None
            try:
                print('Connecting to the PostgreSQL database...')
                con = psycopg2.connect(**params_dic)
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
                sys.exit(1)


            print('Connection successful')
            return con

class database:    
    def createTableScraping():
        con = connection.connect(params_dic)
        cur = con.cursor()

        cur.execute('''CREATE TABLE YOUTUBE_COMMENTS
          (NAMA_USER    TEXT,
          COMMENTS_USER  TEXT,
          VIDEO_TITLE   TEXT,
          CHANNEL       TEXT,
          VIEWS         INT,
          POSTED        DATE);''')
        print("Table created successfully")
        con.commit()
        con.close()
        
    def intoDatabaseScraping(playlist):
        con = connection.connect(params_dic)
        cur = con.cursor()
        with open(path_data + 'scraping_youtube_%s.csv' % playlist,'r', encoding = "UTF-8") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                cur.execute(
                "INSERT INTO YOUTUBE_COMMENTS VALUES (%s, %s, %s, %s, %s, %s)",
                row
            )
        print("Load to database successfully")
        con.commit()
        con.close()
        
    def postgresql_to_dataframe(con, select_query, column_names):
        cursor = con.cursor()
        try:
            cursor.execute(select_query)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            cursor.close()
            return 1

        tupple = cursor.fetchall()
        cursor.close()

        df = pd.DataFrame(tupple, columns=column_names)
        return df
    
    def createTableDatabasePreprocessing():
        con = connection.connect(params_dic)
        cur = con.cursor()

        cur.execute('''CREATE TABLE COMMENTS_PREPROCESSING
          (DOCUMENT_NO    INT,
          USER_NAME    TEXT,
          COMMENTS_USER  TEXT,
          VIDEO_TITLE   TEXT,
          CHANNEL       TEXT,
          VIEWS         INT,
          POSTED        DATE,
          COMMENTS_CLEAN            TEXT,
          COMMENTS_TOKENIZE         TEXT,
          COMMENTS_SLANGWORD        TEXT,
          COMMENTS_STEMMED          TEXT,
          COMMENTS_STOPWORDS        TEXT,
          TEXT_STRING               TEXT);''')
        print("Table created successfully")
        con.commit()
        con.close()
    
    def intoDatabasePreprocessing():
        con = connection.connect(params_dic)
        cur = con.cursor()
        with open(path_data + 'youtube_comments_preprocessing.csv','r', encoding = "UTF-8") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                cur.execute(
                "INSERT INTO COMMENTS_PREPROCESSING VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                row
            )
        con.commit()
        con.close()
        
    def createTableDatabaseTD():
        con = connection.connect(params_dic)
        cur = con.cursor()

        cur.execute('''CREATE TABLE YOUTUBE_COMMENTS_TOPICS_DISTRIBUTION
          (Document_No         INT,
          Dominant_Topic       REAL,
          Topic_Perc_Contrib   REAL,
          Keywords             TEXT,
          Text                 TEXT);''')
        print("Table created successfully")
        con.commit()
        con.close()
        
    def intoDatabaseTD():
        con = connection.connect(params_dic)
        cur = con.cursor()
        with open(path_data + 'Distribution Topics Result.csv','r', encoding = "UTF-8") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                cur.execute(
                "INSERT INTO YOUTUBE_COMMENTS_TOPICS_DISTRIBUTION VALUES (%s, %s, %s, %s, %s)",
                row
            )
        con.commit()
        con.close()

