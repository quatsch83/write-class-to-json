"""
main.py
Simple file for showing a data class with methods for writing and reading it from a json file

Author: Kyle Anderson
Date: April 16, 2020
"""

import json
import numpy as np
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
        dict_to_write = {
            "df": self.df.to_json(),
            "shape": self.shape,
            "name": self.name,
            "color": self.color,
        }
        with open(filename, "w") as file:
            json.dump(dict_to_write, file)

    @classmethod
    def from_json(cls, filename: str) -> cls:
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
        return cls(
            pd.read_json(dict_read["df"]),
            dict_read["name"],
            dict_read["color"],
            dict_read["shape"],
        )

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

    np.random.seed(0)
    x = np.random.randint(0, 10000, 1000)

    COLORS = ["red", "blue", "green", "yellow", "purple"]
    SHAPES = ["square", "triangle", "circle", "line", "hexagon"]
    N = 10
    DF = pd.DataFrame(
        {
            "time": range(0, N),
            "data": np.random.randint(0, 10000, N),
            "estimate": np.random.randint(0, 10000, N),
        }
    )

    my_data = Data(DF, "Module1", "GREEN", "SQUARE")

    print(my_data.df)

    my_data.to_json("test_data.json")

    my_read_data = Data.from_json("test_data.json")

    print(my_read_data.df)

    # IPython.embed_kernel()

    assert my_data == my_read_data
