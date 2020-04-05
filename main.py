# %% import functions
from youtube import extract_a_channel_using_playlists as get_video , fill_blanks, summarize_data
from save import save_to_file

# %% scrap data
#URL="https://www.youtube.com/channel/UCMMJquef91xoOEAWASNZBYA/playlists"#guitar_dd
#URL = "https://www.youtube.com/user/GrabTheGT/playlists"#grab_the_guitar
#URL = "https://www.youtube.com/channel/UCyn-K7rZLXjGl7VXGweIlcA/playlists" #paik's cuisine
#URL = "https://www.youtube.com/channel/UCwk-TaC8rgj7BMzxY3Zu4UQ/playlists" #Jaehoon Jang
#URL = "https://www.youtube.com/channel/UCUpJs89fSBXNolQGOYKn0YQ/playlists" #nomad_coders
URL = "https://www.youtube.com/channel/UCvdvPu_7TTcrZz1nGh98Sqg/playlists" #omar
data=get_video(URL)

#%%
summarize_data(data)
# %% fill in the blanks and check stauts of the data
print(fill_blanks(data))

# %% save file
file_name='youtube_Omar'
csv_format=['Title','','','','','Link','Date','View']
save_to_file(data,file_name,csv_format)