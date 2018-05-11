"""pyazo core views"""
import logging

from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from pyazo.models import Upload

LOGGER = logging.getLogger(__name__)

@login_required
def index(request: HttpRequest) -> HttpResponse:
    """Show overview of newest images"""
    imgfilter = Q()
    if not request.user.is_superuser:
        imgfilter = Q(user=request.user) | Q(user__isnull=True)
    # Per Default, on a 1080p screen, there are 7 rows with 12 tiles => 84
    images = Paginator(Upload.objects.filter(imgfilter).order_by('-id'), 84)

    page = request.GET.get('page')
    try:
        page_instances = images.page(page)
    except PageNotAnInteger:
        page_instances = images.page(1)
    except EmptyPage:
        page_instances = images.page(images.num_pages)

    return render(request, 'core/index.html', {'images': page_instances})
