from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound,\
HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponseRedirect
from models import AcortadorUrls
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def pedirFormulario():
    formulario = '<form action="" method="POST" accept-charset="UTF-8">' +\
                 'Acorta url: <input type="text" name="url">' +\
                 '<input type="submit" value="Enviar"></form>'
    return formulario

def acortarUrl(link):
    http = "http://"
    https = "https://"
    if link.startswith(http) or link.startswith(https):
        link = link
    else:
        link = http + link
    return link

def guardarBD(urlAcortada):
    try:
        encontrado = AcortadorUrls.objects.get(URL=urlAcortada)
    except AcortadorUrls.DoesNotExist:
        encontrado = AcortadorUrls(URL=urlAcortada)
        encontrado.save()
    return encontrado
        

@csrf_exempt
def identificarMetodo(request):
    if request.method == "GET":
        Todas = AcortadorUrls.objects.all()
        formulario = pedirFormulario()
        todasUrls = ""
        url = ""
        for urls in Todas:
           url = "<p>{Url Larga: " + urls.URL + ", Url Corta: "+ str(urls.id) + "}<p>"
           todasUrls += url + "<br/>"
           formulario += "<br/>"
        return HttpResponse(formulario + todasUrls)
    elif request.method == "POST":
        link = request.POST.get("url")
        urlAcortada = acortarUrl(link)
        encontrado = guardarBD(urlAcortada)
        enlace = "<p>url real: <a href=" + urlAcortada + ">" + urlAcortada + "</a></p>"
        enlace += "<p>url acortada: <a href=" + str(encontrado.id) + ">" +\
                          "localhost:PORT/" + str(encontrado.id) + "</a></p>"
        return HttpResponse(enlace)


def redireccion(request, recurso):
    try:
        url = AcortadorUrls.objects.get(id=recurso)
    except AcortadorUrls.DoesNotExist:
        return HttpResponseNotFound(str(id) + " no encontrado")
    return HttpResponseRedirect(url.URL)

def notfound(request, recurso):
    salida = ("404 Not found: " + recurso)
    return HttpResponseNotFound(salida)







          
