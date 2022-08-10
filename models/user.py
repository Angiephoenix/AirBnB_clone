#!/usr/bin/python3

#!/usr/bin/python3
"""module for class User"""

from models.base_model import BaseModel


class User(BaseModel):
    """Child class of BaseModel"""

    email = ""
    password = ""
    first_name = ""
    last_name = ""

    def __init__(self, *args, **kwargs):
        """Initializing User"""
        super().__init__(self, *args, **kwargs)
