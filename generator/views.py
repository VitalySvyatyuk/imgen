from django.shortcuts import render


async def index(request):
    context = {
    }
    return render(request, "index.html", context)
