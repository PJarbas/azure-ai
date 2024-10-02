from pytubefix import YouTube


class YouTubeAudioDownloader:
    def __init__(self, url, output_path='audio.wav'):
        self.url = url
        self.output_path = output_path

    def download_audio(self):
        # Baixa o vídeo do youtube
        yt = YouTube(self.url)
        stream = yt.streams.filter(only_audio=True).first()
        audio_file = stream.download(filename=self.output_path)

        print(f'The audio file is ready: {self.output_path}')

if __name__ == "__main__":
    url = 'https://www.youtube.com/watch?v=zbFAl1qUqzY'
    downloader = YouTubeAudioDownloader(url)
    downloader.download_audio()
