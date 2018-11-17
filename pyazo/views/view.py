"""pyazo viewing views"""
from logging import getLogger

from django.db.models import Q, QuerySet
from django.http import Http404, HttpRequest, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.generic import View

from pyazo.models import Upload
from pyazo.models import UploadView as UploadViewObject
from pyazo.tasks import make_thumbnail
from pyazo.utils import get_remote_ip, get_reverse_dns
from pyazo.utils.files import get_mime_type

LOGGER = getLogger(__name__)

@method_decorator(cache_control(max_age=3600), name='dispatch')
class UploadViewFile(View):
    """View to show upload"""

    @staticmethod
    def count_view(upload: Upload, request: HttpRequest):
        """Create UploadView entry from request"""
        client_ip = get_remote_ip(request)
        client_dns = get_reverse_dns(client_ip)
        user_agent = request.META['HTTP_USER_AGENT'] if 'HTTP_USER_AGENT' in request.META else ''
        UploadViewObject.objects.create(
            upload=upload,
            viewee_ip=client_ip,
            viewee_dns=client_dns,
            viewee_user_agent=user_agent)
        LOGGER.info("Logged view for %s (%s) viewing '%s'", client_ip, client_dns, upload.md5)

    def resolve_hash(self, file_hash: str) -> QuerySet:
        """Resolve hash to QuerySet based on string length"""
        query = Q()
        hash_length = len(file_hash)
        if hash_length == 16:  # SHA512 (short)
            query &= Q(sha512__startswith=file_hash)
        elif hash_length == 32:  # MD5
            query &= Q(md5=file_hash)
        elif hash_length == 64:  # SHA256
            query &= Q(sha256=file_hash)
        elif hash_length == 128:  # SHA512
            query &= Q(sha512=file_hash)
        return Upload.objects.filter(query)

    @cache_control(max_age=3600)
    def dispatch(self, request: HttpRequest, **kwargs) -> HttpResponse:
        """Return uploaded data"""
        matching = self.resolve_hash(kwargs.get('file_hash'))
        if not matching.exists():
            raise Http404
        upload = matching.first()
        content_type = get_mime_type(upload.file.name)
        if 'thumb' in request.GET:
            if not upload.thumbnail:
                try:
                    make_thumbnail.delay(upload.pk).get()
                except Exception: # pylint: disable=broad-except
                    # Catch any kind of redis or Celery error, so we return nothing
                    return HttpResponse(status=400)
                upload.refresh_from_db()
            return HttpResponse(upload.thumbnail.read(), content_type='image/png')
        self.count_view(upload, request)
        return HttpResponse(upload.file.read(), content_type=content_type)
