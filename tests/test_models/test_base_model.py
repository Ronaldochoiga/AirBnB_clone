#!/usr/bin/env python3
"""Unittest base_model module.

Test cases for base_model class and methods documentation and instances.
"""
import inspect
import pycodestyle
import time
import unittest
from models import base_model
from datetime import datetime
from unittest import mock


BaseModel = base_model.BaseModel


class TestBaseModelDocs(unittest.TestCase):
    """Class for testing BaseModel docs"""

    @classmethod
    def setUpClass(self):
        """Set up for docstring tests"""
        self.base_funcs = inspect.getmembers(BaseModel, inspect.isfunction)

    def test_pycodestyle_conformance(self):
        """... pycodestyle conformance"""
        for path in [
                     'tests/test_models/test_base_model.py']:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 3)

    def test_doc_file(self):
        """... documentation for the file"""
        doc = base_model.__doc__
        self.assertIsNotNone(doc, "base_model.py needs a docstring")

    def test_doc_class(self):
        """... documentation for the class"""
        doc = BaseModel.__doc__
        self.assertIsNotNone(doc, "BaseModel class needs a docstring")

    def test_doc_init(self):
        """... documentation for class functions"""
        for func in self.base_funcs:
            with self.subTest(function=func):
                self.assertIsNot(
                    func[1].__doc__,
                    None,
                    "{:s} method needs a docstring".format(func[0])
                )
                self.assertTrue(
                    len(func[1].__doc__) > 1,
                    "{:s} method needs a docstring".format(func[0])
                )


class TestBaseModel(unittest.TestCase):
    """Class for testing BaseModel class"""

    def test_instantiation(self):
        """... checks if BaseModel is properly instantiated"""
        inst = BaseModel()
        self.assertIs(type(inst), BaseModel)
        inst.name = "Alx"
        inst.number = 89
        attrs_types = {
            "id": str,
            "created_at": datetime,
            "updated_at": datetime,
            "name": str,
            "number": int
        }
        for attr, typ in attrs_types.items():
            with self.subTest(attr=attr, typ=typ):
                self.assertIn(attr, inst.__dict__)
                self.assertIs(type(inst.__dict__[attr]), typ)
        self.assertEqual(inst.name, "Alx")
        self.assertEqual(inst.number, 89)

    def test_datetime_attributes(self):
        """... checks if two BaseModel instances have different datetime"""
        tic = datetime.now()
        instance1 = BaseModel()
        toc = datetime.now()
        self.assertTrue(tic <= instance1.created_at <= toc)
        time.sleep(1e-4)
        tic = datetime.now()
        instance2 = BaseModel()
        toc = datetime.now()
        self.assertTrue(tic <= instance2.created_at <= toc)
        self.assertEqual(instance1.created_at, instance1.updated_at)
        self.assertEqual(instance2.created_at, instance2.updated_at)
        self.assertNotEqual(instance1.created_at, instance2.created_at)
        self.assertNotEqual(instance1.updated_at, instance2.updated_at)

    def test_uuid(self):
        """... uuid should be valid"""
        instance1 = BaseModel()
        instance2 = BaseModel()
        for inst in [instance1, instance2]:
            uuid = inst.id
            with self.subTest(uuid=uuid):
                self.assertIs(type(uuid), str)
                self.assertRegex(uuid,
                                 '^[0-9a-f]{8}-[0-9a-f]{4}'
                                 '-[0-9a-f]{4}-[0-9a-f]{4}'
                                 '-[0-9a-f]{12}$')
        self.assertNotEqual(instance1.id, instance2.id)

    def test_to_dict(self):
        """... checks if BaseModel is properly casted to dictionary"""
        my_mod = BaseModel()
        my_mod.name = "Alx"
        my_mod.my_number = 89
        d = my_mod.to_dict()
        exp_attrs = ["id",
                          "created_at",
                          "updated_at",
                          "name",
                          "my_number",
                          "__class__"]
        self.assertCountEqual(d.keys(), exp_attrs)
        self.assertEqual(d['__class__'], 'BaseModel')
        self.assertEqual(d['name'], "Alx")
        self.assertEqual(d['my_number'], 89)

    def test_to_dict_values(self):
        """test that val in dict returned from to_dict are correct"""
        tme_format = "%Y-%m-%dT%H:%M:%S.%f"
        bm = BaseModel()
        new_d = bm.to_dict()
        self.assertEqual(new_d["__class__"], "BaseModel")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], bm.created_at.strftime(tme_format))
        self.assertEqual(new_d["updated_at"], bm.updated_at.strftime(tme_format))

    def test_str(self):
        """test that the str  has the correct output"""
        inst = BaseModel()
        string = "[BaseModel] ({}) {}".format(inst.id, inst.__dict__)
        self.assertEqual(string, str(inst))

    @mock.patch('models.storage')
    def test_save(self, mock_storage):
        """Test that save method updates `updated_at` and calls
        `storage.save`"""
        inst = BaseModel()
        old_created_at = inst.created_at
        old_updated_at = inst.updated_at
        inst.save()
        new_created_at = inst.created_at
        new_updated_at = inst.updated_at
        self.assertNotEqual(old_updated_at, new_updated_at)
        self.assertEqual(old_created_at, new_created_at)
        self.assertTrue(mock_storage.new.called)
        self.assertTrue(mock_storage.save.called)


if __name__ == "__main__":
    unittest.main()
