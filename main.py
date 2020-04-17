"""
main.py
Simple file for showing a data class with methods for writing and reading it from a json file

Author: Kyle Anderson
Date: April 16, 2020
"""

import json
import pandas as pd


class Data:
    """
     Dummy data class

    Can be written to json and read back in

    """

    def __init__(self, df: pd.DataFrame, name: str, color: str, shape: str):
        self.df = df
        self.shape = shape
        self.name = name
        self.color = color

    def to_json(self, filename: str):
        """
        to_json Write Data object to a json file


        Arguments:
            filename {str} -- self-explanatory
        """

        dict_to_write = self.__dict__.copy()
        dict_to_write["df"] = dict_to_write["df"].to_json()
        with open(filename, "w") as file:
            json.dump(dict_to_write, file)

    @classmethod
    def from_json(cls, filename: str) -> "Data":
        """
        from_json - Class method to create a new Data object from a json file

        usage: my_data = Data.from_json("my_data.json")

        Arguments:
            filename {str}

        Returns:
            Data -- New Data object
        """
        with open(filename, "r") as file:
            dict_read = json.load(file)

        dict_read["df"] = pd.read_json(dict_read["df"])

        return cls(**dict_read)

    def __eq__(self, other):
        if (
            (self.df == other.df).all().all()
            and (self.shape == other.shape)
            and (self.name == other.name)
            and (self.color == other.color)
        ):
            return True
        else:
            return False


if __name__ == "__main__":

    import random

    N = 10
    X = random.choices(range(100), k=N)
    # pylint:disable=invalid-name
    test_df = pd.DataFrame(
        {
            "time": range(0, N),
            "data": random.choices(range(100), k=N),
            "estimate": random.choices(range(100), k=N),
        }
    )

    my_data = Data(test_df, "Module1", "GREEN", "SQUARE")

    my_data.to_json("test_data.json")

    my_read_data = Data.from_json("test_data.json")

    assert my_data == my_read_data
