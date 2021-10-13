# pages/views.py
from django.http import HttpResponse
from django.template import loader
from .models import WolfGame
from django.views.decorators.csrf import csrf_exempt


wg = WolfGame()

def homePageView(request):
    template = loader.get_template('player_view.html')
    context = {}
    return HttpResponse(template.render(context, request))

def getEventLogs(request):
    latest = int(request.GET.get("latest"))
    return HttpResponse(wg.getLogAsString(latest))

def addLogUI(request):
    template = loader.get_template('add_log.html')
    context = {}
    return HttpResponse(template.render(context, request))

def addLog(request):
    newLog = request.GET.get("newLog")
    #print("newLog="+newLog)
    wg.addLog(newLog)
    return HttpResponse("ok")

def superAdminUI(request):
    template = loader.get_template('super_admin.html')
    return HttpResponse(template.render({}, request))

def getGameModel(request):
    command = request.GET.get("command")
    wg.evalCommand(command)
    return HttpResponse(wg.getGameModel())

def hostView(request):
    template = loader.get_template('host_view.html')
    context = {}
    return HttpResponse(template.render(context, request))

@csrf_exempt
def sendAction(request):
    if request.method == 'POST':
        return HttpResponse(wg.sendActionViaPost(request.body.decode("utf-8")))
    else:
        return HttpResponse(wg.sendAction(request.GET.get("latest"), request.GET.get("action"), request.GET.get("p1"), request.GET.get("p2"), request.GET.get("p3")))