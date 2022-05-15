A flask server which serves a webpage through which interact and download youtube videos at the highest quality possible, using the pytube library.

It's possible to either download a single video or an entire playlist. For playlists, there's an option to download every video and compress it to a TAR file.

FFMPEG binary is required. Since youtube doesn't provide a single file containing both audio and video streams (for the highest quality), it's necessary to download them separately and then merge them using FFMPEG.
