from django.urls import path
from .views import homePageView
from .views import getEventLogs
from .views import getHostEventLogs
from .views import addLogUI
from .views import addLog
from .views import superAdminUI
from .views import getGameModel
from .views import hostView
from .views import sendAction
from django.contrib import admin
from django.urls import path, include # new
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('wolves/', homePageView, name='home'),
    path('wolves/getEventLogs', getEventLogs, name="getEventLogs"),
    path('wolves/getHostEventLogs', getHostEventLogs, name="getHostEventLogs"),
    path('wolves/addLogUI', addLogUI, name="addLogUI"),
    path('wolves/addLog', addLog, name="addLog"),
    path('wolves/superAdminUI', superAdminUI, name="superAdminUI"),
    path('wolves/getGameModel', getGameModel, name="getGameModel"),
    path('wolves/host5990', hostView, name="hostView"),
    path('wolves/sendAction', sendAction, name="sendAction"),
    path(
        "favicon.ico",
        RedirectView.as_view(url=staticfiles_storage.url("favicon.ico"))
    ),

]
