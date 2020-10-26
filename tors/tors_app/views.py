from django.shortcuts import render, HttpResponse, redirect
from tors_app.models import *
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.core.mail import send_mail, EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
###
from django.core.mail import get_connection, send_mail
from django.core.mail.message import EmailMessage
###
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth import login, logout, authenticate


def index(request):
    tours = tour.objects.all()
    return render(request, 'tour/index.html', {'tours': tours})

def tour_info(request, tour_id):
    tours = tour.objects.get(pk = tour_id)
    return render(request, 'tour/view_tour.html', {'tours': tours})

def reserve_tour(request, tour_id):
    tours = tour.objects.get(pk = tour_id)
    if request.method == 'POST':
        c_name = request.POST.get('name')
        c_phone = request.POST.get('phone')
        c_email = request.POST.get('email')
        c_date = request.POST.get('date')
        try:
            a = User.objects.get(username=c_email)
            
        except ObjectDoesNotExist:
            user = User.objects.create_user(c_email)
            password = User.objects.make_random_password()
            user.password = password
            user.set_password(user.password)
            user.first_name = c_name
            user.email = c_email
            user.save()
            subject, from_email, to = 'TORS ACcount Created', 'workmail052020@gmail.com', c_email
   
            html_content = render_to_string('email/new_customer.html', {'name':c_name, 'u': c_email, 'pwd': password}) 
            text_content = strip_tags(html_content)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        except IntegrityError:
            pass
        try:
            existing_customer = customer.objects.get(phone=c_phone)
            new_reservation = reservation(fk_customer= existing_customer, fk_tour=tours, reservation_date= datetime.today(), tour_date= c_date, status= status.objects.get(pk=1))
            new_reservation.save()
            subject, from_email, to = 'Reservation Done', 'workmail052020@gmail.com', c_email
   
            html_content = render_to_string('email/new_reservation.html', {'name':c_name, 'tour': tours.name, 'r_date': datetime.today(), 't_date': c_date}) 
            text_content = strip_tags(html_content)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return HttpResponse('Tour Reservation Successful')
        except ObjectDoesNotExist:
            new_customer = customer(name= c_name, phone= c_phone, email= c_email)
            new_customer.save()
            existing_customer = customer.objects.get(phone=c_phone)

            new_reservation = reservation(fk_customer= existing_customer, fk_tour=tours, reservation_date= datetime.today(), tour_date= c_date, status= status.objects.get(pk=1))
            new_reservation.save()
            subject, from_email, to = 'Reservation Done', 'workmail052020@gmail.com', c_email
   
            html_content = render_to_string('email/new_reservation.html', {'name':c_name, 'tour': tours.name, 'r_date': datetime.today(), 't_date': c_date}) 
            text_content = strip_tags(html_content)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return HttpResponse('Tour Reservation Successful')
    return render(request, 'tour/reserve_tour.html', {'tours': tours})

def tors_login(request):
    if request.method == "POST":
        if request.POST.get('username') != None or request.POST.get('username') != '':
            usrname = request.POST.get('username')
            pwd = request.POST.get('pwd')
           
            user = authenticate(request, username=usrname, password=pwd)
            
            if user is not None and user.is_active:
                login(request, user)
                try:

                    all_tours = reservation.objects.filter(fk_customer= customer.objects.get(email=usrname))
                    return redirect('home')
                except ObjectDoesNotExist:
                    return HttpResponse("User Account Not Found")
            else:
                return HttpResponse("Invalid Credentials")
    return render(request, 'customer/login.html')

def cutomer_home(request):
    print(request.user)
    all_tours = reservation.objects.filter(fk_customer= customer.objects.get(email=request.user))
    return render(request, 'customer/dashboard.html', {'alltours': all_tours,})

def reservation_info(request, reserve_id):
    reservation_list = reservation.objects.get(pk = reserve_id)
    return render(request, 'customer/view_reservation.html', {'reservation': reservation_list })

def cancel_tour(request, reserve_id):
    reservation_list = reservation.objects.get(pk = reserve_id)
    reservation_list.status=status.objects.get(pk=2)
    reservation_list.save()
    subject, from_email, to = 'TORS ACcount Created', 'workmail052020@gmail.com', reservation_list.fk_customer.email  
    html_content = render_to_string('email/new_customer.html', {'tour': reservation_list.fk_tour.name,'name': reservation_list.fk_customer.name ,'t_date': reservation_list.tour_date}) 
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return HttpResponse("Reservation Cancelled Succesfully")

def feedback(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        msg = request.POST.get('message')
        subject, from_email, to = 'New Feedback For TORS', 'workmail052020@gmail.com', 'workmail052020@gmail.com' 
        html_content = render_to_string('email/feedback_tors.html', {'name': name,'email': email ,'feedback_msg': msg}) 
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    return render(request, 'tour/feedback.html')