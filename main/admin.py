from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import *

admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(Actor)
admin.site.register(Review)
admin.site.register(Like)

