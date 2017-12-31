from django.shortcuts import render
from TwitterAPI import TwitterAPI
from Post.models import Album, User
import calendar
from django.contrib.auth.models import User
import requests

import http.client, urllib.request, urllib.parse, urllib.error, base64, sys
import simplejson as json

# MICROSOFT EMOTION API
subscription_key = ''

headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': subscription_key,
}
params = urllib.parse.urlencode({
})

# twitter access tokens
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

api = TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret)

me = User.objects.get(username='msdeep14')

# get the emotion of image
def get_emotion(url):
    b = { 'url': url}
    body = str(b)
    # print (url)
    try:
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/emotion/v1.0/recognize?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        # 'data' contains the JSON data. The following formats the JSON data for display.
        parsed = json.loads(data)
        # print ("Response:")
        # print (json.dumps(parsed, sort_keys=True, indent=2))
        conn.close()

        # get the most powerful emotion, with maximum value
        if(parsed[0] is not NULL):
            scores = parsed[0]["scored"]
            max_emotion = max(scores, key = scores.get)
            return max_emotion
        else:
            return "happiness"

    except Exception as e:
        # print(e.args)
        return "happiness"


def newsfeed(request):
    # print("request:: ",request)
    hashtag_string = '#katrinakaif'
    hashtag_string = hashtag_string.lower()
    if(request.GET.get('mybtn')):
        hashtag_string = str(request.GET.get('hashtag'))
        print("HashtagString :: ",hashtag_string)

    # display all images stored in database if
    # searched keyword is '#msdeep14'

    if hashtag_string == '#msdeep14':
        url_list = []
        retweet_count_list = []
        url_retweet_dict = {}
        url_favorite_dict = {}
        favorite_count_list = []

        url_list_in_database = Album.objects.all().filter(user = me).values('image_url')
        temp = Album.objects.all().filter(user = me).values('image_url', 'date', 'retweet_count','like_count')

        url_list = {}
        for entry in temp:
            dt = str(entry['date'])[0:10]
            dt = calendar.month_name[int(dt[5:7])] + " " + dt[8:10] + ", " + dt[0:4]
            url_list[str(entry['image_url'])] = (dt, str(entry['retweet_count']),str(entry['like_count']))
        return render(request, 'Post/newsfeed.html', {'url_list': url_list})

    # get the images of particular hashtag
    else:
        url_list = []
        retweet_count_list = []
        url_retweet_dict = {}
        url_favorite_dict = {}
        url_emotion_dict = {}
        favorite_count_list = []
        r = api.request('search/tweets', {'q':hashtag_string, 'filter':'images','count' : 1000})
        # rv = api.request('search/tweets',{'q':'#hello', 'filter' : 'videos'})

        # for item in rv:
        #     print(item)
        #     print('\n\n')

        # 'media_url_https': 'https://pbs.twimg.com/media/DKesMqrVwAAwfby.jpg'
        url_dict = {}
        for item in r:
            line = str(item)
            # get the image url and store it in url_list
            pos = line.find('media_url_https')
            t = line[pos + 21:].find('\'')
            if(pos >= 0):
                url = line[pos + 19:pos + 21 + t]
                url_list.append(str(url))
            # else:
            #     print("pos < 0")

            # get no of retweets and store it in retweet_count_list
            retweet_pos = line.find('retweet_count')
            t = line[retweet_pos:].find(',')
            if(retweet_pos >= 0):
                count = line[retweet_pos + 16:retweet_pos+ t]
                retweet_count_list.append(int(count))

            # get no of favourites and store in favorite_count_list
            favorite_pos = line.find('favorite_count')
            t = line[favorite_pos:].find(',')
            if(favorite_pos >= 0):
                count = line[favorite_pos + 16:favorite_pos+t]
                favorite_count_list.append(int(count))

        # for all the urls, map the url with their corresponding
        # retweet_count and favorite_count
        size = len(url_list)
        for i in range(0,size):
            url_retweet_dict[url_list[i]] = retweet_count_list[i]
            url_favorite_dict[url_list[i]] = favorite_count_list[i]

        # emotion requests are limited to 20 because you can make only
        # 20 requests per minute to microsoft API, and total of
        # 30,000 requests in one month in free subscription

        # other than 20 requests, default emotion is set to "happiness"
        for i in range(0,size):
            if (i < 20):
                url_emotion_dict[url_list[i]] = get_emotion(url_list[i])
                # print(url_emotion_dict[url_list[i]])
            else:
                url_emotion_dict[url_list[i]] = "happiness"
                # print(url_emotion_dict[url_list[i]])

        '''
            from Post.models import Album
            from django.contrib.auth.models import User
            User.objects.all()
            <QuerySet [<User: msdeep14>]>
            me = User.objects.get(username='msdeep14')
            Album.objects.filter(user = me).values('image_url')
            # it will give you all the image urls in database

            User.objects.get(username='msdeep14').delete()
        '''

        url_list_in_database = Album.objects.all().filter(user = me, hashtag = hashtag_string).values('image_url')

        # for url in url_list:
        #     print(url)

        temp = []
        for url in url_list_in_database:
            temp.append(str(url['image_url']))

        # check if there are new urls in the list by taking difference with
        # previously stored urls
        url_list_in_database = temp
        new_urls = list(set(url_list) - set(url_list_in_database))

        # if there are new urls, save them into database
        for url in new_urls:
            album = Album(hashtag = hashtag_string, image_url = url, user = me, retweet_count = url_retweet_dict[url], like_count = url_favorite_dict[url], emotion = url_emotion_dict[url])
            album.save()

        temp = Album.objects.all().filter(user = me, hashtag = hashtag_string).values('image_url', 'date', 'retweet_count','like_count','emotion')


        '''
            example of one entry
            {'retweet_count': 22, 'image_url': 'https://pbs.twimg.com/ext_tw_video_thumb/902590747001491456/pu/img/4WRHbtmvVNQa0ne3.jpg',
            'date': datetime.datetime(2017, 9, 25, 5, 23, 25, 841087, tzinfo=<UTC>), 'like_count': 0}
        '''
        for entry in temp:
            dt = str(entry['date'])[0:10]
            dt = calendar.month_name[int(dt[5:7])] + " " + dt[8:10] + ", " + dt[0:4]
            url_dict[str(entry['image_url'])] = (dt, str(entry['retweet_count']),str(entry['like_count']),str(entry['emotion']))

        return render(request, 'Post/newsfeed.html', {'url_list': url_dict})



# def request_page(request):
#     print("hello")
#     if(request.GET.get('mybtn')):
#         print("string :: ",str(request.GET.get('hashtag')))
#         newsfeed( str(request.GET.get('hashtag')) )
#     return render(request,'Post/newsfeed.html')
