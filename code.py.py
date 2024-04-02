import pandas as pd

file_path = "toy_example.csv"

 #Q 1.1
 #Complexity: O(1)
def load_history(file_path):
	return pd.read_csv(file_path)

print("\n Q 1.1")
history = load_history(file_path)
print(history.head())



 #Q 1.2
 #Complexity: O(n*m)
def prepare_history(file_path):
	file = load_history(file_path)
	played_songs = file['played_songs'].tolist() #tolist() complexsity O(1)
	for i in range(len(played_songs)): #iterate n times
		played_songs[i] = [str(item) for item in played_songs[i].split(',')] #iterate m times
	file['played_songs'] = played_songs
	return file

print("\n Q 1.2")
history = prepare_history(file_path)
print(history.head())


 #Q 1.3
 #Complexity: O(n*m)
def print_history(file_path):
	file = prepare_history(file_path) #prepare_history() complexsity O(n*m)
	print(file.head()) #print first 5 rows
	sum = count = avg = 0 #init to 0
	played_songs = file['played_songs'].tolist() #tolist() complexsity O(1)
	#iterate n*m times
	for i in played_songs: #iterate n times
		count += 1 #count number of users
		for j in i: #iterate m times
			sum += 1 #count number of songs from all users
	if (count != 0): avg = sum / count #calc avarage
	print("Average length of the songs per user is %.2f" % avg) #display with 2 decimal

print("\n Q 1.3")
print_history(file_path)



 #Q 2.1
 #Complexity: O(n*m)
def get_songs(file_path):
	file = prepare_history(file_path) #prepare_history() complexsity O(n*m)
	played_songs = file['played_songs'].tolist() #tolist() complexsity O(1)
	songs = list()
	for i in range(len(played_songs)): #iterate n times
		for j in range(len(played_songs[i])): #iterate m times
			#split() splits the string by the dlimiter '(' and returns an array
			#the fisrt item in the array is the song name
			#strip() trims the spaces at the start and from the end of the string
			song_name = played_songs[i][j].split('(')[0].strip() #extract song name
			songs.append(song_name) #append() complexsity O(1)
	return songs

print("\n Q 2.1")
songs = get_songs(file_path)
print(songs)


 #Q 2.2
 #Complexity: O(n*m)
def get_singers(file_path):
	file = prepare_history(file_path) #prepare_history() complexsity O(n*m)
	played_songs = file['played_songs'].tolist() #tolist() complexsity O(1)
	singers = list()
	for i in range(len(played_songs)): #iterate n times
		for j in range(len(played_songs[i])): #iterate m times
			#the second item in the array is the singer name
			#[:-1] is to eliminate the ending )
			singer_name = played_songs[i][j].split('(')[1][:-1].strip() #extract singer name
			singers.append(singer_name) #append() complexsity O(1)
	return singers

print("\n Q 2.2")
singers = get_singers(file_path)
print(singers)


 #Q 2.3
 #Complexity: O(n*m)
def count_singers(file_path):
	file = prepare_history(file_path) #prepare_history() complexsity O(n*m)
	played_songs = file['played_songs'].tolist() #tolist() complexsity O(1)
	singers = get_singers(file_path) #get_singers() complexsity O(n*m)
	singers = list(set(singers)) # complexsity O(n*m)

	singer_dict = {}
	for i in range(len(played_songs)): #iterate n times
		for j in range(len(played_songs[i])): #iterate m times
			singer_name = played_songs[i][j].split('(')[1][:-1].strip()
			if singer_name in singer_dict: singer_dict[singer_name] += 1 #complexsity O(1)
			else: singer_dict[singer_name] = 1 #complexsity O(1)
	
	count = [0] *26
	i=0
	for singer_key in singer_dict: #complexsity O(n*m)
		singers[i] = singer_key
		count[i] = singer_dict[singer_key]
		i += 1
	return singers, count 

print("\n Q 2.3")
singers, singer_count = count_singers(file_path)
for singer, count in zip(singers, singer_count):
	print(f'{singer}: {count}')


 #Q 3.1
 #Complexity: O(n*m)
 #explanation: bucket sort to al
def hist_by_letter(file_path):
	file = prepare_history(file_path) #prepare_history() complexsity O(n*m)
	played_songs = file['played_songs'].tolist() #tolist() complexsity O(1)
	singers = list(get_singers(file_path)) #get_singers() complexsity O(n*m)
	minValue = ord('a') #ascii value of 'a'
	singer_count_by_letter = [0] * 26 # there are 26 letters in the alphabet
	for i in range(len(singers)): #iterate n*m times
		singer_letter = singers[i][0].lower()
		singer_count_by_letter[ord(singer_letter) - minValue] += 1 #complexsity O(1)
	return singer_count_by_letter

print("\n Q 3.1")
singers, singer_count = count_singers(file_path)
singer_count_by_letter = hist_by_letter(file_path)
print(singer_count_by_letter)



import matplotlib.pyplot as plt
 #Q 3.2
 #Complexity: O(n*m)
def plot_bar(file_path):
	x_arr = [i for i in range(0, 27)] # values for x
	singer_count_by_letter = hist_by_letter(file_path) #hist_by_letter() complexsity O(n*m)
	data = list() # values for y
	for i in range(len(singer_count_by_letter)):#iterate max n*m times
		for j in range(singer_count_by_letter[i]):
			#if the letter has value k, then it will be added k times to data
			data.append(i) # i is the index of the letter
	plt.hist(data, bins=x_arr, align='left')
	plt.show()

print("\n Q 3.2")
plot_bar(file_path)


 #Q 4
 #Complexity: O(n*m)
def best_song(file_path):
	file = prepare_history(file_path) #prepare_history() complexsity O(n*m)
	users_songs = file['played_songs'].tolist() #tolist() complexsity O(1)
	#songs = get_songs(file_path)
	song_count = {}
	for user_songs in users_songs: #iterate n times
		for song_name in user_songs: #iterate m times
			if song_name in song_count: song_count[song_name] += 1 #complexsity O(1)
			else: song_count[song_name] = 1 #complexsity O(1)
	print(max(song_count)) #complexsity O(n*m)

print("\n Q 4")
file_path = "my_history.csv"
best_song(file_path)