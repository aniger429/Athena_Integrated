"""
Masked wordcloud
================
Using a mask you can generate wordclouds in arbitrary shapes.
"""

import random
from os import path, pardir

import numpy as np
import pandas as pd
from PIL import Image
from palettable.colorbrewer.sequential import Reds_9, Greens_9, Blues_9, Greys_9
from wordcloud import WordCloud

directory = path.dirname(__file__)
SOURCE = ""


def read_xlsx(filename):
    return pd.read_excel(filename, encoding='utf-8', keep_default_na=False)


def transparent_to_white():
    viz_list = ["cloud", 'frown-o', 'meh-o', 'smile-o', 'thumbs-down', 'thumbs-up', 'twitter', 'user']
    source = "/home/dudegrim/Documents/scratch/exported/"
    dest = "/home/dudegrim/Documents/scratch/1080/"
    for v in viz_list:
        print(v)
        im = Image.open(source+v+".png")

        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, im)
        bg.save(dest+v+".png")


def which_masks():
    if SOURCE == "candidate":
        return np.array(Image.open(path.join(directory, "masks", "user.png")))
    elif SOURCE == "positive":
        return np.array(Image.open(path.join(directory, "masks", "thumbs-up.png")))
    elif SOURCE == "neutral":
        return np.array(Image.open(path.join(directory, "masks", "thumbs-down.png")))
    elif SOURCE == "negative":
        return np.array(Image.open(path.join(directory, "masks", "meh-o.png")))
    else:
        return np.array(Image.open(path.join(directory, "masks", "cloud.png")))


def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return tuple(Reds_9.colors[random.randint(2, 8)])


def which_color(word, font_size, position, orientation, random_state=None, **kwargs):
    if SOURCE == "positive":
        return tuple(Greens_9.colors[random.randint(2, 8)])
    elif SOURCE == "neutral":
        return tuple(Blues_9.colors[random.randint(2, 8)])
    elif SOURCE == "negative":
        return tuple(Reds_9.colors[random.randint(2, 8)])
    else:
        return tuple(Greys_9.colors[random.randint(2, 8)])


def word_cloud(source, text):
    ngram_freq = dict((x, y) for x, y in text.items())
    SOURCE = source

    #  loads the mask for the cloud shape to be used
    mask = which_masks()

    #  initialize the word cloud
    wc = WordCloud(background_color="black", mask=mask, height=700, width=500, max_font_size=1000)

    # generate word cloud
    # wc.generate(text)
    wc.generate_from_frequencies(frequencies=ngram_freq)
    wc.recolor(color_func=which_color, random_state=3)


    # store to file
    static_folder = path.join(directory, pardir)
    wc.to_file(path.join(static_folder, "word_cloud.png"), )

    return path.join(static_folder, "word_cloud.png")


