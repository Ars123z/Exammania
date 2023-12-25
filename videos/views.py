from django.shortcuts import render
from .models import Topic, Video

# Create your views here.
def main(request):
    return render(request, "videos/main.html")

def chemistry(request, topic, no):
    topic= Topic.objects.get(title=topic)
    videos= Video.objects.filter(topic=topic).order_by("code")
    video1= videos[no]
    no= no + 1
    temp= {
        "no": no,
        "video1": video1,
        "topic":topic,
        "videos":videos,
    }
    print(videos)
    return render(request, "videos/video.html", temp)

def physics(request, topic, no):
    topic= Topic.objects.get(title=topic)
    videos= Video.objects.filter(topic=topic).order_by("code")
    video1= videos[no]
    no= no + 1
    temp= {
        "no": no,
        "video1": video1,
        "topic":topic,
        "videos":videos,
    }
    print(videos)
    return render(request, "videos/video.html", temp)

def maths(request, topic, no):
    topic= Topic.objects.get(title=topic)
    videos= Video.objects.filter(topic=topic).order_by("code")
    video1= videos[no]
    no= no + 1
    temp= {
        "no": no,
        "video1": video1,
        "topic":topic,
        "videos":videos,
    }
    print(videos)
    return render(request, "videos/video.html", temp)