import vlc
import json
import time
import random
import os
import fnmatch
import csv
SpecifiedFolder = 'C:\\MusicSource'

class MusicPlayer:
    def __init__(self,LibraryLocation):
        self.LibraryLocation = LibraryLocation
        self.CompiledLibrary = []
        self.TagArtist = []
        self.TagAlbum = []
        self.TagTrack = []
        self.RequestLibrary = []
        self.instance = vlc.Instance()
        self.player=self.instance.media_player_new()
    def GetLibrary(self):
        print('Getting Library from ' + self.LibraryLocation)
        for dirname, dirnames, filenames in os.walk(self.LibraryLocation):
            for filename in filenames:
                if fnmatch.fnmatch(filename, "*.mp3"):
                    self.CompiledLibrary.append(os.path.join(dirname, filename))
                elif fnmatch.fnmatch(filename, "*.wav"):
                    self.CompiledLibrary.append(os.path.join(dirname, filename))
    def TrackTags(self):
        #for song in self.CompiledLibrary:
            #m = MP3(song, ID3=EasyID3)
            #self.TagArtist.append(m['artist'][0])
            #self.TagAlbum.append(m['album'][0])
            #self.TagTrack.append(m['title'][0])
            #print("Artist: %s" % m['artist'][0])
            #print("Album: %s" % m['album'][0])
            #print("Track: %s" % m['title'][0])
        print('done')
    def AddRequest(self, Location):
        self.RequestLibrary.append(Location)
        print('Request Added')
    def PrintLibrary(self):
        for song in self.CompiledLibrary:
            print(song)
    def Play(self,song):
        media = self.instance.media_new_path(song)
        self.player.set_media(media)
        self.player.play()
        playing = set([1,2,3,4])
        time.sleep(1)
        duration = self.player.get_length() / 1000
        mm, ss = divmod(duration, 60)
        while True:
            state = self.player.get_state()
            #print(state)
            if state not in playing:
                #track not playing, so break while loop
                break
            continue
    def Stop(self):
        self.player.stop
        print('Play stopped.')
        return
    def Routine1(self):
        while True:
            if not self.RequestLibrary:
                random.shuffle(self.CompiledLibrary)
                for song in self.CompiledLibrary:
                    print( "random - " + song)
                    self.Play(song)
                    break
            else:
                for song in self.RequestLibrary:
                    print( "request - " + song)
                    self.Play(song)
                    self.RequestLibrary.remove(song)
                    break

if __name__ == '__main__':
    x = MusicPlayer(SpecifiedFolder)
    x.GetLibrary()
    x.TrackTags()
    #x.GetRequests()
    #x.PrintLibrary()
    #x.Play('C:\\Users\\Craig Hissett\\Desktop\\play.mp3')
    #x.Routine1()
