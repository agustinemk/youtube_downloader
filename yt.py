from pytube import YouTube
from pytube import Playlist
from pytube.cli import on_progress
from os import rename
from os import system
from colors import * #color fg bg

def upgrade_pytube():
	system('python -m pip install pytube')
	system('python -m pip install git+https://github.com/pytube/pytube')

#Convert .mp4 audio file to .mp3
def mp3_convert(out_file):
	root, ext = os.path.splitext(out_file)
	new_file = root + '.mp3'
	os.rename(out_file, new_file)

def printable_size(size):
	ext = ['BYTES', 'KB', 'MB', 'GB', 'TB']
	i = 0
	if size < 62914560: #60 MB
		color = fg.green
	elif size < 209715200: #200 MB
		color = fg.orange
	elif size < 838860800: #800 MB
		color = fg.red
	else:
		color = bg.red

	while int(size/1024) != 0:
		size = size/1024
		i = i+1
	return color + str('{:.4f} '.format(size)) + ext[i] + colors.reset

#upgrade_pytube()
url_list = input('Ingrese la lista de videos: ').split(' ')
video_list = []

for url in url_list:
	if url.find("list") != -1:
		playlist = Playlist(url)
		for video in playlist:
			video_list.append(video)
	else:
		video_list.append(url)

for link in video_list:
	try:
		yt = YouTube(link, on_progress_callback = on_progress)
		print("Link: " + link)
		print("Descargando Video: " + fg.cyan + yt.streams[0].title + colors.reset)
	except:
		print(bg.red + "ERROR CON EL LINK " + link + " SE CONTINUARA CON EL SIGUIENTE" + colors.reset)
	else:	
		#Imprimir streams con formatos disponibles
		formats = yt.streams.order_by('mime_type')
		print(fg.pink + '{0:<10}{1:<15}{2:<15}{3:<15}'.format('itag', 'type', 'quality', 'size') + colors.reset)
		for video_format in formats:
			print('{itag:<10}{type:<15}{quality:<15}{size:>15}'.format(
				itag = video_format.itag,
				type = video_format.mime_type,
				quality = video_format.abr if video_format.mime_type.startswith('audio') else str(video_format.resolution) + '/' + str(video_format.fps),
				size = printable_size(yt.streams.get_by_itag(video_format.itag).filesize)))
		try:
			itag = input('Ingrese itag del formato: ')
			stream = yt.streams.get_by_itag(itag)
			print('Descargando ' + printable_size(stream.filesize) + fg.cyan + ' ' + stream.title + colors.reset)
		except:
			print(bg.red + "ITAG INVALIDO" + colors.reset)
		else:
			out_file = stream.download("Videos/")
			if stream.mime_type == 'audio/mp4':
				if input(fg.red + '\nDesea convertirlo a .mp3? [Y/N] ' + colors.reset).upper() == 'Y':
					mp3_convert(out_file)
			print(fg.green + '\nCompletado con exito!' + colors.reset)
