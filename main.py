
import textwrap

import jwt
import requests
import json
import os
from time import time
import re
import string

API_KEY = '###################'
API_SEC = '###################'

# your zoom live meeting id, it is optional though


# create a function to generate a token using the pyjwt library
# def generateToken():
#     token = jwt.encode(
#         # Create a payload of the token containing API Key & expiration time
#         {'iss': API_KEY, 'exp': time() + 5000},
#         # Secret used to generate token signature
#         API_SEC,
#         # Specify the hashing alg
#         algorithm='HS256'
#         # Convert token to utf-8
#     )
#     return token
#     # send a request with headers including a token


generateToken = 'enter your token here'


# fetching zoom meeting info now of the user, i.e, YOU
def getUsers():
    headers = {'authorization': 'Bearer %s' % generateToken,
               'content-type': 'application/json'}

    r = requests.get('https://api.zoom.us/v2/users/', headers=headers)
    print("\n fetching zoom meeting info now of the user ... \n")
    print(r.text)


# fetching zoom meeting participants of the live meeting

# def getMeetingParticipants():
#     headers = {'authorization': 'Bearer %s' % generateToken(),
#                'content-type': 'application/json'}
#     r = requests.get(
#         f'https://api.zoom.us/v2/metrics/meetings/{meetingId}/participants', headers=headers)
#     print("\n fetching zoom meeting participants of the live meeting ... \n")
#
#     # you need zoom premium subscription to get this detail, also it might not work as i haven't checked yet(coz i don't have zoom premium account)
#
#     print(r.text)


# this is the json data that you need to fill as per your requirement to create zoom meeting, look up here for documentation
# https://marketplace.zoom.us/docs/api-reference/zoom-api/meetings/meetingcreate


meetingdetails = {"topic": "The title of your zoom meeting",
                  "type": 2,
                  "start_time": "2019-06-14T10: 21: 57",
                  "duration": "45",
                  "timezone": "Europe/Madrid",
                  "agenda": "test",

                  "recurrence": {"type": 1,
                                 "repeat_interval": 1
                                 },
                  "settings": {"host_video": "true",
                               "participant_video": "true",
                               "join_before_host": "False",
                               "mute_upon_entry": "False",
                               "watermark": "true",
                               "audio": "voip",
                               "auto_recording": "cloud"
                               }
                  }

# def createMeeting():
#     headers = {'authorization': 'Bearer %s' % generateToken(),
#                'content-type': 'application/json'}
#     r = requests.post(
#         f'https://api.zoom.us/v2/users/{userId}/meetings', headers=headers, data=json.dumps(meetingdetails))
#
#     print("\n creating zoom meeting ... \n")
#     print(r.text)


parameters = {
    "type": "past",
    "from": "2022-03-11",
    "to": "2022-03-12"
}

cloudparameters = {
    "from": "2022-04-09",
    "to": "2022-04-09"
}
deletecloudparameters = {
    "from": "2022-03-01",
    "to": "2022-04-"
}


def listallmeetings():
    headers = {'authorization': 'Bearer %s' % generateToken,
               'content-type': 'application/json'}

    r = requests.get('https://api.zoom.us/v2/metrics/meetings', headers=headers, params=parameters)

    print(r.text)


# userId = 'niezoomac10@nie.edu.lk'
# nieusers = ['niezoomac25@nie.edu.lk','niezoomac26@nie.edu.lk','niezoomac27@nie.edu.lk','niezoomac28@nie.edu.lk','niezoomac29@nie.edu.lk','niezoomac30@nie.edu.lk']
#
# for userId in nieusers:
#     print(a)


def getmeeting_name(getmeetingname):
    # getmeetingname = 86510855992
    parent = '/home/sahan/PycharmProjects/video download project'
    headers = {'authorization': 'Bearer %s' % generateToken,
               'content-type': 'application/json'}

    response_get_Meeting_name = requests.get(f'https://api.zoom.us/v2/meetings/{getmeetingname}', headers=headers)

    data_getmeeting_name = response_get_Meeting_name.json()

    returnName = "deleted meeting"
    try:
        returnName = data_getmeeting_name['topic']
        translation_table = str.maketrans('', '', string.punctuation)
        sample_str = returnName.translate(translation_table)

        shortname = sample_str[0:60]

        return shortname
    except KeyError as e:
        return returnName
        raise

    # print(response_get_Meeting_name.text)


def getcloudrecordings():
    nieusers = ['niezoomac3@nie.edu.lk', 'niezoomac4@nie.edu.lk', 'niezoomac5@nie.edu.lk', 'niezoomac6@nie.edu.lk',
                'niezoomac7@nie.edu.lk',
                'niezoomac8@nie.edu.lk', 'niezoomac9@nie.edu.lk', 'niezoomac10@nie.edu.lk', 'niezoomac11@nie.edu.lk',
                'niezoomac12@nie.edu.lk', 'niezoomac13@nie.edu.lk', 'niezoomac14@nie.edu.lk', 'niezoomac25@nie.edu.lk',
                'niezoomac26@nie.edu.lk', 'niezoomac27@nie.edu.lk', 'niezoomac28@nie.edu.lk', 'niezoomac29@nie.edu.lk',
                'niezoomac30@nie.edu.lk', 'niezoomac2@nie.edu.lk']

    # global filetype
    for emailid in nieusers:
        parent = '/home/sahan/PycharmProjects/videoproject'
        headers = {'authorization': 'Bearer %s' % generateToken,
                   'content-type': 'application/json'}

        r = requests.get(f'https://api.zoom.us/v2/users/{emailid}/recordings', headers=headers, params=cloudparameters)

        # print(r.text)

        data = r.json()
        for i in data['meetings']:

            print(i['id'])
            fileid = i['id']
            Meeting_name = getmeeting_name(fileid)
            beforefiledate = i['start_time']
            translation_table = str.maketrans('', '', string.punctuation)
            filedate = beforefiledate.translate(translation_table)
            filename = str(filedate) + "   " + str(fileid) + "  " + Meeting_name

            path = os.path.join(parent, filename)
            os.mkdir(path)
            for t in i['recording_files']:
                filetype = 'MP4'
                if filetype == t['file_extension']:
                    videofile = t['download_url']
                    response_video_download = requests.get(videofile, headers=headers, allow_redirects=True,
                                                           stream=True)

                    with open(f"{filename}/{fileid} zoom video.{t['file_extension']}", "wb") as video:
                        for chunk in response_video_download.iter_content(chunk_size=8192):
                            # writing one chunk at a time to pdf file
                            if chunk:
                                video.write(chunk)

                else:
                    audiofile = t['download_url']
                    response_audio_download = requests.get(audiofile, headers=headers, allow_redirects=True,
                                                           stream=True)

                    with open(f"{filename}/{fileid} zoom audio.{t['file_extension']}", "wb") as audio:
                        for chunk in response_audio_download.iter_content(chunk_size=8192):
                            # writing one chunk at a time to pdf file
                            if chunk:
                                audio.write(chunk)


def deletecloudrec():
    nieusers = ['niezoomac3@nie.edu.lk', 'niezoomac4@nie.edu.lk', 'niezoomac5@nie.edu.lk', 'niezoomac6@nie.edu.lk',
                'niezoomac7@nie.edu.lk',
                'niezoomac8@nie.edu.lk', 'niezoomac9@nie.edu.lk', 'niezoomac10@nie.edu.lk', 'niezoomac11@nie.edu.lk',
                'niezoomac12@nie.edu.lk', 'niezoomac13@nie.edu.lk', 'niezoomac14@nie.edu.lk', 'niezoomac25@nie.edu.lk',
                'niezoomac26@nie.edu.lk', 'niezoomac27@nie.edu.lk', 'niezoomac28@nie.edu.lk', 'niezoomac29@nie.edu.lk',
                'niezoomac30@nie.edu.lk', 'niezoomac2@nie.edu.lk']

    # global filetype
    for emailid in nieusers:
        parent = '/home/sahan/PycharmProjects/videoproject'
        headers = {'authorization': 'Bearer %s' % generateToken,
                   'content-type': 'application/json'}

        r = requests.get(f'https://api.zoom.us/v2/users/{emailid}/recordings', headers=headers,
                         params=deletecloudparameters)

        print(r.text)

        data = r.json()
        for i in data['meetings']:
            print(i['id'])
            deleteid = i['id']

            r = requests.delete(f'https://api.zoom.us/v2/meetings/{deleteid}/recordings', headers=headers)
            print(r.text)



# deletecloudrec()

getcloudrecordings()
