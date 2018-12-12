# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 10:46:05 2018

@author: Tish
"""
import itertools
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim


data_dir = 'C:\\Users\\Tish\\Documents\\Spyder\\zxy_data\\'

game_one_half_one = os.path.join(data_dir, '2013-11-03_tromso_stromsgodset_first.csv')
game_one_half_second = os.path.join(data_dir, '2013-11-03_tromso_stromsgodset_second.csv')
game_two_half_one = os.path.join(data_dir, '2013-11-07_tromso_anji_first.csv')
game_two_half_two = os.path.join(data_dir, '2013-11-07_tromso_anji_second.csv')
game_three = os.path.join(data_dir, '2013-11-28_tromso_tottenham.csv')


def data_in(file):
    data = pd.read_csv(file, header=None)
    data.columns = ['Timestamp', 'player_id', 'x_pos', 'y_pos', 'heading', 'direction', 'energy', 'speed', 'total_distance']
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])
    data = data.set_index('Timestamp')
    # return the dataframe
    return data


def process_players(dataframe, first=True):
    # groups is a generator
    groups = dataframe.groupby('player_id')
    
    player_list = []
    
    if first:
        for player, group in groups:
            # resample by second
            player_list.append( group.resample('S').first().dropna().astype(dataframe.dtypes))
    else:
        for player, group in groups:
            player_list.append(group)
            
    # concat the players back in order by timestamp    
    out_df = pd.concat(player_list)
    out = out_df.sort_index()

    # add row number back as index, keep timestamp column
    if first:
        out = out.reset_index()
    return player_list, out


def update(frame, axes_list, field_pos):
    for i in range(len(axes_list)):
        key = axes_list[i][0]
        seq_length = axes_list[i][1]
        if frame < seq_length:
            axes_list[i][2].set_offsets(np.array([field_pos[key][0][frame],field_pos[key][1][frame]]))
            

def get_field_dict(player_list, num_of_frames=300):
    field_pos_dict = {}

    for player in player_list:
        # reset each player dataframe to have a row index
        player = player.reset_index()

        # grab each player id to add as dict key
        p = player['player_id'][:1]
        p = pd.to_numeric(p[0])
    
        # make 2D array for of x,y-pos for 300 seconds (5 min)
        pos_arr = np.array((player['x_pos'][:num_of_frames].values, player['y_pos'][:num_of_frames].values))
        field_pos_dict[p] = pos_arr
        
    return field_pos_dict


def make_visualization(field_dict, filename, num_of_frames=300, frame_num=0):  
    ax_list = []
    colors = itertools.cycle(['r', 'g', 'b', 'm', 'c', 'k', 'y', 'olive', 'aqua',
                          'lime', 'maroon', 'yellow', 'magenta', 'lightcoral'])

    fig = plt.figure(figsize=(10, 8))
    plt.xlim(0, 115)
    plt.ylim(0, 78)

    for key in field_dict.keys():
        length_of_seq = field_dict[key].shape[1]
        ax_list.append((key,length_of_seq,plt.scatter(x=field_dict[key][0][frame_num], 
                                    y=field_dict[key][1][frame_num], color=next(colors))))
    
    ani = anim.FuncAnimation(fig, update, frames=num_of_frames, fargs=(ax_list, field_dict)).save(filename)
    
    
df = data_in(game_three)
plist, out_data = process_players(df, True)
fpd = get_field_dict(plist, 600)
make_visualization(fpd, 'out_9.mp4', 600)

# drop players under 1000
df_drop_players = out_data[~out_data.isin([3, 7, 10, 13])]
df_drop_cols = df_drop_players[['Timestamp', 'player_id', 'x_pos', 'y_pos']]
#
p2, o = process_players(df_drop_players, False)
fpd2 = get_field_dict(p2)
make_visualization(fpd2, 'out_10.mp4')

# drop players under 1000
df_drop_players3 = out_data[~out_data.isin([3, 7, 9, 10, 13])]
df_drop_cols3 = df_drop_players3[['Timestamp', 'player_id', 'x_pos', 'y_pos']]
#
p3, o3 = process_players(df_drop_players3, False)
fpd3 = get_field_dict(p3)
make_visualization(fpd3, 'out_11.mp4')

clean_data = o3[['Timestamp', 'player_id', 'x_pos', 'y_pos']]

clean_data.to_csv('2013-11-28_tromso_tottenham.csv', index=None)




    
        

    








