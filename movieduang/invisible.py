#!/usr/bin/env python3
import moviepy.editor as mp
import argparse
import numpy as np


def color_diff(rgb1, rgb2):
    (r1, g1, b1), (r2, g2, b2) = rgb1, rgb2
    d = abs(r1-r2) + abs(g1-g2) + abs(b1-b2)
    return d / 3


def parser_color(c) -> (int, int, int):
    if len(c) == 2:
        c = int(c, 0x10)
        return c, c, c
    elif len(c) == 3:
        r, g, b = list(map(lambda x: int(x, 0x10), [c[0]*2, c[1]*2, c[2]*2]))
        return r, g, b
    elif len(c) == 6:
        r, g, b = list(map(lambda x: int(x, 0x10), [c[:2], c[2:4], c[4:]]))
        return r, g, b


def get_filter(background_image, diff, target_color):

    def f(image):
        shape = image.shape
        image = np.copy(image)
        color_array = np.full(shape, target_color)
        direct_diff = abs(color_array-image)
        diff_array = direct_diff.sum(axis=2) / 3
        pos_array = diff_array <= diff
        image[pos_array, :] = 0
        complement = np.copy(background_image)
        complement[~pos_array, :] = 0
        return image+complement
    return f


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--color", '-c', help='mask color', default="0F0")  # green
    parser.add_argument("--diff", '-d', help='diff between color and target color', type=int, default=16)
    parser.add_argument("--picture", '-p', help='background image', default=None)
    parser.add_argument("--output", '-o', help='output path', default='output.mp4')
    parser.add_argument("--input", '-i', help='input video')
    args = parser.parse_args(argv)

    movie = mp.VideoFileClip(args.input)
    r, g, b = parser_color(args.color)
    if args.picture is None:
        img = movie.get_frame(0)
    else:
        img = mp.ImageClip(args.picture).get_frame(0)
    new_movie = movie.fl_image(get_filter(img, args.diff, (r, g, b)))
    new_movie.write_videofile(args.output)


if __name__ == '__main__':
    main()
