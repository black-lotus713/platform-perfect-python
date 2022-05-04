import ffmpeg
import os
import sys

path = os.getcwd()


##list of codec:libraries
codeclist_file = path + os.path.sep + 'clist.txt'

codeclist_list = []

with open(codeclist_file, 'r') as c:
    for line in c.readlines():
        codeclist_list.append(line.strip())


##list must be platform:get_video_codec
##e.g.  "youtube:vp9"
formatlist_file = path + os.path.sep + 'flist.txt'

def get_video_codecs(media):
    streams = ffmpeg.probe(media)["streams"]

    vid_codecs = []
    for stream in streams:
        if stream["codec_type"] == "video":
            vid_codecs.append(stream["codec_name"])

    return vid_codecs

def get_library(format):
    for codec in codeclist_list:
        if format in codec:
            c_ix = codec.index(':')
            library = codec[c_ix + 1:]
            return library
    return 'missing'

def pp_ffmpeg(platform, media_file):

    formatlist_list = []

    with open(formatlist_file, 'r') as f:
        for line in f.readlines():
            formatlist_list.append(line.strip())

    platformatlist_list = []

    for line in formatlist_list:
        if platform in line:
            pf_ix = line.index(':')
            platformat = line[pf_ix + 1:]
            platformatlist_list.append(platformat)

    if not platformatlist_list:
        print("No valid formats in file 'flist.txt'")
    else:
        valid_format = False
        ##pulls first video codec
        ##not sure if we should validate all video streams or not
        current_format = get_video_codecs(media_file)[0]
        for pf in platformatlist_list:
            if pf == current_format:
                valid_format = True

        if valid_format == True:
            print(f"File is already of a valid format: {current_format}")
        else:
            target_format = platformatlist_list[0]
            output_file = f"converted_{media_file}"

            print(f"File is currently of format: {current_format}")
            print(f"Converting file to: {target_format}")

            try:
                target_library = get_library(target_format)

                if target_library == 'missing':
                    raise Exception(f'Codec library for {target_format} missing from clist.txt')

                (
                ffmpeg.input(media_file)
                .output(output_file,acodec='copy',vcodec=target_library)
                .run(capture_stdout=True, capture_stderr=True)
                )
            except ffmpeg.Error as e:
                print(f"Failed to transcode file {media_file}.")
                print(e.stderr)

            print("file converted")
