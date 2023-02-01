from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
import environ
env = environ.Env()
environ.Env.read_env()
import pyrebase
from django.views.decorators.csrf import csrf_exempt
import slack
import threading
import json

config = {
        "apiKey": env('API_KEY'),
        "authDomain": env('AUTH_DOMAIN'),
        "projectId": env('PROJECT_ID'),
        "storageBucket": env('STORAGE_BUCKET'),
        "messagingSenderId": env('MESSAGING_SENDER_ID'),
        "appId": env('APP_ID'),
        "measurementId": env('MEASUREMENT_ID'),
        "databaseURL": env('DATABASE_URL')
    }

# Create your views here.
def fetch_blogs(req):
    firebase = pyrebase.initialize_app(config)

    database = firebase.database()

    blogs_path = database.child('blogs')

    blog_content = blogs_path.get().val()

    blogs = []

    for key in blog_content:
        blog_item = database.child('blogs').child(key).get().val()
        blogs.append(
            {'key': key,
             'title' : blog_item['title'],
             'date_time': blog_item['date_time'],
             'description': blog_item['description']
            })

    return JsonResponse(blogs, safe=False)

@csrf_exempt
def send_email(req):
    message = req.POST['message']
    full_name = req.POST['full_name']
    email = req.POST['email']
    print(message, email, full_name)

    client = slack.WebClient(token=env('SLACK_TOKEN'))
    client.chat_postMessage(channel="#testing", text=f"{full_name} - {email} -- {message}")

    return HttpResponse('Message Sent')