#!/usr/bin/env python3
"""HBNBCommand Class.

Command line for airbnb
"""
import cmd
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class HBNBCommand(cmd.Cmd):
    """shows methods and attributes of console"""

    prompt = "(hbnb) "

    models = ("Amenity", "BaseModel", "City", "Place", "Review", "State", "User")

    def do_quit(self, arg):
        """Quit command"""
        return True

    def do_EOF(self, arg):
        """Exits the program"""
        return True

    def emptyline(self):
        # Overrides the default and repeats prev command
        return False

    def do_create(self, arg):
        """Creates a new instance of a class, saves it and prints the id"""
        error = HBNBCommand.HBNBCommand_error_handler(arg)
        if error:
            return

        obj = eval(arg)()
        obj.save()
        print(obj.id)

    def do_show(self, arg):
        """Prints the str rep of an obj based on the class
        name and id

        """
        error = HBNBCommand.HBNBCommand_error_handler(arg, command="show")
        if error:
            return

        arg = arg.split()
        objs = storage.all()
        key = f"{arg[0]}.{arg[1]}"
        object = objs.get(key)
        if object:
            print(object)
        else:
            print("** no instance found **")

    def do_destroy(self, arg):
        """Deletes an object in relation to name nd id"""
        error = HBNBCommand.HBNBCommand_error_handler(arg, command="destroy")

        if error:
            return

        arg = arg.split()
        key = f"{arg[0]}.{arg[1]}"
        objs = storage.all()
        if key in objs and storage.delete(objs[key]):
            pass
        else:
            print("** no instance found **")

    def do_all(self, arg):
        """returns str rep of all objs based on or not
        the class_name

        """
        error = HBNBCommand.HBNBCommand_error_handler(arg, command="all")

        if error:
            return

        arg = arg.split(" ")
        objs = storage.all()
        if arg[0] == "":
            for object in objs.values():
                print(object)
        else:
            for key in objs:
                obj_key = key.split(".")
                if obj_key[0] == arg[0]:
                    print(objs[key])

    def do_update(self, arg):
        """Updates the name or id based on the attributes availble or new ones

        """
        error = HBNBCommand.HBNBCommand_error_handler(arg, command="update")

        if error:
            return

        arg = arg.split()
        cl_name = arg[0]
        obj_id = arg[1]

        objs = storage.all()
        key = f"{cl_name}.{obj_id}"

        arg_len = len(arg) - 1
        for obj_key in objs:
            if obj_key == key:
                object = objs[obj_key]
                for count in range(2, arg_len):
                    attr_name = arg[count]
                    attr_value = arg[count + 1]
                    if '"' in attr_value:
                        attr_value = attr_value[1:-1]

                    if attr_value.isdigit():
                        attr_value = int(attr_value)

                    setattr(object, attr_name, attr_value)

                object.save()
                return

        print("** no instance found **")

    def do_count(self, arg):
        """Returns the number of objs available based on class_name"""
        error = HBNBCommand.HBNBCommand_error_handler(arg)

        if error:
            return

        count = 0
        arg = arg.split()
        objs = storage.all()
        key = arg[0]

        for object in objs:
            if key in object:
                count += 1

        print(count)

    def precmd(self, arg):
        if "." in arg:
            arg_string = (
                arg.replace(".", " ")
                .replace(", ", " ")
                .replace("(", " ")
                .replace(")", " ")
                .replace('"', "")
                .replace("{", "")
                .replace("}", "")
                .replace("'", "")
                .replace(":", "")
            )
            arg_string = arg_string.split()
            arg_string[0], arg_string[1] = arg_string[1], arg_string[0]
            arg = " ".join(arg_string)

        return super().precmd(arg)

    def onecmd(self, args):
        if args == "quit":
            return self.do_quit(args)
        elif args == "EOF":
            return self.do_EOF(args)
        else:
            return cmd.Cmd.onecmd(self, args)

    @classmethod
    def HBNBCommand_error_handler(cls, arg, **kwargs):
        if "all" in kwargs.values():
            if not arg:
                return False

        if not arg:
            print("** class name missing **")
            return True
        else:
            arg = arg.split()

        number_of_command_arg = len(arg)

        if arg[0] not in HBNBCommand.models:
            print("** class doesn't exist **")
            return True

        if "command" not in kwargs:
            return False

        for command_arg in kwargs.values():
            if command_arg in ["show", "destroy"]:
                if number_of_command_arg < 2:
                    print("** instance id missing **")
                    return True

            if command_arg == "update":
                if number_of_command_arg < 2:
                    print("** instance id missing **")
                    return True
                elif number_of_command_arg < 3:
                    print("** attribute name missing **")
                    return True
                elif number_of_command_arg < 4:
                    print("** value missing **")
                    return True

        return False


if __name__ == "__main__":
    HBNBCommand().cmdloop()
