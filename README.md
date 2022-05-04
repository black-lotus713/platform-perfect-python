# platform-perfect-python
script for calling ffmpeg to check a video and convert as needed

two args -
- platform - target platform such as youtube, brighteon
- media_file - filename of media file to be checked/converted
  
the script requires two files to be maintained in the same path:
- flist.txt - platform:videocodec (e.g. "youtube:vp9") 
- clist.txt - codec:codeclibrary (e.g. "vp9:libvpx-vp9")

keep in mind that some libraries have to be special enabled at setup time for ffmpeg (libvpx-vp9 being one of them)

regular maintenance will include recompiling ffmpeg to enable new libraries as needed
  
