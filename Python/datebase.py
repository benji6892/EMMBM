""" takes as input the number of days since block 1 was mined (row index in our
 data base) and returns the corresponding date (as a date or string type).
 Day 0 -> 09/01/2009; 1 -> 10/01/2009 ...
 The last function does the opposite. Takes a date as input and gives
 the corresponding number in the database.
"""

from datetime import *

def date_base(j):

     return date(year=2009, month=1, day=9)+timedelta(days=j)

def date_str(j):
  
     j=date_base(j)
     m=j.month
     if m<10:
          m=str(0)+str(m)
     else:
          m=str(m)
     d=j.day
     if d<10:
          d=str(0)+str(d)
     else:
          d=str(d)
     return str(j.year)+'-'+m+'-'+d


def string_to_database(datestring):
     # datestring: YYYY-MM-DD
    diff = date(int(datestring[:4]), int(datestring[5:7]), int(datestring[8:10]))\
           - date(year=2009, month=1, day=9)
    return diff.days

