#!/usr/bin/python3

"""module for class City"""

from models.base_model import BaseModel


class City(BaseModel):
    """child class for BaseModel"""
    state_id = ""
    name = ""
