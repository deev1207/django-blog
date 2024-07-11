# views.py
from django.shortcuts import redirect

def redirectToBlog(request):
    return redirect('index')  # 'blog-list' should be the name of your target URL pattern
