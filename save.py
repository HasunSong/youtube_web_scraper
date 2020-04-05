# %%
import csv

#Title Date View Comment Link

def save_to_file(channel_data,file_name,csv_format):
    file = open(f"{file_name}.csv", mode="w", encoding='utf-8-sig',newline='\n')
    writer = csv.writer(file)
    writer.writerow(csv_format)
    for playlist_title in list(channel_data.keys()):
        writer.writerow([f"\n{playlist_title}"])
        playlist_data = channel_data[playlist_title]
        for v_number in range(len(playlist_data)):
            video_info = playlist_data[v_number]
            line=[]
            for i in range(len(csv_format)):
                if csv_format[i] == '':
                    line.append('')
                else:
                    line.append(video_info[csv_format[i]])
            writer.writerow(line)
    return