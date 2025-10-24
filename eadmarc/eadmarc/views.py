from django.shortcuts import render

def home_view(request):
    images = [
        "farm1.png", "farm2.png", "farm3.png", "farm4.png", "farm5.png",
        "farm6.png", "farm7.png", "farm8.png", "farm9.png", "farm10.png"
    ]
    return render(request, "home.html", {"images": images})
