#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import psycopg2

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

