import urllib
import threading
import subprocess
import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

class video_stitcher(object):

	def read_video_from_url(self, **kwargs):
		'''
		Read a file from s3 to use for stitching
		'''
		video_urls = kwargs['video_urls']
		video_num = 0
		video_names = []
		with open('output.mp4', 'a') as output:
			for url in video_urls:
				url_file = urllib.urlopen(url)
				output.write(url_file.read())
				# with open('video{}.mp4'.format(video_num), 'wb') as  f:
				# 	f.write(url_file.read())

				# subprocess.call('ffmpeg -i video{}.mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts intermediate{}.ts'.format(video_num, video_num))
				video_names.append('video{}.mp4'.format(video_num))
				video_num += 1
				print 'Wrote video: {}'.format(video_num)
		concatenate_string = ' '.join(video_names)
		print 'mencoder -oac copy -ovc copy -idx -o output.mp4 {}'.format(concatenate_string)
		# subprocess.call('ffmpeg -vcodec copy -isync -i "concat:{}" outputfile.mp4'.format(concatenate_string))
		# subprocess.call('ffmpeg -i "concat:{}" -c copy -bsf:a aac_adtstoasc output.mp4'.format(concatenate_string))
		# subprocess.call('mencoder -of lavf -oac copy -ovc copy -o output.mp4 {}'.format(concatenate_string))
		print 'Done Writing Files'


	def stitch_videos(self, video_urls):
		# video_urls = ['https://rapchat.s3.amazonaws.com/sessions/session_59/clip_1.mp4?Signature=er0cRiEqlngiJ0YJ9OdmFwRuaKo%3D&Expires=1389250773&AWSAccessKeyId=AKIAJ2KVSZDJH7UPGAAQ',]
		thread = threading.Thread(target=self.read_video_from_url, kwargs={'video_urls':video_urls})
		thread.start()
		print 'Spun off thread'

if __name__ == '__main__':
	urls = ['https://s3.amazonaws.com/rapchat/sessions/session_59/clip_1.mp4',
	'https://s3.amazonaws.com/rapchat/sessions/session_55/clip_2.mp4']
	vs = video_stitcher()
	vs.stitch_videos(urls)
	print 'done'