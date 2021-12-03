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

urlpatterns = [
    path('', homePageView, name='home'),
    path('getEventLogs', getEventLogs, name="getEventLogs"),
    path('getHostEventLogs', getHostEventLogs, name="getHostEventLogs"),
    path('addLogUI', addLogUI, name="addLogUI"),
    path('addLog', addLog, name="addLog"),
    path('superAdminUI', superAdminUI, name="superAdminUI"),
    path('getGameModel', getGameModel, name="getGameModel"),
    path('host5990', hostView, name="hostView"),
    path('sendAction', sendAction, name="sendAction")

]
