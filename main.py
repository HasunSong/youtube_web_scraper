# %% import functions
from youtube import extract_a_channel_using_playlists as get_video , fill_blanks, summarize_data
from save import save_to_file

# %% scrap data
URL="https://www.youtube.com/channel/UCMMJquef91xoOEAWASNZBYA/playlists"#guitar_dd
data=get_video(URL)

#%%
summarize_data(data)
# %% fill in the blanks and check stauts of the data
print(fill_blanks(data))

# %% save file
file_name='youtube_Omar'
csv_format=['Title','','','','','Link','Date','View']
save_to_file(data,file_name,csv_format)
