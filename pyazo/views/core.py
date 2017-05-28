from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(req):
    """

    """
    return render(req, 'core/index.html')
