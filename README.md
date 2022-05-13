# platform-perfect-python
module for calling ffmpeg to check a video and convert as needed

two main functions: pp_codec_mod(platform, media_file) and pp_dar_mod(platform, media_file)
- platform - target platform such as youtube, brighteon
- media_file - filename of media file to be checked/converted

the first function checks the video codec and the second function checks the display aspect ratio (calculating from video width/height if not present in the ffprobe results) and uses the lists below to drive changes as needed

the script requires three files to be maintained in the same path:
- flist.txt - platform:videocodec (e.g. "youtube:vp9") 
- clist.txt - codec:codeclibrary (e.g. "vp9:libvpx-vp9")
- rlist.txt - platform|ratio1,ratio2,ratio3 (e.g. "brighteon|16:9,9:16,4:3,3:4")

keep in mind that some libraries have to be special enabled at setup time for ffmpeg (libvpx-vp9 being one of them)

regular maintenance will include recompiling ffmpeg to enable new libraries as needed
  
