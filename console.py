#!/usr/bin/python3
"""This is the console for AirBnB"""
import cmd
import shlex
import json
import re
from ast import literal_eval
from models import storage
from datetime import datetime
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from shlex import split


class HBNBCommand(cmd.Cmd):
    """this class is entry point of the command interpreter
    """
    prompt = "(hbnb) "
    all_classes = {"BaseModel": BaseModel, "User": User, "State": State,
                   "City": City, "Amenity": Amenity, "Place": Place,
                   "Review": Review}

    def emptyline(self):
        """Ignores empty spaces"""
        pass

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, line):
        """Quit command to exit the program at end of file"""
        return True

    def do_create(self, line):
        """Creates a new instance of BaseModel, saves it
        Exceptions:
            SyntaxError: when there is no args given
            NameError: when there is no object that has the name
        """
        try:
            if not line:
                raise SyntaxError()
            # my_list = line.split(" ")
            # if len(my_list) > 1:
            #     cls = my_list.pop(0)
            #     obj = eval("{}({})".format(cls, temp3))
            # else:
            #     obj = eval("{}()".format(my_list[0]))

            # parser = shlex.shlex(line, posix=True)
            # parser.whitespace_split = True
            # token = " "
            # arg_list = []
            # tok_list = []
            # cls = parser.get_token()
            # while token is not None:
            #     token = parser.get_token()
            #     tok_list.append(token)
            # del tok_list[-1]
            # print(tok_list)
            # for arg in tok_list:
            #     arg_list.append(arg.split('=')[0])
            # for arg in tok_list:
            #     arg_list.append(arg.split('=')[1])
            #     temp = literal_eval(arg_list[0])

            parser = shlex.shlex(line, posix=True)
            parser.whitespace_split = True
            token = " "
            tok_list = []
            tup_list = []
            to_parse = {}
            sanitized_args = {}
            cls = parser.get_token()
            while token is not None:
                token = parser.get_token()
                tok_list.append(token)
            for tup in tok_list:
                if tup is not None:
                    tup_list.append(tup.partition('='))
            for tuple_item in tup_list:
                to_parse[tuple_item[0]] = tuple_item[2]
            for k, v in to_parse.items():

                # Matches string beginnig with 1 or more alphanum
                # followed and ended by _id
                if re.match("^\w+_id$", k):
                    sanitized_args[k] = v

                # Matches string that could be starting with + or -,
                # followed by 1 to any amount of numbers
                # followed by  a '.'
                # followed by and anding with 1 to any amount of numbers
                elif re.match("^[-+]?\d+\.\d+$", v):
                    sanitized_args[k] = float(v)
                elif v.isdigit() is True:
                    sanitized_args[k] = int(v)
                else:
                    if '_' in v:
                        sanitized_args[k] = v.replace('_', ' ')
                    else:
                        sanitized_args[k] = v
            obj = HBNBCommand.all_classes[cls](**sanitized_args)
            obj.save()
            print("{}".format(obj.id))
        except SyntaxError:
            print("** class name missing **")
        except KeyError:
            print("** class doesn't exist **")

    def do_show(self, line):
        """Prints the string representation of an instance
        Exceptions:
            SyntaxError: when there is no args given
            NameError: when there is no object taht has the name
            IndexError: when there is no id given
            KeyError: when there is no valid id given
        """
        try:
            if not line:
                raise SyntaxError()
            my_list = line.split(" ")
            if my_list[0] not in self.all_classes:
                raise NameError()
            if len(my_list) < 2:
                raise IndexError()
            objects = storage.all()
            key = my_list[0] + '.' + my_list[1]
            if key in objects:
                print(objects[key])
            else:
                raise KeyError()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id
        Exceptions:
            SyntaxError: when there is no args given
            NameError: when there is no object taht has the name
            IndexError: when there is no id given
            KeyError: when there is no valid id given
        """
        try:
            if not line:
                raise SyntaxError()
            my_list = line.split(" ")
            if my_list[0] not in self.all_classes:
                raise NameError()
            if len(my_list) < 2:
                raise IndexError()
            objects = storage.all()
            key = my_list[0] + '.' + my_list[1]
            if key in objects:
                del objects[key]
                storage.save()
            else:
                raise KeyError()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")

    def do_all(self, line):
        """Prints all string representation of all instances
        Exceptions:
            NameError: when there is no object taht has the name
        """

        my_list = []
        if not line:
            objects = storage.all()
            for key in objects:
                my_list.append(objects[key])
            print(my_list)
            return
        try:
            args = line.split(" ")
            if args[0] not in self.all_classes:
                raise NameError()
            objects = storage.all(args[0])
            for value in objects.values():
                my_list.append(value)
            print(my_list)
        except NameError:
            print("** class doesn't exist **")

    def do_update(self, line):
        """Updates an instanceby adding or updating attribute
        Exceptions:
            SyntaxError: when there is no args given
            NameError: when there is no object taht has the name
            IndexError: when there is no id given
            KeyError: when there is no valid id given
            AttributeError: when there is no attribute given
            ValueError: when there is no value given
        """
        try:
            if not line:
                raise SyntaxError()
            my_list = split(line, " ")
            if my_list[0] not in self.all_classes:
                raise NameError()
            if len(my_list) < 2:
                raise IndexError()
            objects = storage.all()
            key = my_list[0] + '.' + my_list[1]
            if key not in objects:
                raise KeyError()
            if len(my_list) < 3:
                raise AttributeError()
            if len(my_list) < 4:
                raise ValueError()
            v = objects[key]
            try:
                v.__dict__[my_list[2]] = eval(my_list[3])
            except Exception:
                v.__dict__[my_list[2]] = my_list[3]
                v.save()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")
        except AttributeError:
            print("** attribute name missing **")
        except ValueError:
            print("** value missing **")

    def count(self, line):
        """count the number of instances of a class
        """
        counter = 0
        try:
            my_list = split(line, " ")
            if my_list[0] not in self.all_classes:
                raise NameError()
            objects = storage.all()
            for key in objects:
                name = key.split('.')
                if name[0] == my_list[0]:
                    counter += 1
            print(counter)
        except NameError:
            print("** class doesn't exist **")

    def strip_clean(self, args):
        """strips the argument and return a string of command
        Args:
            args: input list of args
        Return:
            returns string of argumetns
        """
        new_list = []
        new_list.append(args[0])
        try:
            my_dict = eval(
                args[1][args[1].find('{'):args[1].find('}')+1])
        except Exception:
            my_dict = None
        if isinstance(my_dict, dict):
            new_str = args[1][args[1].find('(')+1:args[1].find(')')]
            new_list.append(((new_str.split(", "))[0]).strip('"'))
            new_list.append(my_dict)
            return new_list
        new_str = args[1][args[1].find('(')+1:args[1].find(')')]
        new_list.append(" ".join(new_str.split(", ")))
        return " ".join(i for i in new_list)

    def default(self, line):
        """retrieve all instances of a class and
        retrieve the number of instances
        """
        my_list = line.split('.')
        if len(my_list) >= 2:
            if my_list[1] == "all()":
                self.do_all(my_list[0])
            elif my_list[1] == "count()":
                self.count(my_list[0])
            elif my_list[1][:4] == "show":
                self.do_show(self.strip_clean(my_list))
            elif my_list[1][:7] == "destroy":
                self.do_destroy(self.strip_clean(my_list))
            elif my_list[1][:6] == "update":
                args = self.strip_clean(my_list)
                if isinstance(args, list):
                    obj = storage.all()
                    key = args[0] + ' ' + args[1]
                    for k, v in args[2].items():
                        self.do_update(key + ' "{}" "{}"'.format(k, v))
                else:
                    self.do_update(args)
        else:
            cmd.Cmd.default(self, line)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
