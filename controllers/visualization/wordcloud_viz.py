"""
Masked wordcloud
================
Using a mask you can generate wordclouds in arbitrary shapes.
"""

from os import path, pardir
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import random

from wordcloud import WordCloud, STOPWORDS
from palettable.colorbrewer.sequential import Reds_9, Greens_9, Blues_9, Greys_9

import pandas as pd

directory = path.dirname(__file__)


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


def which_masks(source):

    if source == "default":
        return np.array(Image.open(path.join(directory, "masks", "cloud.png")))
    elif source == "candidate":
        return np.array(Image.open(path.join(directory, "masks", "user.png")))
    elif source == "positive":
        return np.array(Image.open(path.join(directory, "masks", "thumbs-up.png")))
    elif source == "neutral":
        return np.array(Image.open(path.join(directory, "masks", "thumbs-down.png")))
    elif source == "negative":
        return np.array(Image.open(path.join(directory, "masks", "meh-o.png")))


def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return tuple(Reds_9.colors[random.randint(2,8)])


def which_color(source):
    if source == "default":
        return tuple(Greys_9.colors[random.randint(2, 8)])
    elif source == "positive":
        return tuple(Greens_9.colors[random.randint(2, 8)])
    elif source == "neutral":
        return tuple(Blues_9.colors[random.randint(2, 8)])
    elif source == "negative":
        return tuple(Reds_9.colors[random.randint(2, 8)])


def word_cloud(source, text):
    ngram_freq = dict((x, y) for x, y in text.items())

    #  loads the mask for the cloud shape to be used
    mask = which_masks(source)

    #  initialize the word cloud
    wc = WordCloud(background_color="black", mask=mask, height=800, width=800, max_font_size=1000)

    # generate word cloud
    # wc.generate(text)
    wc.generate_from_frequencies(frequencies=ngram_freq)
    wc.recolor(color_func=which_color(source), random_state=3)

    # store to file
    static_folder = path.join(directory, pardir, pardir, "static", "img")
    print(static_folder)
    wc.to_file(path.join(static_folder, "word_cloud.png"))

    # show
    # plt.figure(figsize=(7, 5), facecolor='k')
    # plt.imshow(wc, interpolation='bilinear')
    # plt.axis("off")
    # plt.tight_layout(pad=0)
    # plt.annotate("BANANA", xy=(0, -.025), xycoords='axes fraction', fontsize=20, color='white')
    # plt.show()

# word_cloud()




