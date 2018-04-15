import os
from src import generate_model


data_dir = '../data'


def main():
    try:
        with open(os.path.join(data_dir, 'numerator.json'))