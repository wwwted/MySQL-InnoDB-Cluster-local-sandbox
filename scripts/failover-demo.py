

import mysql.connector
from mysql.connector import errorcode

import time
import sys

conn=None

def add_employee(conn, emp_no, first_name, last_name):
    try:
       cur = conn.cursor()
       cur.execute(
          "INSERT INTO employees VALUES (%s, %s, %s)",
          (emp_no, first_name, last_name)
       )
    except mysql.connector.Error: 
       print "Database connection error, trying to reconnect ..." 
       connect() 

def find_employee(conn, emp_no):
    try:
       cur = conn.cursor()
       cur.execute(
           "SELECT concat('Hostname:',@@hostname),concat(': ',@@port,' ; '), first_name, last_name FROM employees "
           "WHERE emp_no = %s", (emp_no, )
       )
       for row in cur:
           print row[0],row[1],row[2],row[3]
    except mysql.connector.Error: 
       print "Database connection error, trying to reconnect ..." 
       connect() 

def connect():
   global conn
   print "inside  connect()"
   try:
       conn=mysql.connector.connect(user="root", password="root", database="test", port=sys.argv[1], host="127.0.0.1", autocommit=True)

   except mysql.connector.Error as err: 
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
          print("Something is wrong with your user name or password")
          sys.exit()
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
          print("Database does not exist")
          sys.exit()
      else:
          print(err)

      print "Error trying to get a new database connection"
      time.sleep(1)
   return conn

if len(sys.argv) != 2:
   print "Syntax: ", sys.argv[0], "<port> exiting ...."
   sys.exit()

print "Starting to insert data into MySQL on port:", sys.argv[1]

connect()
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS employees")
cur.execute(
    "CREATE TABLE employees ("
    "   emp_no INT PRIMARY KEY, "
    "   first_name CHAR(40), "
    "   last_name CHAR(40)"
    ")"
    )

high=10
for x in range(0, high):
   add_employee(conn, x, "John"+":"+str(x), "Doe")

high+=1
while True:
   add_employee(conn, high, "John"+":"+str(high), "Doe")
   time.sleep(0.5)
   for x in range(high-5, high):
      find_employee(conn, x)
   high+=1


