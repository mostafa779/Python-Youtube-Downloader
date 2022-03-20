from pytube import YouTube , Playlist
import winsound,os
import socket


def getInput():
    '''Return [link, dest, option]'''

    link = input('Enter the link: ')
    dest = input('Enter destination(optional): ')
    option = int(input('Video(1) or audio(0): '))
    
    if option == 1:
        quality = input('Enter quality(360 or 720): ')+'p'
    else:
        quality = None
    
    print()

    return [link,dest,option,quality]

def downloadPlaylist(inputs):
    
    for item in inputs:
    
        link = item[0].split()
        url = link[0]

        if len(link) == 2:
            exception = list(map(int,link[1].split(',')))
        else:
            exception = [-1]

        dest = item[1]
        option = item[2]
        quality = item[3]

        playlist = Playlist(url)
        print("%s video(s)" % len(playlist.video_urls))

        if option == 1:
            i = 1
            for video in playlist.videos:
                
                if i in exception:
                    i += 1
                    continue

                print("Downloading {}".format(video.title))
                v = video.streams.get_by_resolution(quality)

                if v is None:
                    v = video.streams.get_highest_resolution()
                
                v.download(dest)

                i+=1
            print(f"Downloaded {i-1} of {len(playlist.video_urls)}")
            print('===============')
        
        elif option == 0:
            i = 1
            for video in playlist.videos:
                
                if i in exception:
                    continue
                
                print("Downloading {}".format(video.title))
                video.streams.get_audio_only().download(dest)
                i+=1
            print(f"Downloaded {i-1} of {len(playlist.video_urls)}")
            print('===============')

def downloadSingleVideo(inputs):
    
    for item in inputs:
    
        link = item[0]
        dest = item[1]
        option = item[2]
        quality = item[3]

        video = YouTube(link)
        print("Title: ",video.title)

        print("Downloading...")
        
        if option == 1:
            video.streams.get_by_resolution(quality).download(dest)

        elif option == 0:
            video.streams.get_audio_only().download(dest)

        print("Downloaded!")
        print('===============')


def main():
    
    while True:
        
        c = input("Press s for single video, p for playlist or q to quit: ")
        
        if c == 'q':
            break
        
        n = int(input('Enter number of trials: '))
        print()
        inputs = []
        
        if c == 'p':
            for x in range(n):
                inputs.append(getInput())
            
            downloadPlaylist(inputs)
        
        elif c == 's':
            for x in range(n):
                inputs.append(getInput())
            
            downloadSingleVideo(inputs)

        winsound.MessageBeep()


def checkConnection():
    try:
        host = socket.gethostbyname("www.google.com")
        s = socket.create_connection((host, 80), 2)
        return True
    except:
        return False


if checkConnection():

    stream = os.popen('pip install --upgrade pytube')
    output = stream.readlines()

    if 'already' not in output[0]:
        for o in output:
            print(o,end="")

    main()

else:
    
    print('Connection Error')
    input()
    

