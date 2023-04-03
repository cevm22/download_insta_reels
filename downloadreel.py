 
import os
import shutil
import instaloader
from pydub import AudioSegment

def extract_audio(fileName, id):
    # # Load the MP4 video
    print("Loading MP4 file...")
    video = AudioSegment.from_file(str('./firstdownload/' + fileName), format="mp4")

    # Extract the audio from the video
    audio = video.set_channels(1)  # convert to mono 
    audio = audio.set_frame_rate(22050)  # set sample rate to 22050 Hz 
    audio = audio.set_sample_width(2)  # set sample width to 16-bit

    # Save the audio as a WAV file
    print("saving audio ...")
    name = fileName[:-4]
    audio.export(os.path.join("audio", id + ".wav"), format="wav", parameters=["-ac", "1", "-ar", "22050", "-sample_fmt", "s16"])
    
    # Save the mp4 to dir videos
    src_path = os.path.abspath(str('./firstdownload/' + fileName))
    dest_path = os.path.abspath(os.path.join("videos", os.path.basename(str(id)+'.mp4')))
    shutil.move(src_path, dest_path)
    
    # Cleaning the firstdownload dir
    dir_path = 'firstdownload'

    # Get a list of all the files and directories inside the directory
    print("cleaning file")
    items = os.listdir(dir_path)

    # Loop through each item
    for item in items:
        # Create the full item path
        item_path = os.path.join(dir_path, item)
        # Check if the item is a file or directory
        if os.path.isfile(item_path):
            os.remove(item_path)  # Remove the file
    return


filename = 'links.txt' # Links must be only the ID post

# Open the file and read all the lines into a list
with open(filename, 'r') as file:
    rows = [line.strip() for line in file]


total = len(rows)
i = 1
for link in rows:
    print("Downloading # ", str(i), "of ", str(total), "POST ID: ", str(link))
    # print(link)
    loader = instaloader.Instaloader()
    post = instaloader.Post.from_shortcode(loader.context,str(link))
    loader.download_post(post, "firstdownload")

    dir_path = "./firstdownload"  

    mp4_files = [f for f in os.listdir(dir_path) if f.endswith(".mp4")]

    for mp4_file in mp4_files:
        print('getting file >>> ',mp4_file)
        extract_audio(mp4_file,link)
    i+=1
    