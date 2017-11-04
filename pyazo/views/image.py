"""
pyazo image views
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import ugettext as _

from pyazo.models import Upload


@login_required
def view(req, file_hash):
    """
    Show stats about image and allow user to claim it
    """
    img = Upload.objects.filter(sha512=file_hash)
    if not img.exists():
        raise Http404
    r_img = img.first()

    url_prefix = req.build_absolute_uri('/')

    views = r_img.uploadview_set.order_by('-viewee_date')[:10]
    return render(req, 'image/view.html', {
        'image': r_img,
        'url_prefix': url_prefix,
        'views': views
        })

@login_required
def claim(req, file_hash):
    """
    Attempt to claim a picture
    """
    images = Upload.objects.filter(sha512=file_hash)
    if not images.exists():
        raise Http404
    r_image = images.first()

    if req.method == 'POST' \
        and 'confirmdelete' in req.POST \
        and (req.user.is_superuser \
        or not r_image.user):
        # User confirmed deletion
        r_image.user = req.user
        r_image.save()
        messages.success(req, _('Upload successfully claimed'))
        return redirect(reverse('core-image_view', kwargs={'file_hash': file_hash}))

    return render(req, 'core/generic_delete.html', {
        'object': 'Upload %s' % r_image.md5,
        'delete_url': reverse('core-image_claim', kwargs={
            'file_hash': file_hash
            }),
        'action': _('claim'),
        'primary_action': _('Confirm Claim')
        })
