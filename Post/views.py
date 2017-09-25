from django.shortcuts import render
from TwitterAPI import TwitterAPI
from Post.models import Album, User
import calendar
import collections

# Create your views here.

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

api = TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret)

def newsfeed(request):
    # print("request:: ",request)


    hashtag_string = '#katrinakaif'
    hashtag_string = hashtag_string.lower()
    if(request.GET.get('mybtn')):
        hashtag_string = str(request.GET.get('hashtag'))
        print("HashtagString :: ",hashtag_string)

    # display all images in database if
    # searched keyword is '#msdeep14'

    if hashtag_string == '#msdeep14':
        url_list = []
        retweet_count_list = []
        url_retweet_dict = {}
        url_favorite_dict = {}
        favorite_count_list = []

        url_list_in_database = Album.objects.all().filter(user = request.user).values('image_url')
        temp = Album.objects.all().filter(user = request.user).values('image_url', 'date', 'retweet_count','like_count')

        url_list = {}
        for entry in temp:
            dt = str(entry['date'])[0:10]
            dt = calendar.month_name[int(dt[5:7])] + " " + dt[8:10] + ", " + dt[0:4]
            url_list[str(entry['image_url'])] = (dt, str(entry['retweet_count']),str(entry['like_count']))
        return render(request, 'Post/newsfeed.html', {'url_list': url_list})


    else:
        url_list = []
        retweet_count_list = []
        url_retweet_dict = {}
        url_favorite_dict = {}
        favorite_count_list = []
        r = api.request('search/tweets', {'q':hashtag_string, 'filter':'images','count' : 50})
        # rv = api.request('search/tweets',{'q':'#hello', 'filter' : 'videos'})

        # for item in rv:
        #     print(item)
        #     print('\n\n')

        # 'media_url_https': 'https://pbs.twimg.com/media/DKesMqrVwAAwfby.jpg'

        for item in r:
            line = str(item)
            # get the image url and store it in url_list
            pos = line.find('media_url_https')
            t = line[pos + 21:].find('\'')
            if(pos >= 0):
                url = line[pos + 19:pos + 21 + t]
                url_list.append(str(url))

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

            '''
            from Post.models import Album
            from django.contrib.auth.models import User
            User.objects.all()
            <QuerySet [<User: msdeep14>]>
            me = User.objects.get(username='msdeep14')
            Album.objects.filter(user = me).values('image_url')

            # it will give you all the image urls in database
            '''

            url_list_in_database = Album.objects.all().filter(user = request.user, hashtag = hashtag_string).values('image_url')

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
                album = Album(hashtag = hashtag_string, image_url = url, user = request.user, retweet_count = url_retweet_dict[url], like_count = url_favorite_dict[url])
                album.save()

            temp = Album.objects.all().filter(user = request.user, hashtag = hashtag_string).values('image_url', 'date', 'retweet_count','like_count')

            url_list = {}
            '''
            example of one entry
            {'retweet_count': 22, 'image_url': 'https://pbs.twimg.com/ext_tw_video_thumb/902590747001491456/pu/img/4WRHbtmvVNQa0ne3.jpg',
            'date': datetime.datetime(2017, 9, 25, 5, 23, 25, 841087, tzinfo=<UTC>), 'like_count': 0}
            '''
            for entry in temp:
                dt = str(entry['date'])[0:10]
                dt = calendar.month_name[int(dt[5:7])] + " " + dt[8:10] + ", " + dt[0:4]
                url_list[str(entry['image_url'])] = (dt, str(entry['retweet_count']),str(entry['like_count']))

            total_entries_in_database = len(url_list)

            return render(request, 'Post/newsfeed.html', {'url_list': url_list})



# def request_page(request):
#     print("hello")
#     if(request.GET.get('mybtn')):
#         print("string :: ",str(request.GET.get('hashtag')))
#         newsfeed( str(request.GET.get('hashtag')) )
#     return render(request,'Post/newsfeed.html')
