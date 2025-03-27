from django.shortcuts import render


def diary_page(request):
    return render(request, 'diary/diary.html')