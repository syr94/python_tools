#/usr/bin/python3

'''
Script which compares version of installed package and argument

'''
from sys import argv,exit, stderr, stdout, exc_info
from os import  popen

def main():
  PACKAGE_GET_LIST = {
      "memcached" : "get_memcached_version"
  }


  ARGUMENTS_LIST = {
      "package_name" : "name of package",
      "operation" : "operation with value get/compare(needs third numeric argument return True if given argument greater \
        than current version, False if not)"
  }

  ARGUMENTS_COUNT = len(ARGUMENTS_LIST)

  if len(argv) < ARGUMENTS_COUNT:
    stderr.write("You need to enter {} arguments:\n".format(ARGUMENTS_COUNT))
    for key,value in ARGUMENTS_LIST.items():
      stderr.write("{0}. {1} - {2}\n".format(
        list(ARGUMENTS_LIST.keys()).index(key) + 1,
        key,
        value
      ))
    exit(1)

  args = argv[1:]

  package_name = args[0]
  operation = args[1]

  if package_name not in list(PACKAGE_GET_LIST.keys()):
    stderr.write("Wrong package name \"{}\". Only following package enabled:\n".format(package_name))
    for key in PACKAGE_GET_LIST:
      stderr.write("{0}. {1}\n".format(
        list(PACKAGE_GET_LIST.keys()).index(key) + 1,
        key
      ))
    exit(1)

  if operation == "compare":
    try:
      version = args[2]
      compare_version = compare_versions(
        version,
        globals()[PACKAGE_GET_LIST[package_name]]()
        )
      stdout.write(str(compare_version).lower())
    except ValueError:
      stderr.write("Wrong argument \"{}\": for compare\n".format(version))
      exit(1)
    except Exception:
      e = exc_info()[1]
      stderr.write("The was problem while compare:\n {}\n".format(e))
      exit(1)

  if operation == "get":
    try:
      package_version = globals()[PACKAGE_GET_LIST[package_name]]()
      stdout.write(str(package_version))
    except KeyError:
      stderr.write("The package {} not installed!\n".format(package_name))
    except Exception:
      e = exc_info()[1]
      stderr.write("The was problem while compare:\n {}\n".format(e))
      exit(1)

'''
Возвращает версию memcached установленную в системе
''' 
def get_memcached_version():
    package_version = popen("memcached -V").read().split()[1]
    return package_version

'''
Сравнивает версии переданной аргументом и установленной у пакета
'''
def compare_versions(argument_version, current_version):
    result = False
    argument_version_splitted = argument_version.split('.')
    current_version_splitted = current_version.split('.')
    count_arguments = min(len(argument_version_splitted), len(current_version_splitted))
    for index in range(0, count_arguments):
      if int(argument_version_splitted[index]) > int(current_version_splitted[index]):
        result = True
        break
    return result

if __name__ == '__main__':
    main()
