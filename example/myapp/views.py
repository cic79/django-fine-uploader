# !/usr/bin/env python
# encoding:UTF-8

import json

from django.http.response import HttpResponse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from django_fine_uploader.fineuploader import SimpleFineUploader
from django_fine_uploader.forms import FineUploaderUploadForm
from django_fine_uploader.views import FineUploaderView
from .models import FineFile


class HomeView(generic.TemplateView):
    template_name = 'myapp/home.html'


class CustomView(generic.TemplateView):
    template_name = 'myapp/example_custom.html'


class GalleryView(generic.TemplateView):
    template_name = 'myapp/example_gallery.html'


class RowView(generic.TemplateView):
    template_name = 'myapp/example_row.html'


class ExampleView(generic.TemplateView):
    template_name = 'myapp/old/example.html'


class MyAppUploaderView(FineUploaderView):
    """FineUploaderView is basically a django.views.generic.FormView.
    So, you can use mixins or extends this view as you wish.

    You may want to see the code:
    django_fine_uploader.views.FineUploaderView

    Or you can create your own view, from scratch, and just take
    advantage from the upload handlers:
    django_fine_uploader.fineuploader.SimpleFineUploader
    OR
    django_fine_uploader.fineuploader.ChunkedFineUploader
    """
    # Do some stuff, override methods, change settings...


class NotConcurrentUploaderView(FineUploaderView):
    """Example of a chunked, but NOT concurrent upload.
    Disabling concurrent uploads per view.

    Remember, you can turn off concurrent uploads on your settings, with:
    FU_CONCURRENT_UPLOADS = False
    """
    @property
    def concurrent(self):
        return False

    def form_valid(self, form):
        self.process_upload(form)
        return self.make_response({'success': True})


class SimpleCustomUploaderView(generic.FormView):
    """Example of a not concurrent not chunked upload. A.K.A. Simple upload.
    """
    form_class = FineUploaderUploadForm

    def form_valid(self, form):
        """You could use the ChunkedFineUploader too, it will detect
        it's not a chunked upload, and it will upload anyway.
        from django_fine_uploader.fineuploader import ChunkedFineUploader
        upload = ChunkedFineUploader(form.cleaned_data, concurrent=False)
        ..but if you want a ~ real ~ simple upload:
        """
        upload = SimpleFineUploader(form.cleaned_data)
        upload.save()
        return HttpResponse(json.dumps({'success': True}), content_type="application/json")

    def form_invalid(self, form):
        data = {'success': False, 'error': '%s' % repr(form.errors)}
        return HttpResponse(json.dumps(data), content_type="application/json", status=400)


class CustomFineUploaderView(FineUploaderView):
    """Let's get the file url and add to the json response, so we can
    get it on the frontend. More info on `onComplete` callback on
    myapp/example.html
    """
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(CustomFineUploaderView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.process_upload(form)
        data = {'success': True}
        if self.upload.finished:
            data['file_url'] = self.upload.url
            # Let's save in database?
            FineFile.objects.create(fine_file=self.upload.real_path)
        return self.make_response(data)
