from django.urls import path

from codes.views import CodesView, CodeView, UploadCsvView

urlpatterns = [
    path("", CodesView.as_view(), name='codes'),
    path("upload/", UploadCsvView.as_view(), name='upload'),
    path("<pk>", CodeView.as_view(), name='code'),

]
