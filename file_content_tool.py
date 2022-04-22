#!/usr/bin/python3
'''
  Скрипт для комментирования, раскоментирования строк в файлах Script for comment/uncomment/add/delete lines in file
  file_path - path to file
  active_line - working line
  operation - operation with file (com, uncom, del, add) - (comment, uncomment, add, delete)
'''
from sys import argv,exc_info,exit,stderr,stdout
from os import path
def main():
  ARGUMENTS_LIST = {
      "file_path" : "system path to file",
      "operation" : "del - delete; add - adding; com - comment; uncom - uncomment",
      "line" : "which line you want to modify"
  }

  ARGUMENTS_COUNT = len(ARGUMENTS_LIST)

  OPERATIONS_FUNCTIONS_LIST = {
      "del" : "delete_line",
      "add" : "add_line",
      "com" : "comment_line",
      "uncom" : "uncomment_line"
  }

  OPERATIONS_FUNCTIONS_COUNT = len(OPERATIONS_FUNCTIONS_LIST)

  if len(argv) < ARGUMENTS_COUNT:
    stderr.write("You need to enter {} arguments:\n".format(ARGUMENTS_COUNT))
    for key,value in ARGUMENTS_LIST.items():
      stderr.write("{0}. {1} - {2}\n".format(
        list(ARGUMENTS_LIST.keys()).index(key) + 1,
        key,
        value
      ))
    exit(1)
  
  operation_succes = False

  args = argv[1:]
  file_path = args[0]
  operation = args[1]
  active_line = args[2]

  if not path.isfile(file_path):
    stderr.write("File \"{}\" doesn't exists\n".format(file_path))
    exit(1)


  if operation not in list(OPERATIONS_FUNCTIONS_LIST.keys()):
    stderr.write("Wrong operation \"{0}\". There are only {1} operations:\n".format(
      operation,
      OPERATIONS_FUNCTIONS_COUNT
    ))
    for key,value in OPERATIONS_FUNCTIONS_LIST.items():
      stderr.write("{0}. {1} - {2}\n".format(
        list(OPERATIONS_FUNCTIONS_LIST.keys()).index(key) + 1,
        key,
        value
      ))
    exit(1)

  try:
    if operation == "add":
      with open(file_path, 'a') as file:
        add_line(file, active_line)
        operation_succes = True
    else:
      active_line = '#'+active_line if operation=="uncom" else active_line
      active_line_len = len(active_line)
      new_file = []
      with open(file_path, 'r') as file:
        for line in file:
          if line[0:active_line_len] == active_line:
            line = locals()[OPERATIONS_FUNCTIONS_LIST[operation]](line)
            operation_succes = True
          new_file.append(line)
      with open(file_path, 'w') as file:
        for line in new_file:
          file.write(line)
  except Exception:
    e = exc_info()[1]
    stderr.write("The was error:\n {}\n".format(e))
    exit(1)

  if not operation_succes:
    stdout.write("Nothing changed, there was problem\n".format(file_path, active_line))
    exit(0)

stdout.write("Scripts worked succesful\n")

def delete_line(line):
    return ''

def add_line(file, line):
    file.write('\n' + line + '\n')

def comment_line(line):
    return '#'+line

def uncomment_line(line):
    return line[1:]

if __name__ == '__main__':
    main()
