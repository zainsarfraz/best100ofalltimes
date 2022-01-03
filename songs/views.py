from django.http import response
from django.shortcuts import render
from .models import Song
import requests
import json
from django.http import JsonResponse



# Create your views here.
CLIENT_ID = '222947f8b81c40edb70b68624315be69'
CLIENT_SECRET = '58f9df3aa1ee45f595aaebff60737570'


def getToken():
    AUTH_URL = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })

    # convert the response to JSON
    auth_response_data = auth_response.json()

    # save the access token
    access_token = auth_response_data['access_token']
    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }
    return headers
   

def songsDetail(track_id,headers):
     # base URL of all Spotify API endpoints
    BASE_URL = 'https://api.spotify.com/v1/'
    # Track ID from the URI
    track_id = '6y0igZArWVi6Iz0rj35c1Y'
    # actual GET request with proper header
    r = requests.get(BASE_URL + 'audio-features/' + track_id, headers=headers)
    r = r.json()
    print(r)


def searchItem(text,headers):
    BASE_URL = 'https://api.spotify.com/v1/search'
    r = requests.get(BASE_URL + '?q=' + text + '&type=track&limit=5', headers=headers)
    r = r.json()
    f = open('result.json','w')
    json.dump(r, f, ensure_ascii=False, indent=4)
    return r


def songsIndex(request):
    # get songs sorted by votes
    all_songs = Song.objects.order_by('-votes')
    # get top 100 songs
    songs = all_songs[:100]
    Recaptcha_Client_ID= '104170391579849516009'
    Recaptcha_Key= 'd380b9dc2f1ef19f68464420c623099b06fb6934'
    
    return render(request, 'songs_index.html', {'songs': songs,'recap_secret':Recaptcha_Key})


def search(request):
    search = request.POST.get('search')

    data = searchItem(search,getToken())

    return JsonResponse({'data': data})

def vote(request):
    id = request.POST.get('id')
    track = request.POST.get('track')
    artist = request.POST.get('artist')
    album = request.POST.get('album')

    # check the song
    try:
        song = Song.objects.get(track_id=id)
        song.votes += 1
        song.save()
    except Song.DoesNotExist:
        song = None
        song = Song(track_id=id, track=track, artist=artist, album=album)
        song.save()
    
    return JsonResponse({'data': 'Voted'})
