#!/usr/bin/env python3
import moviepy.editor as mp
import os
import argparse


def process_one(video_path, logo_path, output_path):
    video = mp.VideoFileClip(video_path)
    logo_h = logo_w = video.h // 8
    logo_margin_x = logo_h // 3
    logo = (
        mp.
        ImageClip(logo_path).
        set_duration(video.duration).
        resize(width=logo_w, height=logo_h).
        margin(right=logo_margin_x, top=logo_margin_x, opacity=0).
        set_pos(("right", "top"))
    )

    final = mp.CompositeVideoClip([video, logo])
    final.write_videofile(output_path)


def output_file_name(file_path, output_path):
    return os.path.join(output_path, os.path.basename(file_path))


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--logo", '-l', help='logo path')
    parser.add_argument("--output", '-o', help='output path', default='.')
    parser.add_argument("movies", nargs='+', help='move path')
    args = parser.parse_args(argv)

    n = len(args.movies)
    for i, one in enumerate(args.movies):
        print("%d, %.2f%%" % (i + 1, i / n * 100), one)
        process_one(one, args.logo, output_file_name(one, args.output))


if __name__ == '__main__':
    main()
