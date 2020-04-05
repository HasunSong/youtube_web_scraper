# %%
import requests
from bs4 import BeautifulSoup

no_comment_list ,no_date_list, no_view_list, comment_list, date_list, view_list = [], [], [], [], [], []


def extract_a_video(url):
    soup = generate_soup(url)
    # link = soup.find("link")['href']
    title = soup.find("title").string
    comment = soup.find("p", {"id": "eow-description"})
    if comment is None:
        no_comment_list.append(url)
    else:
        comment_list.append(url)
        comment = comment.get_text().strip()
    date = soup.find("strong", {"class": "watch-time-text"})
    if date is None:
        no_date_list.append(url)
    else:
        date_list.append(url)
        date = cut_date(date.string)
    view = soup.find("div", {"class": "watch-view-count"})
    if view is None:
        no_view_list.append(url)
    else:
        view_list.append(url)
        view = cut_view(view.string)
    # likes=
    # length =

    # meta_content=soup.find("meta content").string
    return {
        'Title': title,
        'Date': date,
        'View': view,
        'Comment': comment,
        'Link': url
    }


def extract_a_playlist(title, playlist_url):
    soup = generate_soup(playlist_url)
    playlist_title = soup.find("h1", {"class": "pl-header-title"})
    if playlist_title is None:
        playlist_title = title
        print(f"Error with getting playlist_title =={title}== in ==extract_a_playlist==")
    else:
        playlist_title = playlist_title.string.strip()
    print(f"Extracting ***{playlist_title}***  PlayList Link: {playlist_url}")
    videos = soup.find_all("a", {"class": "pl-video-title-link yt-uix-tile-link yt-uix-sessionlink spf-link"})
    playlist_data = []
    for video in videos:
        # title=video.string
        link = f"https://www.youtube.com{video['href']}"
        playlist_data.append(extract_a_video(link))
        #playlist_data.append(temp_extract_a_video(link))
        length = len(playlist_data)
        if length % 10 is 0:
            print(f"Progress : {length} videos.")
        # playlist_data.append(link)
        # print(title, link)
    if len(playlist_data) == 0:
        print(f"Oop! Failed to get videos in playlist {playlist_title}. I will try again.")
        return extract_a_playlist(title, playlist_url)
    else:
        return playlist_data


def extract_a_channel_using_playlists(url):
    soup = generate_soup(url)
    playlists = soup.find_all("a",
                              {"class": "yt-uix-sessionlink yt-uix-tile-link spf-link yt-ui-ellipsis yt-ui-ellipsis-2"})
    channel_data = {}
    for playlist in playlists:
        title = playlist['title']
        url = f"https://www.youtube.com{playlist['href']}"
        # print(f"extract_a_channel_by_playlists_for_{title},{url}")
        channel_data[f"{title}"] = extract_a_playlist(title, url)
        # channel_data[f"{title}"] = temp_extract_a_playlist(title, url)
    return channel_data


def fill_blanks_once(channel_data):
    blank_list=[]
    for playlist_title in list(channel_data.keys()):
        print(f"Checking PlayList {playlist_title}...")
        playlist_data = channel_data[playlist_title]
        for v_number in range(len(playlist_data)):
            video_dict = playlist_data[v_number]
            if (video_dict['Link'] is not None) and ((video_dict['Title'] is None)
                                                     or (video_dict['Date'] is None) or (video_dict['View'] is None)):
                blank_list.append(video_dict['Link'])
                print(f"Retrying to get data of the video. Link: {video_dict['Link']}")
                channel_data[playlist_title][v_number]=extract_a_video(video_dict['Link'])
    return blank_list

def fill_blanks(channel_data,repeat=5):
    for i in range(repeat):
        print(f"Filling the Blanks. Attempt {i+1} ...")
        fill_blanks_once(channel_data)

def summarize_data(channel_data):
    names=list(channel_data.keys())
    for i in range(len(names)):
        print(f"PlayList {names[i]}:{len(channel_data[names[i]])}")


def generate_soup(url):
    result = requests.get(url)
    # print(result.status_code)
    return BeautifulSoup(result.text, "html.parser")
def temp_extract_a_playlist(title, url):
    print(f"Extracting Playlist {title}. Link: {url}")
    return ["dict_video1", "dict_video2"]
def temp_extract_a_video(url):
    print(f"Extracting Video. Link: {url}")
    return {"title": "temp_title", "link": "temp_link"}
def cut_view(s):
    l=len(s)
    init=0
    fin=l
    for i in range(l):
        if s[i] in ('0','1','2','3','4','5','6','7','8','9'):
            init=i
            break
    for j in range(l-1,-1,-1):
        if s[j] in ('0','1','2','3','4','5','6','7','8','9'):
            fin=j+1
            break
    return s[init:fin]
def cut_date(s):
    l=len(s)
    init=0
    fin=l
    for i in range(l):
        if s[i] in ('0','1','2','3','4','5','6','7','8','9'):
            init=i
            break
    for j in range(l-1,-1,-1):
        if s[j] is '.':
            fin=j+1
            break
    return s[init:fin]
