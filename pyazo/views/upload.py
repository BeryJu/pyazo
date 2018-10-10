"""pyazo upload views"""
import logging
from urllib.parse import urljoin

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.utils import DataError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from pyazo.forms.view import CollectionAssignForm
from pyazo.models import Collection, Upload, UploadView, save_from_post
from pyazo.utils import get_remote_ip, get_reverse_dns

LOGGER = logging.getLogger(__name__)


class View(LoginRequiredMixin, TemplateView):
    """Show statistics about image and allow user to manage it."""

    template_name = 'upload/view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['upload'] = get_object_or_404(Upload, sha512=self.kwargs.get('file_hash'))
        context['url_prefix'] = self.request.build_absolute_uri('/')
        context['views'] = context['upload'].uploadview_set.order_by('-viewee_date')[:10]
        context['collections'] = Collection.objects.filter(owner=self.request.user)
        context['forms'] = {
            'collection': CollectionAssignForm(
                prefix='collection',
                data=self.request.POST if any(
                    'collection' in k for k in self.request.POST.keys()) else None
            )
        }
        return context


class ClaimView(LoginRequiredMixin, TemplateView):
    """Claim an upload"""

    template_name = 'core/generic_delete.html'

    def post(self, request: HttpRequest, file_hash: str) -> HttpResponse:
        """Claim upload to user (only if upload has no owner yet or user is superuser)"""
        upload = get_object_or_404(Upload, sha512=file_hash)
        if request.user.is_superuser or not upload.user:
            upload.user = request.user
            upload.save()
            messages.success(request, _('Upload successfully claimed'))
        else:
            messages.warning(request, _('Permission denied'))
        return redirect(reverse('upload_view', kwargs={'file_hash': file_hash}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        upload = get_object_or_404(Upload, sha512=self.kwargs.get('file_hash'))
        context['object'] = 'Upload %s' % upload.md5,
        context['delete_url'] = reverse('upload_claim', kwargs={
            'file_hash': self.kwargs.get('file_hash')
        }),
        context['action'] = _('claim'),
        context['primary_action'] = _('Confirm Claim')

@csrf_exempt
def upload(request: HttpRequest) -> HttpResponse:
    """Main upload handler. Fully Gyazo compatible."""
    if 'id' in request.POST and 'imagedata' in request.FILES:
        client_ip = get_remote_ip(request)
        client_dns = get_reverse_dns(client_ip)

        file = save_from_post(request.FILES['imagedata'].read())

        new_upload = Upload(
            file=file,
            type=0)

        # Run auto-claim
        if settings.AUTO_CLAIM_ENABLED and 'username' in request.POST:
            matching = User.objects.filter(username=request.POST.get('username'))
            # pylint: disable=no-member
            if matching.exists():
                # pylint: disable=no-member
                new_upload.user = matching.first()
                LOGGER.debug("Auto-claimed upload to user '%s'", request.POST.get('username'))

        new_upload.save()

        try:
            uag = request.META['HTTP_USER_AGENT'] if 'HTTP_USER_AGENT' in request.META else ''
            new_upload_view = UploadView(
                upload=new_upload,
                viewee_ip=client_ip,
                viewee_dns=client_dns,
                viewee_user_agent=uag
                )
            new_upload_view.save()
        except DataError:
            LOGGER.info("Failed to create initial view with rIP '%r'", client_ip)

        LOGGER.info("Uploaded %s from %s", new_upload.filename, client_ip)

        # Generate url for client to open
        upload_prop = settings.DEFAULT_RETURN_VIEW.replace('view_', '')
        upload_hash = getattr(new_upload, upload_prop, 'sha256')
        url = reverse(settings.DEFAULT_RETURN_VIEW, kwargs={'file_hash': upload_hash})
        full_url = urljoin(settings.EXTERNAL_URL, url)
        return HttpResponse(full_url)
    return HttpResponse(status=400)


@login_required
def upload_browser(req):
    """Handle uploads from browser"""
    if req.method == 'POST':
        # do stuff
        for filen in req.FILES:
            client_ip = get_remote_ip(req)
            client_dns = get_reverse_dns(client_ip)

            file = save_from_post(req.FILES[filen].read())

            new_upload = Upload(
                file=file,
                type=0,
                user=req.user)
            new_upload.save()

            try:
                uag = req.META['HTTP_USER_AGENT'] if 'HTTP_USER_AGENT' in req.META else ''
                new_upload_view = UploadView(
                    upload=new_upload,
                    viewee_ip=client_ip,
                    viewee_dns=client_dns,
                    viewee_user_agent=uag
                    )
                new_upload_view.save()
            except DataError:
                LOGGER.info("Failed to create initial view with rIP '%r'", client_ip)

            LOGGER.info("Uploaded %s from %s", new_upload.filename, client_ip)
    return render(req, 'upload/upload.html')
