#!/usr/bin/python3
"""Documentation for Review Class"""
from models.base_model import BaseModel


class Review(BaseModel):
    """Defines the Review Class"""
    place_id = ""
    user_id = ""
    text = ""
