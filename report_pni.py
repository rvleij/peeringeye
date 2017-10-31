#!/usr/bin/python

from peeringdb import PeeringDB
import json
import MySQLdb
pdb = PeeringDB()

conn = MySQLdb.connect(host="localhost", user="", passwd="", db="")
dbcursor = conn.cursor()
counter = 0
total_cap = 0

dbcursor.execute("DROP TABLE IF EXISTS IX")
sql = """CREATE TABLE IX (
         ID VARCHAR(100),  
         IX_ID VARCHAR(20),
         IX_CITY VARCHAR(50),
         IX_COUNTRY VARCHAR(100),
         IX_NAME VARCHAR(100),
         REAL_SPEED VARCHAR(10),
         NICE_SPEED VARCHAR(10))"""
dbcursor.execute(sql)

dbcursor.execute("DROP TABLE IF EXISTS SUMMARY")
sql = """CREATE TABLE SUMMARY (
         CAPACITY VARCHAR(10),
         PEERINGS VARCHAR(10),
         FACILITIES VARCHAR(10))"""
dbcursor.execute(sql)

net = pdb.type_wrap('net')

response = net.all(id=1956,depth=2)

for i in response[0]['netixlan_set']:
  counter = counter+1
  speed = (i['speed'] / 1000)
  total_cap = total_cap + speed
  nice_speed = "%s G" %(speed)

  try:
    dbcursor.execute("""INSERT INTO IX values (%s,%s,%s,%s,%s,%s,%s)""",(counter,i['ix_id'],0,0,0,speed,nice_speed))
    conn.commit()
  except:
    print "meh, db failure first step"
    conn.rollback()

total_cap = total_cap / 1000

try:
  dbcursor.execute("""SELECT count(DISTINCT IX_ID) FROM IX""")
  total_fac = dbcursor.fetchall()
  dbcursor.execute("""SELECT count(*) FROM IX""")
  total_peerings = dbcursor.fetchall()
except:
  print "meh, db failure on totals"
  conn.rollback()

print "total facilities: %s" %total_fac[0]
print "total cap: %s" %total_cap
print "total peerings: %s" %total_peerings

try:
  dbcursor.execute("""INSERT INTO SUMMARY values (%s,%s,%s)""",(total_cap,total_peerings,total_fac))
except:
  print "meh, db failure on total insertion"
  conn.rollback()

try:
  dbcursor.execute("""SELECT DISTINCT IX_ID FROM IX""")
except:
  print "meh, db failure on IX selection"
  conn.rollback()

ix = pdb.type_wrap('ix')

for j in dbcursor:
  ix_query="%s"%j 
  ixname = ix.get(ix_query)
  print "IX Name : %s processed" %(ixname[0]['name'])
  sql_query = """UPDATE IX SET IX_NAME=%s, IX_CITY=%s, IX_COUNTRY=%s WHERE IX_ID=%s"""
  try:
    dbcursor.execute(sql_query, (ixname[0]['name'],ixname[0]['city'],ixname[0]['country'],j))
    conn.commit()
  except:
    print "meh, db failure third step"
    conn.rollback()

dbcursor.close()
conn.close()
    
