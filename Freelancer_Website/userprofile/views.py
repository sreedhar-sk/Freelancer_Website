from django.shortcuts import get_object_or_404,render
from django.core.exceptions import *
from django.http import HttpResponse,HttpResponseRedirect
from main.models import *
from django.db.models.functions import Lower
from django.contrib.auth.forms import UserChangeForm
from .forms import *
from django.contrib.auth.models import User
# Create your views here.


	
def search(request):
	if(request.method=="POST"):
		searchvalue=request.POST['searchvalue']
		searchby=request.POST.get('keyword')
		if searchby=="skills":
			providerobj=service_provider_info.objects.raw("""SELECT * FROM provider WHERE skills LIKE %s """, [("%"+searchvalue+"%")])
		elif searchby == "service":
			providerobj=service_provider_info.objects.raw("""SELECT * FROM provider WHERE service LIKE %s """, [("%"+searchvalue+"%")])

		elif searchby == "location":
			providerobj=service_provider_info.objects.raw("""SELECT * FROM provider WHERE location LIKE %s """, [("%"+searchvalue+"%")])

		elif searchby == "name":
			providerobj=service_provider_info.objects.raw("""SELECT * FROM provider WHERE first_name LIKE %s OR last_name LIKE %s """, [("%"+searchvalue+"%"),("%"+searchvalue+"%")])

		elif searchby=="toggle":
			serviceobj=service_provider_info.objects.all().order_by(Lower("service"))
			copy1 = []
			copy2 = []
			for data in serviceobj:
				if data.service not in copy1:
					copy1.append(data.service)
					copy2.append(data)
				serviceobj = copy2
			return render(request,"userprofile/search.html",{'serviceobj':serviceobj})

		else:
			providerobj=service_provider_info.objects.raw("""SELECT * FROM provider WHERE first_name LIKE %s OR last_name LIKE %s OR skills LIKE %s """, [("%"+searchvalue+"%"),("%"+searchvalue+"%"),("%"+searchvalue+"%")])
		return render(request,"userprofile/search.html",{'searchvalue':searchvalue,'providerobj':providerobj})
	else:
		providerobj=service_provider_info.objects.raw("""SELECT * FROM provider ORDER BY ratings DESC""")
		return render(request,"userprofile/search.html",{'providerobj':providerobj})

def ticket_form(request):
	submitted=False
	if request.method == "POST":
		form = ticketform(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/tickets?submitted=True')
	else:
		form=ticketform
		if 'submitted' in request.GET:
			submitted=True
	return render(request,"userprofile/ticketform.html",{'form': form,'submitted':submitted})

def ticket_list(request):
	ticketobj=ticket_info.objects.raw("""SELECT * FROM ticket ORDER BY hourly_rate DESC""")
	return render(request,"userprofile/tickets_list.html",{"ticketobj":ticketobj})

def edit_profile(request):
    if request.method == 'POST':
        form = EditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = EditForm(instance=request.user)

    return render(request, "userprofile/edit_profile.html", {"form": form})


def updateprofile(request):

	return render(request, "userprofile/updateprofile.html")

def wishlist(request):
	wishlistobj=service_provider_info.objects.filter(users_wishlist=request.user)
	return render(request, "userprofile/wishlist.html",{"wishlistobj":wishlistobj})

def add_to_wishlist(request, id):
	provider=get_object_or_404(service_provider_info,id=id)
	if provider.users_wishlist.filter(id=request.user.id).exists():
		provider.users_wishlist.remove(request.user)
	else:
		provider.users_wishlist.add(request.user)
	return HttpResponseRedirect(request.META["HTTP_REFERER"])

def add_to_cart(request, id):
	provider=get_object_or_404(service_provider_info,id=id)
	if provider.users_cart.filter(id=request.user.id).exists():
		provider.users_cart.remove(request.user)
	else:
		provider.users_cart.add(request.user)
	return HttpResponseRedirect(request.META["HTTP_REFERER"])

def cart(request):
	cartobj=service_provider_info.objects.filter(users_cart=request.user)
	return render(request, "userprofile/cart.html",{"cartobj":cartobj})

def provide_service(request):
	submitted=False
	is_available=False
	provider=service_provider_info.objects.filter(user_provider__isnull=False)
	for p in provider:
		if p.user_provider.id==request.user.id:
			is_available=True
			present_provider=service_provider_info.objects.get(id=p.id)
			break
	if(is_available):
		if request.method == "POST":
			form = ProvideServiceForm(request.POST,instance=present_provider)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/provide_service?submitted=True')
		else:
			form=ProvideServiceForm(instance=present_provider)
			if 'submitted' in request.GET:
				submitted=True
		return render(request,"userprofile/provide_service.html",{'form': form,'submitted':submitted})

	else:
		if request.method == "POST":
			form = ProvideServiceForm(request.POST)
			if form.is_valid():
				form.save()
				last_id=(service_provider_info.objects.last()).id
				service_provider_info.objects.filter(id=last_id).update(user_provider=request.user)
				return HttpResponseRedirect('/provide_service?submitted=True')
		else:
			form=ProvideServiceForm
			if 'submitted' in request.GET:
				submitted=True
	return render(request,"userprofile/provide_service.html",{'form': form,'submitted':submitted})

def profile(request):
	wishlistobj=service_provider_info.objects.filter(users_wishlist=request.user)
	skillsobj=service_provider_info.objects.filter(skills__in=[w.skills for w in wishlistobj])
	locationobj=service_provider_info.objects.filter(location__in=[w.location for w in wishlistobj])
	return render(request, "userprofile/profile.html",{"skillsobj":skillsobj,"locationobj":locationobj})