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
    cur_braces = re.search(r"\{(.*?)\}", arg)
    brack = re.search(r"\[(.*?)\]", arg)
    if cur_braces is None:
        if brack is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brack.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brack.group())
            return retl
    else:
        lexer = split(arg[:cur_braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(cur_braces.group())
        return retl


class HBNBCommand(cmd.Cmd):
    """Defines the HBnB command interpreter.
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
        """Do nothing on empty line."""
        pass

    def default(self, arg):
        """normal behavior for cmd module for invalide"""
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        mat = re.search(r"\.", arg)
        if mat is not None:
            arg0 = [arg[:mat.span()[0]], arg[mat.span()[1]:]]
            mat = re.search(r"\((.*?)\)", arg0[1])
            if mat is not None:
                command = [arg0[1][:mat.span()[0]], mat.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(arg0[0], command[1])
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to quit the program."""
        print("")
        return True

    def do_create(self, arg):
        """Usage: create class
        Create a new class instance and print its id.
        """
        arg0 = parse(arg)
        if len(arg0) == 0:
            print("** class name missing **")
        elif arg0[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(arg0[0])().id)
            storage.save()

    def do_show(self, arg):
        """Usage: show classes and id as well as name.
        Display the string rep of a class inst of a given id.
        """
        arg0 = parse(arg)
        obj_dict = storage.all()
        if len(arg0) == 0:
            print("** class name missing **")
        elif arg0[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg0) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg0[0], arg0[1]) not in obj_dict:
            print("** no instance found **")
        else:
            print(obj_dict["{}.{}".format(arg0[0], arg0[1])])

    def do_destroy(self, arg):
        """Usage: destroy class or id
        Delete a class inst of a given id."""
        arg0 = parse(arg)
        obj_dict = storage.all()
        if len(arg0) == 0:
            print("** class name missing **")
        elif arg0[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg0) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg0[0], arg0[1]) not in obj_dict.keys():
            print("** no instance found **")
        else:
            del obj_dict["{}.{}".format(arg0[0], arg0[1])]
            storage.save()

    def do_all(self, arg):
        """Usage: all classes displayed
        Display string repr of all inst of a given class.
        when class is not specified, displays all objects."""
        arg0 = parse(arg)
        if len(arg0) > 0 and arg0[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objl = []
            for obj in storage.all().values():
                if len(arg0) > 0 and arg0[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(arg0) == 0:
                    objl.append(obj.__str__())
            print(objl)

    def do_count(self, arg):
        """Usage: count
        display the number of inst of a given class."""
        arg0 = parse(arg)
        count = 0
        for obj in storage.all().values():
            if arg0[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, arg):
        """Usage: update attributes eg class,time,name id and city
        Update a class inst of a given id by adding or updating
        a given att key or value pair or dict."""
        arg0 = parse(arg)
        obj_dict = storage.all()

        if len(arg0) == 0:
            print("** class name missing **")
            return False
        if arg0[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(arg0) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(arg0[0], arg0[1]) not in obj_dict.keys():
            print("** no instance found **")
            return False
        if len(arg0) == 2:
            print("** attribute name missing **")
            return False
        if len(arg0) == 3:
            try:
                type(eval(arg0[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(arg0) == 4:
            obj = obj_dict["{}.{}".format(arg0[0], arg0[1])]
            if arg0[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[arg0[2]])
                obj.__dict__[arg0[2]] = valtype(arg0[3])
            else:
                obj.__dict__[arg0[2]] = arg0[3]
        elif type(eval(arg0[2])) == dict:
            obj = obj_dict["{}.{}".format(arg0[0], arg0[1])]
            for k, v in eval(arg0[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
