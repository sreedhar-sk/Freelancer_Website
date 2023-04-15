from django.shortcuts import get_object_or_404,render,redirect
from django.core.exceptions import *
from django.http import HttpResponse,HttpResponseRedirect
from main.models import *
from django.db.models.functions import Lower
from django.contrib.auth.forms import UserChangeForm
from .forms import *
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils import timezone
# Create your views here.

# developed on sprint 2
def search(request): # function to render the search page
	if(request.method=="POST"):
		searchvalue=request.POST['searchvalue']
		searchby=request.POST.get('keyword')
		if searchby=="skills":
			providerobj=service_provider_info.objects.raw("""SELECT * FROM provider WHERE skills LIKE %s """, [("%"+searchvalue+"%")])
			log=Audit.objects.create(
				user=request.user,
				action='Search By Skills',
				details=f'Search for "{searchvalue}" under Skills Category',
				)
			log.timestamp_local = timezone.localtime(log.timestamp)
			log.save()
		elif searchby == "service":
			providerobj=service_provider_info.objects.raw("""SELECT * FROM provider WHERE service LIKE %s """, [("%"+searchvalue+"%")])
			log=Audit.objects.create(
		        user=request.user,
		        action='Search By Service',
		        details=f'Search for "{searchvalue}" under Service Category',
		        )
			log.timestamp_local = timezone.localtime(log.timestamp)
			log.save()
		elif searchby == "location":
			providerobj=service_provider_info.objects.raw("""SELECT * FROM provider WHERE location LIKE %s """, [("%"+searchvalue+"%")])
			log=Audit.objects.create(
		        user=request.user,
		        action='Search By Location',
		        details=f'Search for "{searchvalue}" under Location Category',
		        )
			log.timestamp_local = timezone.localtime(log.timestamp)
			log.save()
		elif searchby == "name":
			providerobj=service_provider_info.objects.raw("""SELECT * FROM provider WHERE first_name LIKE %s OR last_name LIKE %s """, [("%"+searchvalue+"%"),("%"+searchvalue+"%")])
			log=Audit.objects.create(
		        user=request.user,
		        action='Search By Name',
		        details=f'Search for "{searchvalue}" under Name Category',
		        )
			log.timestamp_local = timezone.localtime(log.timestamp)
			log.save()
		elif searchby=="toggle": # search by service catogories functionality
			serviceobj=service_provider_info.objects.all().order_by(Lower("service"))
			copy1 = []
			copy2 = []
			for data in serviceobj:
				if data.service not in copy1:
					copy1.append(data.service)
					copy2.append(data)
				serviceobj = copy2
			log=Audit.objects.create(
		        user=request.user,
		        action='Search By Service Category',
		        details=f'Search for Search By Service Category',
		        )
			log.timestamp_local = timezone.localtime(log.timestamp)
			log.save()
			return render(request,"userprofile/search.html",{'serviceobj':serviceobj}) #here search.html is rendered

		else:
			providerobj=service_provider_info.objects.raw("""SELECT * FROM provider WHERE first_name LIKE %s OR last_name LIKE %s OR skills LIKE %s """, [("%"+searchvalue+"%"),("%"+searchvalue+"%"),("%"+searchvalue+"%")])
			log=Audit.objects.create(
		        user=request.user,
		        action='General Search',
		        details=f'Search for Keyword "{searchvalue}".',
		        )
			log.timestamp_local = timezone.localtime(log.timestamp)
			log.save()
		return render(request,"userprofile/search.html",{'searchvalue':searchvalue,'providerobj':providerobj})
	else:
		providerobj=service_provider_info.objects.raw("""SELECT * FROM provider ORDER BY ratings DESC""")
		return render(request,"userprofile/search.html",{'providerobj':providerobj})

# developed on sprint 2
def ticket_form(request): # function to render the post a project page
	submitted=False
	if request.method == "POST":
		form = ticketform(request.POST)
		if form.is_valid():
			form.save()
			log=Audit.objects.create(
		        user=request.user,
		        action='Post A Project',
		        details=f'Posted A Project Successfully',
		        )
			log.timestamp_local = timezone.localtime(log.timestamp)
			log.save()
			last_id=(ticket_info.objects.last()).id
			ticket_info.objects.filter(id=last_id).update(users_ticket=request.user)
			return HttpResponseRedirect('/tickets?submitted=True')
	else:
		form=ticketform
		if 'submitted' in request.GET:
			submitted=True
	return render(request,"userprofile/ticketform.html",{'form': form,'submitted':submitted}) #here the ticketform.html is rendered

def ticket_list(request):
	ticketobj=ticket_info.objects.raw("""SELECT * FROM ticket ORDER BY hourly_rate DESC""")
	log=Audit.objects.create(
		user=request.user,
		action='View Tickets',
		details=f'You had a look at the list of the available tickets',
		)
	log.timestamp_local = timezone.localtime(log.timestamp)
	log.save()
	return render(request,"userprofile/tickets_list.html",{"ticketobj":ticketobj})

def edit_profile(request):
    if request.method == 'POST':
        form = EditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            log=Audit.objects.create(
				user=request.user,
				action='Edit Profile',
				details=f'You have Successfully updated your profile',
				)
            log.timestamp_local = timezone.localtime(log.timestamp)
            log.save()
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
		provider_name=provider.first_name+" "+provider.last_name
		log=Audit.objects.create(
			user=request.user,
			action='Wish List Removed',
			details=f'You have Successfully removed "{provider.first_name+" "+provider.last_name}" from your wishlist',
			)
		log.timestamp_local = timezone.localtime(log.timestamp)
		log.save()
	else:
		provider.users_wishlist.add(request.user)
		log=Audit.objects.create(
			user=request.user,
			action='Wish List Added',
			details=f'You have Successfully added "{provider.first_name+" "+provider.last_name}" to your wishlist',
			)
		log.timestamp_local = timezone.localtime(log.timestamp)
		log.save()
	return HttpResponseRedirect(request.META["HTTP_REFERER"])

def add_to_cart(request, id):
	provider=get_object_or_404(service_provider_info,id=id)
	if provider.users_cart.filter(id=request.user.id).exists():
		provider.users_cart.remove(request.user)
		log=Audit.objects.create(
			user=request.user,
			action='Removed from Cart',
			details=f'You have Successfully removed "{provider.first_name+" "+provider.last_name}" from your cart',
			)
		log.timestamp_local = timezone.localtime(log.timestamp)
		log.save()
	else:
		provider.users_cart.add(request.user)
		log=Audit.objects.create(
			user=request.user,
			action='Added to Cart',
			details=f'You have Successfully added "{provider.first_name+" "+provider.last_name}" to your cart',
			)
		log.timestamp_local = timezone.localtime(log.timestamp)
		log.save()
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
				log=Audit.objects.create(
					user=request.user,
					action='Update Service Provider Profile',
					details=f'You have Successfully updated your service provider profile',
					)
				log.timestamp_local = timezone.localtime(log.timestamp)
				log.save()
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
				log=Audit.objects.create(
					user=request.user,
					action='Create Service Provider Profile',
					details=f'You have Successfully created your service provider profile',
					)
				log.timestamp_local = timezone.localtime(log.timestamp)
				log.save()
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
	serviceprovider=service_provider_info.objects.filter(user_provider=request.user).values("service")
	ticketobj=[]
	if serviceprovider:
		provide_service=serviceprovider[0]["service"]
		ticketobj=ticket_info.objects.filter(service=provide_service)
	log=Audit.objects.create(
		user=request.user,
		action='View Dashboard',
		details=f'You have Visited your Dashboard',
		)
	log.timestamp_local = timezone.localtime(log.timestamp)
	log.save()
	return render(request, "userprofile/profile.html",{"skillsobj":skillsobj,"locationobj":locationobj,"ticketobj":ticketobj})
def your_tickets(request):
	ticketobj=ticket_info.objects.filter(users_ticket=request.user)
	return render(request,"userprofile/your_tickets.html",{"ticketobj":ticketobj})
# developed on sprint 3
def invite(request):  # function to render the invite a friend page
	if request.method == "POST":
		form = InviteForm(request.POST)

		if form.is_valid():
			name=form.cleaned_data['name']
			toaddress=[form.cleaned_data['email']]
			sendfrom='settings.EMAIL_HOST_USER'
			content="Hi "+ name + ", \n"+ form.cleaned_data['content']
			subject=str(request.user).capitalize()+" invited you to Find Your Programmer"
			send_mail(subject,content,sendfrom,toaddress)
			log=Audit.objects.create(
				user=request.user,
				action='Invite A Friend',
				details=f'You have invited your friend - "{name}"',
				)
			log.timestamp_local = timezone.localtime(log.timestamp)
			log.save()
	else:
		form = InviteForm(initial={"content": "Hi, Sign-Up with Find Your Programmer through this link https://siva613.pythonanywhere.com/login/"})
	return render(request,"userprofile/invite.html",{"form":form}) # here the invite.html is rendered

def activity(request):
	activityobj=Audit.objects.filter(user=request.user)
	return render(request,"userprofile/activity.html",{"activityobj":activityobj})


# developed on sprint 3
def mainchat(request): # function to render the chat page
    users = User.objects.exclude(id=request.user.id)
    context = {'users': users}
    return render(request, 'userprofile/mainchat.html', context)# here the mainchat.html is rendered

def chat(request, sender_id, recipient_id):
	users = User.objects.exclude(id=request.user.id)
	chats = Chat.objects.filter(sender=sender_id, recipient=recipient_id) | Chat.objects.filter(sender=recipient_id, recipient=sender_id)
	context = {'users': users, 'chats': chats, 'sender_id':sender_id, 'recipient_id':recipient_id}
	return render(request, 'userprofile/chat.html', context)


def send_message(request, sender_id, recipient_id):
	users = User.objects.exclude(id=request.user.id)
	chats = Chat.objects.filter(sender=sender_id, recipient=recipient_id) | Chat.objects.filter(sender=recipient_id, recipient=sender_id)
	if request.method == 'POST':
		form = ChatForm(request.POST)
		if form.is_valid():
			message = form.cleaned_data['message']
			chat = Chat(sender=sender_id, recipient=recipient_id, message=message)
			chat.save()
			return redirect('chat', sender_id=sender_id, recipient_id=recipient_id)
	else:
		form = ChatForm()
	context = {'users': users, 'chats': chats,'form': form,'sender_id':sender_id, 'recipient_id':recipient_id}
	return render(request, 'userprofile/send_message.html', context)
