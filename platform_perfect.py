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

codec_dict = {}
with open(codeclist_file, 'r') as c:
    for line in c.readlines():
        codec_item = line.strip()
        key,value = codec_item.split(':',1)
        codec_dict[key] = value

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

def pp_ffmpeg(platform, media_file):
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
