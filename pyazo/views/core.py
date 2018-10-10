"""pyazo core views"""
import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from pyazo.models import Upload

LOGGER = logging.getLogger(__name__)

class IndexView(LoginRequiredMixin, TemplateView):
    """Show overview of uploads"""

    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        upload_filter = Q()
        if not self.request.user.is_superuser:
            upload_filter = Q(user=self.request.user) | Q(user__isnull=True)
        # Per Default, on a 1080p screen, there are 7 rows with 12 tiles => 84
        images = Paginator(Upload.objects.filter(upload_filter).order_by('-id'), 84)

        page = self.request.GET.get('page')
        try:
            context['uploads'] = images.page(page)
        except PageNotAnInteger:
            context['uploads'] = images.page(1)
        except EmptyPage:
            context['uploads'] = images.page(images.num_pages)
        return context
