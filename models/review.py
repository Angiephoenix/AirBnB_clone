#!/usr/bin/python3
"""module for class Reviews"""

from models.base_model import BaseModel


class Review(BaseModel):
    """child class for BaseModel"""
    place_id = ""
    user_id = ""
    text = ""
