import ffmpeg
import os
import sys

#vestigial cli args
#platform = sys.argv[1]
#media_file = sys.argv[2]

path = os.getcwd()

##list must be platform:get_video_codec
##e.g.  "youtube:vp9"
formatlist_file = path + os.path.sep + 'flist.txt'

##list of codec:libraries
codeclist_file = path + os.path.sep + 'clist.txt'

##list of platform|aspect ratios
##key|value is pipe delim and ratios may be comma sep
ratiolist_file = path + os.path.sep + 'rlist.txt'

codec_dict = {}

with open(codeclist_file, 'r') as c:
    for line in c.readlines():
        codec_item = line.strip()
        key,value = codec_item.split(':',1)
        codec_dict[key] = value

def get_video_dar(media):
    streams = ffmpeg.probe(media)["streams"]

    stream = next((stream for stream in streams if stream['codec_type'] == 'video'), None)

    if stream:
        if 'display_aspect_ratio' in stream:
            return "dar", stream['display_aspect_ratio']
        else:
            return "w:h", f"{stream['width']}:{stream['height']}"
    else:
        return None, "None"

def closest(list, current):
    return list[min(range(len(list)), key = lambda i: abs(list[i]-current))]

def pp_dar_mod(platform,media_file):
    ratiolist_dict = {}
    try:
        with open(ratiolist_file, 'r') as r:
            for line in r.readlines():
                ratio_item = line.strip()
                key,value = ratio_item.split('|',1)
                ratiolist_dict[key] = value

        if not platform in ratiolist_dict:
            raise Exception(f"No valid ratios for {platform} in file 'rlist.txt'")

        med_ratio_type, med_ratio = get_video_dar(media_file)

        if not med_ratio_type:
            raise Exception(f"No video stream in {media_file}")

        if med_ratio in ratiolist_dict[platform]:
            print(f"{media_file} already in appropriate DAR for {platform}")
        else:
            ratios_list = []
            ratios_dict = {}
            for ratio in ratiolist_dict[platform].split(','):
                width,height = ratio.split(':')
                dec_ratio = int(width) / int(height)
                ratios_list.append(dec_ratio)
                ratios_dict[dec_ratio] = ratio

            med_width, med_height = med_ratio.split(':')
            med_dec_ratio = int(med_width) / int(med_height)
            target_dec_ratio = closest(ratios_list, med_dec_ratio)
            target_ratio = ratios_dict[target_dec_ratio]

            if med_dec_ratio == target_dec_ratio:
                print(f"{media_file} already in appropriate DAR for {platform}")
            else:
                print(f"Converting file to {target_ratio}")

                (
                ffmpeg.input(media_file)
                .output(output_file,acodec='copy',vcodec='copy',setdar=target_ratio)
                .run(capture_stdout=True, capture_stderr=True)
                )

                print("file converted")

    except ffmpeg.Error as e:
        print(f"Failed to transcode file {media_file}.")
        print(e.stderr)

def get_video_codecs(media):
    streams = ffmpeg.probe(media)["streams"]

    vid_codecs = []
    for stream in streams:
        if stream["codec_type"] == "video":
            vid_codecs.append(stream["codec_name"])

    return vid_codecs

def get_library(format):
    if format in codec_dict:
        library = codec_dict[format]
        return library
    else:
        return None

def pp_codec_mod(platform, media_file):
    format_dict = {}
    try:
        with open(formatlist_file, 'r') as f:
            for line in f.readlines():
                format_item = line.strip()
                key,value = format_item.split(':',1)
                format_dict[key] = value

        if not platform in format_dict:
            raise Exception(f"No valid formats for {platform} in file 'flist.txt'")
        else:
            target_format = format_dict[platform]
            current_format = get_video_codecs(media_file)[0]

            if target_format == current_format:
                print(f"File is already of a valid format: {current_format}")
            else:
                output_file = f"converted_{media_file}"

                print(f"File is currently of format: {current_format}")
                print(f"Converting file to: {target_format}")

                target_library = get_library(target_format)

                if not target_library:
                    raise Exception(f'Codec library for {target_format} missing from clist.txt')

                (
                ffmpeg.input(media_file)
                .output(output_file,acodec='copy',vcodec=target_library)
                .run(capture_stdout=True, capture_stderr=True)
                )

                print("file converted")
    except ffmpeg.Error as e:
        print(f"Failed to transcode file {media_file}.")
        print(e.stderr)
