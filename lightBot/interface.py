#!/usr/bin/env python3

#Author: Cameron Haddock
#Last Modified: 9 September 2019
#Purpose of File: 
# Used to establish times that the stepper motor will not be activatable

import sqlite3

#Determine if time is a valid time
def valid_time(time):
  if ':' not in time:
    return False
  split = time.split(':')
  if len(split) != 2:
    return False
  try:
    hour = int(split[0])
    minute = int(split[1])
  except:
    return False
  if not 1 <= hour <= 24 or not 0 <= minute <= 59:
    return False

  return True

#Determine if time is on a valid day
def valid_days(time):
  days = "MTWHFSU"
  for day in time:
    if day not in days:
      return False
  for day in time:
    if time.count(day) > 1:
      return False
  return True

#Pointless function to pad left with spaces. Theres a library function for this
def pad_spaces(string,length):
  string = ' ' + string
  while(len(string) < length):
    string = string + ' '
  return string

#Return all rules matching the name, or all if no name is given
def get_all(cur,match):
  if match == '':
    request = """SELECT name,start,end,days,desc FROM rules;"""
    cur.execute(request)
  else:
    request = """SELECT name,start,end,days,desc FROM rules WHERE name=?;"""
    cur.execute(request,(match,))
  rules = cur.fetchall()
  return rules;

#Print all rows in given rows as rules
def print_all(rows):
  print('Existing Rules:\n\n    Name        | Start        | End        | Days        | Description')
  print('    -------------------------------------------------------------------')
  for rule in rows:
    print('   ',end='')
    print(pad_spaces(str(rule[0]),13) + '|',end='')
    print(pad_spaces(str(rule[1]),14) + '|',end='')
    print(pad_spaces(str(rule[2]),12) + '|',end='')
    print(pad_spaces(str(rule[3]),13) + '|',end='')
    print(' ' + rule[4])


def main():
  while True:
    switch = input('Enter 1 to view rules\nEnter 2 to enter new rule\nEnter 3 to delete existing rule\nEnter 4 to exit\n')
    conn = sqlite3.connect('/home/pi/LUCSMACL/lightBot/bot.db')
    cur = conn.cursor()

    if(switch == '4' or switch == 'q' or switch == 'quit' or switch == 'exit'):
      break;
    elif(switch == '1'):
      print('\n')
      print_all(get_all(cur,''))

    elif(switch == '2'):
      while True:
        print('\n\nInput new rule')
        print('Type quit in any cell to exit')
        #insert
        
        print('Input name for new rule: ',end = '')
        name = input()
        if name == 'quit':
          break
        if not (len(name) > 0):
          print("Name must not be blank")
          continue

        print('Input start time for new rule (Ex. 13:30): ',end='')
        start = input()
        if start == 'quit':
          break
        if not valid_time(start):
          print("Start time incorrectly formatted")
          continue
        
        print('Input end time for new rule (Ex. 14:45): ', end='')
        end = input()
        if end == 'quit':
          break
        if not valid_time(end):
          print("End time incorrectly formatted")
          continue
        
        print('Input days for new rule (Ex. MWF, Ex. WH): ', end='')
        days = input()
        if days == 'quit':
          break      
        if not valid_days(days):
          print("Listed days invalid")
          continue

        print('Input description: ', end='')
        desc = input()
        if desc == 'quit':
          break
        if not (len(desc) > 0):
          print("Must input a description")
          continue


        #insert
        insert = """INSERT INTO rules(name,start,end,days,desc) VALUES (?,?,?,?,?);"""
        cur.execute(insert,(name,start,end,days,desc))
        conn.commit()

        #view
        print_all(get_all(cur,name))
        break

    elif(switch == '3'):
      print('\n\nDelete new rule')
      print_all(get_all(cur,''))
      while True:
        print('Input name of rule to delete: ',end = '')
        name = input()
        if len(name) == 0:
          print('Enter valid name')
          continue
        rows = get_all(cur,name)
        if len(rows) == 0:
          print('No current rule exists by that name\n')
          continue

        print_all(rows)
        verify = input('Are you sure you want to delete these rules? ');
        if verify not in ['yes','y','true']:
          break

        delete = """DELETE FROM rules WHERE name = ?;"""
        cur.execute(delete,(name,))
        conn.commit()
        print_all(get_all(cur,''))
        break

    else:
      print('Invalid input\n')
    conn.close()
    print('\n\n\n')

if __name__ == '__main__':
  main();
