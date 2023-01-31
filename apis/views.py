from django.shortcuts import render
from django.http.response import HttpResponse
import environ
env = environ.Env()
environ.Env.read_env()
import pyrebase
from django.views.decorators.csrf import csrf_exempt

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
        blogs.append([key, blog_item['title'], blog_item['date_time']])

    return HttpResponse(blogs)

@csrf_exempt
def send_email(req):
    message = req.POST['message']
    full_name = req.POST['full_name']
    email = req.POST['email']
    print(message, email, full_name)
    return HttpResponse(f"{message} {full_name} {email}")