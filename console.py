#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg):
    curled = re.search(r"\{(.*?)\}", arg)
    braces = re.search(r"\[(.*?)\]", arg)
    if curled is None:
        if braces is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lex = split(arg[:braces.span()[0]])
            output = [i.strip(",") for i in lex]
            output.append(braces.group())
            return output
    else:
        lex = split(arg[:curled.span()[0]])
        output = [i.strip(",") for i in lex]
        output.append(curled.group())
        return output


class HBNBCommand(cmd.Cmd):
    """Console entry point.
    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass

    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        dict_args = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            lst_arg = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", lst_arg[1])
            if match is not None:
                command = [lst_arg[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in dict_args.keys():
                    call = "{} {}".format(lst_arg[0], command[1])
                    return dict_args[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, arg):
        """Usage: create <class>
        Create a new class instance and print its id.
        """
        lst_arg = parse(arg)
        if len(lst_arg) == 0:
            print("** class name missing **")
        elif lst_arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(lst_arg[0])().id)
            storage.save()

    def do_show(self, arg):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        lst_arg = parse(arg)
        dict_ojb = storage.all()
        if len(lst_arg) == 0:
            print("** class name missing **")
        elif lst_arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(lst_arg) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(lst_arg[0], lst_arg[1]) not in dict_ojb:
            print("** no instance found **")
        else:
            print(dict_ojb["{}.{}".format(lst_arg[0], lst_arg[1])])

    def do_destroy(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id."""
        lst_arg = parse(arg)
        dict_ojb = storage.all()
        if len(lst_arg) == 0:
            print("** class name missing **")
        elif lst_arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(lst_arg) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(lst_arg[0], lst_arg[1]) not in dict_ojb.keys():
            print("** no instance found **")
        else:
            del dict_ojb["{}.{}".format(lst_arg[0], lst_arg[1])]
            storage.save()

    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""

        lst_arg = parse(arg)
        if len(lst_arg) > 0 and lst_arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            list_objects = []
            for obj in storage.all().values():
                if len(lst_arg) > 0 and lst_arg[0] == obj.__class__.__name__:
                    list_objects.append(obj.__str__())
                elif len(lst_arg) == 0:
                    list_objects.append(obj.__str__())
            print(list_objects)

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""

        lst_arg = parse(arg)
        count = 0
        for obj in storage.all().values():
            if lst_arg[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value>"""

        lst_arg = parse(arg)
        dict_ojb = storage.all()

        if len(lst_arg) == 0:
            print("** class name missing **")
            return False
        if lst_arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(lst_arg) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(lst_arg[0], lst_arg[1]) not in dict_ojb.keys():
            print("** no instance found **")
            return False
        if len(lst_arg) == 2:
            print("** attribute name missing **")
            return False
        if len(lst_arg) == 3:
            try:
                type(eval(lst_arg[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(lst_arg) == 4:
            obj = dict_ojb["{}.{}".format(lst_arg[0], lst_arg[1])]
            if lst_arg[2] in obj.__class__.__dict__.keys():
                value_type = type(obj.__class__.__dict__[lst_arg[2]])
                obj.__dict__[lst_arg[2]] = value_type(lst_arg[3])
            else:
                obj.__dict__[lst_arg[2]] = lst_arg[3]
        elif type(eval(lst_arg[2])) == dict:
            obj = dict_ojb["{}.{}".format(lst_arg[0], lst_arg[1])]
            for k, v in eval(lst_arg[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    value_type = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = value_type(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()    
