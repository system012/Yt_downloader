from pytube import YouTube
from pytube import Playlist
import os
import re
import tarfile
from constants import downloaded_dir

def extract_playlist_urls_and_titles(link):
    playlist = Playlist(link)
    urls = playlist.video_urls
    titles = []
    for url in urls:
        youtube = YouTube(url)
        title = youtube.title
        titles.append(title)
    
    return urls, titles

def is_playlist(link):
    return 'list=' in link

def link_handler(link):
    youtube = YouTube(link)
    video_title, audio_title = renamer(youtube)

    download_streams(youtube, video_title, audio_title)

    error, video_title_with_ext, audio_title_with_ext, final_title_with_location, final_title_no_loc = extension_check(video_title, audio_title)

    if error:
        print('Error: File extension not supported')
        raise SystemExit

    merge_audio_video(video_title_with_ext, audio_title_with_ext, final_title_with_location)
    delete_residue(video_title_with_ext, audio_title_with_ext)

    return final_title_with_location, final_title_no_loc

def renamer(youtube):
    '''Adding "v" and "a" to the end of the title to differentiate between video and audio files'''
    original_title = youtube.title
    video_title = re.sub("[^0-9a-zA-Z]+", "", original_title) + 'v' # remove special characters and add 'v' to the end of the title
    audio_title = video_title + 'a' # add 'a' to the end of the title
   
    return video_title, audio_title

def download_streams(youtube, video_title, audio_title):
    try: 

        print(f'Downloading {video_title} video')
        print(f'Downloading {audio_title} audio')
        youtube.streams.filter(adaptive=True, only_video=True).order_by('resolution').desc().first().download(downloaded_dir, video_title) # download video
        youtube.streams.filter(only_audio=True).order_by('abr').desc().first().download(downloaded_dir, audio_title) # download audio

    except (Exception, IOError) as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print (message)

def extension_check(video_title, audio_title):
    audio_title_with_ext = os.path.join(downloaded_dir, audio_title + '.webm')
    error = False
    
    allowed_extensions = ['.webm', '.mp4']

    for ext in allowed_extensions:
        video_path = os.path.join(downloaded_dir, video_title)
        video_title_with_ext = video_path + ext

        if os.path.isfile(video_title_with_ext):
            final_title_no_loc = video_title + 'Final' + ext
            final_title_with_location = os.path.join(downloaded_dir, final_title_no_loc)

            return error, video_title_with_ext, audio_title_with_ext, final_title_with_location, final_title_no_loc
    
    error = True

    return error, None, None, None, None

def merge_audio_video(video_title_with_ext, audio_title_with_ext, final_title_with_location):
    os.system(f'ffmpeg -y -i {audio_title_with_ext} -i {video_title_with_ext} -c:a copy -c:v copy {final_title_with_location}')

def delete_residue(video_title_with_ext, audio_title_with_ext):
    if os.path.isfile(video_title_with_ext) and os.path.isfile(audio_title_with_ext):
        os.remove(video_title_with_ext)
        os.remove(audio_title_with_ext)
        print('Residue files were deleted successfully')

#Tar_location è importante perché il file tar è ubicato in una directory diversa dai file che andiamo ad archiviare (e.g. il file è in app/downloaded mentre il tar è in app/)

def tar_files(downloaded_files):
    with tarfile.open('playlist.tar','w') as tar:
        for file in downloaded_files:
            tar.add(file)
    tar_location = os.path.join(os.getcwd(), 'playlist.tar')

    return tar_location

# def yt_download(link):
#     final_title_with_location, final_title_no_loc = is_single_or_playlist(link)