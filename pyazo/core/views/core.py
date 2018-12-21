"""pyazo core views"""
import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import Http404
from django.views.generic import TemplateView

from pyazo.core.models import Collection, Upload

LOGGER = logging.getLogger(__name__)

class IndexView(LoginRequiredMixin, TemplateView):
    """Show overview of uploads"""

    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        upload_filter = Q()
        if not self.request.user.is_superuser:
            upload_filter = Q(user=self.request.user) | Q(user__isnull=True)
        # Filter by collection if set
        if 'collection' in self.request.GET:
            # Check if user has access to collection
            if not Collection.objects.filter(
                    name=self.request.GET.get('collection'),
                    owner=self.request.user).exists():
                raise Http404
            upload_filter &= Q(collection__name=self.request.GET.get('collection'))
            # Set collection name so we can show in the template
            context['collection'] = self.request.GET.get('collection')
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
