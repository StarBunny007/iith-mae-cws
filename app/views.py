# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.template import RequestContext
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from .form import orderForm,LoginForm,RegisterForm , DecisionForm , StatusForm
from .models import Order, Approver , Status
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.timezone import localtime, now
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import hashlib
from django.shortcuts import render
from django.template import RequestContext
# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.utils.timezone import localtime, now
from django.contrib.sites.shortcuts import get_current_site
import hashlib
# import xlsxwriter
from django.http import HttpResponse
from .models import Order

def handler404(request,exception):
    return render(request, 'app/404.html', status=404)
    

def handler500(request):
    return render(request, 'app/index.html')
    

def index(request):
	approver = Approver.objects.all()
	approver = approver[0]
	return render(request,'app/index.html',{'approver':approver})

# views.py
def order(request):
    if request.method == "POST":
        form = orderForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                data = form.cleaned_data
                new_object = Order(
                    name=data['name'],
                    mail=data['mail'],
                    mobile=data['mobile'],
                    title=data['title'],
                    work=data['work'],
                    worktype=data['worktype'],
                    prof_name=data['prof_name'],
                    prof_mail=data['prof_mail'],
                    file=request.FILES.get('file'),
                    uploaded_at=localtime(now())
                )
                new_object.save()

                order = Order.objects.get(id=new_object.id)
                try:
                    current_site = get_current_site(request)
                    hash_prof = hashlib.md5(order.prof_mail.encode('utf-8')).hexdigest()
                    message = (
                        f"Dear Sir/Madam \r\n\r\n {data['name']} has submitted a Work request with you as the faculty Guide/Incharge."
                        f"This Work request is awaiting your approval for further processing. Please click on the following link for details and approval. \r\n\r\n"
                        f"{current_site.domain}/order_decision/{order.id}/{hash_prof}/ \r\n\r\nThanking You\r\nIITH CWS\r\n"
                    )
                    mail_subject = 'IITH CWS Work Request Approval'
                    to_email = data['prof_mail']
                    email = EmailMessage(mail_subject, message, to=[to_email])
                    email.send()

                    hash_mail = hashlib.md5(order.mail.encode('utf-8')).hexdigest()
                    message2 = (
                        f"Hello \r\n\r\n We have successfully received your Work request to Central Workshop."
                        f"Please use the link below for more details and to track the Work request status. \r\n\r\n"
                        f"{current_site.domain}/details/{order.id}/{hash_mail}/ \r\n\r\nThanking You\r\nIITH CWS\r\n"
                    )
                    mail_subject2 = 'IITH CWS Work request'
                    to_email2 = data['mail']
                    email = EmailMessage(mail_subject2, message2, to=[to_email2])
                    email.send()
                except Exception as e:
                    print(str(e))
                    order.delete()
                    message = "There is something wrong. Try again later: 1"
                    return render(request, 'app/form.html', {'form': form, 'message': message})

                return HttpResponseRedirect("/orders")
            except Exception as e:
                print(str(e))
                order.delete()
                message = "There is something wrong. Try again later: 2"
                return render(request, 'app/form.html', {'form': form, 'message': message})
        else:
            message = "There is something wrong with your form. Try again: 3"
            return render(request, 'app/form.html', {'form': form, 'message': message})
    else:
        form = orderForm()
        return render(request, 'app/form.html', {'form': form})

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from .models import Order

def all_orders(request):
    orders_list = Order.objects.all().order_by('-uploaded_at')
    page = request.GET.get('page')
    paginator = Paginator(orders_list, 20)  # Show 20 orders per page
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        orders = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        orders = paginator.page(paginator.num_pages)
    category = "ALL WORK REQUESTS"

    return render(request, 'app/orders.html', {'orders': orders, 'category': category})
def pending_orders(request):
	orders_list = Order.objects.filter(
        Q(approval1="Pending") | Q(approval2="Pending") | Q(approval3="Pending")
    ).order_by('-uploaded_at')
	page = request.GET.get('page')
	paginator = Paginator(orders_list, 20)
	try:
		orders = paginator.page(page)
	except PageNotAnInteger:
		orders = paginator.page(1)
	except EmptyPage:
		orders = paginator.page(paginator.num_pages)
	category = "PENDING WORK REQUESTS"
	return render(request,'app/orders.html',{'orders':orders,'category':category})

def unapproved_orders(request):
    orders_list = Order.objects.filter(
        Q(approval1="Pending") | Q(approval2="Pending") | Q(approval3="Pending")
    ).order_by('-uploaded_at')
    
    page = request.GET.get('page')
    paginator = Paginator(orders_list, 20)
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)
    
    category = "UNAPPROVED WORK REQUESTS"
    return render(request, 'app/orders.html', {'orders': orders, 'category': category})

def paginate_orders(request, orders_list, per_page=20):
    page = request.GET.get('page')
    paginator = Paginator(orders_list, per_page)
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)
    return orders

def status_list(request):
    orders_list = Order.objects.filter(approval1="Accepted",approval3="Accepted",complete="Inprogress").order_by('-uploaded_at')
    orders = paginate_orders(request, orders_list)
    return render(request, 'app/status_list.html', {'orders': orders, 'type': "UPDATE EXISTING WORK REQUEST"})

def status_completed_list(request):
    orders_list = Order.objects.filter(approval3="Accepted", complete="Workdone").order_by('-uploaded_at')
    orders = paginate_orders(request, orders_list)
    return render(request, 'app/status_list.html', {'orders': orders, 'type': "UPDATE COMPLETED WORK REQUEST"})

def rejected_orders(request):
    orders_list = Order.objects.filter(
        Q(approval1="Rejected") | Q(approval2="Rejected") | Q(approval3="Rejected")
    ).order_by('-uploaded_at')
    page = request.GET.get('page')
    paginator = Paginator(orders_list, 20)
    
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)
    
    print("Paginated orders:", orders)  # Debugging line
    
    category = "REJECTED WORK REQUESTS"
    return render(request, 'app/orders.html', {'orders': orders, 'category': category})

def completed_orders(request):
	orders_list = Order.objects.filter(complete="Workdone").order_by('-uploaded_at')
	page = request.GET.get('page')
	paginator = Paginator(orders_list, 20)
	try:
		orders = paginator.page(page)
	except PageNotAnInteger:
		orders = paginator.page(1)
	except EmptyPage:
		orders = paginator.page(paginator.num_pages)
	category = "COMPLETED WORK REQUESTS"
	return render(request,'app/orders.html',{'orders':orders,'category':category})


def login_menu(request):
	loginform = LoginForm()
	registerform = RegisterForm()
	return render(request,'app/login.html',{'loginform':loginform,'registerform':registerform})

def do_login(request):
	if request.method == "POST":
		loginform = LoginForm(request.POST)
		if loginform.is_valid():
			data = loginform.cleaned_data
			username = data['username']
			password = data['password']
			user = authenticate(username=username,password=password)
			
			if user is not None:
				login(request, user)
				return HttpResponseRedirect("/")
			else:
				registerform = RegisterForm()
				message = "User doesn't exists or Password is incorrect"
				return render(request,'playground/login.html',{'loginform':loginform,'registerform':registerform,'message':message})
		else:
			registerform = RegisterForm()
			message = "Please enter coreect details"
			return render(request,'app/login.html',{'loginform':loginform,'registerform':registerform,'message':message})
	else:
		loginform = LoginForm()
		registerform = RegisterForm()
		return render(request,'app/login.html',{'loginform':loginform,'registerform':registerform})

def do_register(request):
    if request.method == "POST":
        registerform = RegisterForm(request.POST)
        if registerform.is_valid():
            data = registerform.cleaned_data
            password1 = data['password1']
            password2 = data['password2']
            user = registerform.save(commit=False)
            if password1 == password2:
                user.set_password(password1)
                user.save()
                login(request, user)
                return HttpResponseRedirect("/")
            else:
                message = "Passwords don't match"
        else:
            message = "User already exists or form is invalid"
        loginform = LoginForm()
        return render(request, 'app/login.html', {'loginform': loginform, 'registerform': registerform, 'message': message})
    else:
        loginform = LoginForm()
        registerform = RegisterForm()
        return render(request, 'app/login.html', {'loginform': loginform, 'registerform': registerform})


def approve_orders(request):
    if request.user.is_authenticated:
        user = request.user
        approver = Approver.objects.first()  # Safely get the first Approver instance

        if not approver:
            # Handle case where there are no approvers
            return render(request, 'app/approve_orders.html', {'orders': []})

        if user.username == approver.approver2:
            # Orders for approval2
            orders = Order.objects.filter(approval1='Accepted', approval2='Pending').order_by('-uploaded_at')
        
        elif user.username == approver.approver3:
            # Orders for approval3
            orders = Order.objects.filter(
                (Q(approval1='Accepted') & Q(approval3='Pending')) 
            ).order_by('-uploaded_at')

        else:
            # Orders for approval1 by the professor
            orders = Order.objects.filter(prof_mail=user.username, approval1='Pending').order_by('-uploaded_at')

        return render(request, 'app/approve_orders.html', {'orders': orders})
    
    return redirect('/login')  # Redirect to login if not authenticated

def decision_input(request, order_id):
    if request.user.is_authenticated:  # No parentheses needed
        user = request.user
        order = Order.objects.get(id=order_id)
        approver = Approver.objects.first()  # Get the first Approver instance

        prof_hash = ""
        if order.approval1 == 'Pending' and order.prof_mail == user.username:
            decisionform = DecisionForm()
            return render(request, 'app/decision.html', {'order': order, 'decisionform': decisionform, 'prof_hash': prof_hash, 'approver': approver})

        elif order.approval1 == 'Accepted' and approver.approver2 == user.username:
            decisionform = DecisionForm()
            return render(request, 'app/decision.html', {'order': order, 'decisionform': decisionform, 'prof_hash': prof_hash, 'approver': approver})

        elif order.approval1 == 'Accepted' and (order.approval2 in ['Accepted', 'May be']) and approver.approver3 == user.username:
            decisionform = DecisionForm()
            return render(request, 'app/decision.html', {'order': order, 'decisionform': decisionform, 'prof_hash': prof_hash, 'approver': approver})

        else:
            return HttpResponseRedirect("/approve_orders")
    else:
        return HttpResponseRedirect("/orders")


def detail(request,order_id):
	order = Order.objects.get(id=order_id)
	status_list = Status.objects.filter(order=order_id)
	return render(request,'app/detail.html',{'order':order,'status_list':status_list})
	

def decision(request, order_id):
    if request.user.is_authenticated:
        user = request.user
        order = get_object_or_404(Order, id=order_id)
        approver = Approver.objects.first()

        if user.username == approver.approver2 and order.approval1 == 'Accepted':
            decisionform = DecisionForm(request.POST or None)
            if request.method == 'POST' and decisionform.is_valid():
                data = decisionform.cleaned_data
                decision = data['decision']
                decision1 = data['decision1']
                remark = data['remarks']
                
                current_site = get_current_site(request)
                hash_mail = hashlib.md5(order.mail.encode()).hexdigest()

                if decision == "Reject":
                    order.approval2 = 'Rejected'
                    order.approval3 = 'Rejected'
                    order.remarks = remark
                    message = f"Hello \r\n\r\n Your Work request to CWS is rejected by Central Workshop Technical team. Please use the link below for more details and to track the Work request status. \r\n\r\n{current_site.domain}/details/{order.id}/{hash_mail}/\r\n\r\nThanking You\r\nIITH CWS\r\n"
                
                elif decision == "May be":
                    order.remarks = remark
                    order.approval2 = 'May be'
                    message = f"Hello \r\n\r\n Your Work request to CWS is marked as 'May be' by the Central Workshop Technical team. This means that they are not sure of the feasibility of the product. It is suggested that you meet the faculty in charge of the Central Workshop for further discussion. Please use the link below for more details and to track the Work request status. \r\n\r\n{current_site.domain}/details/{order.id}/{hash_mail}/\r\n\r\nThanking You\r\nIITH CWS\r\n"

                else:  # "Accept"
                    order.approval2 = 'Accepted'
                    order.remarks = remark
                    message = f"Hello \r\n\r\n Your Work request to CWS is accepted by Central Workshop Technical team. Please use the link below for more details and to track the Work request status. \r\n\r\n{current_site.domain}/details/{order.id}/{hash_mail}/\r\n\r\nThanking You\r\nIITH CWS\r\n"

                # Handle decision1 (Progress/Work Done)
                if decision1 == "Inprogress":
                    # Handle "In Progress" case
                    pass
                elif decision1 == "Workdone":
                    # Handle "Work Done" case
                    pass
                else:
                    # Handle "Not Started" or any other default case
                    pass

                mail_subject = 'IITH CWS Work request'
                to_email = order.mail
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                order.save()
                return HttpResponseRedirect("/approve_orders")
            else:
                return render(request, 'app/decision.html', {'order': order, 'decisionform': decisionform})

        elif user.username == approver.approver3 and (order.approval2 in ['Accepted', 'May be']) and order.approval1 == 'Accepted':
            decisionform = DecisionForm(request.POST or None)
            if request.method == 'POST' and decisionform.is_valid():
                data = decisionform.cleaned_data
                decision = data['decision']
                decision1 = data['decision1']
                remark = data['remarks']
                
                current_site = get_current_site(request)
                hash_mail = hashlib.md5(order.mail.encode()).hexdigest()

                if decision == "Reject":
                    order.approval3 = 'Rejected'
                    order.remarks = remark
                    message = f"Hello \r\n\r\n Your Work request to CWS is rejected by Central Workshop Faculty Incharge. Please use the link below for more details and to track the Work request status. \r\n\r\n{current_site.domain}/details/{order.id}/{hash_mail}/\r\n\r\nThanking You\r\nIITH CWS\r\n"

                else:  # "Accept"
                    order.remarks = remark
                    order.approval3 = 'Accepted'
                    message = f"Hello \r\n\r\n Your Work request to CWS is approved by Central Workshop Faculty Incharge. Please use the link below for more details and to track the Work request status. \r\n\r\n{current_site.domain}/details/{order.id}/{hash_mail}/\r\n\r\nThanking You\r\nIITH CWS\r\n"

                # Handle decision1 (Progress/Work Done)
                if decision1 == "Inprogress":
                    # Handle "In Progress" case
                    pass
                elif decision1 == "Workdone":
                    # Handle "Work Done" case
                    pass
                else:
                    # Handle "Not Started" or any other default case
                    pass

                mail_subject = 'IITH CWS Work request'
                to_email = order.mail
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                order.save()
                return HttpResponseRedirect("/approve_orders")
            else:
                return render(request, 'app/decision.html', {'order': order, 'decisionform': decisionform})

        elif user.username == order.prof_mail and order.approval1 == 'Pending':
            decisionform = DecisionForm(request.POST or None)
            if request.method == 'POST' and decisionform.is_valid():
                data = decisionform.cleaned_data
                decision = data['decision']
                decision1 = data['decision1']
                remark = data['remarks']

                if decision == "Reject":
                    order.approval1 = 'Rejected'
                    order.approval2 = 'Rejected'
                    order.approval3 = 'Rejected'
                    order.remarks = remark
                else:  # "Accept"
                    order.remarks = remark
                    order.approval1 = 'Accepted'
                
                # Handle decision1 (Progress/Work Done)
                if decision1 == "Inprogress":
                    # Handle "In Progress" case
                    pass
                elif decision1 == "Workdone":
                    # Handle "Work Done" case
                    pass
                else:
                    # Handle "Not Started" or any other default case
                    pass

                order.save()
                return HttpResponseRedirect("/approve_orders")
            else:
                return render(request, 'app/decision.html', {'order': order, 'decisionform': decisionform})

        else:
            return HttpResponseRedirect("/approve_orders")
    else:
        return HttpResponseRedirect("/orders")

def update_status(request, order_id):
    if request.user.is_authenticated:
        order = get_object_or_404(Order, id=order_id)
        
        if request.method == "POST":
            statusform = StatusForm(request.POST)
            
            if statusform.is_valid():
                data = statusform.cleaned_data
                status_input = data['status_input']
                completed_input = data['completed_input']

                # Create new Status object
                new_object = Status()
                new_object.order = order  # Link to the order instance
                new_object.status_text = status_input

                if order.complete:  # If already completed
                    new_object.save()
                    return HttpResponseRedirect("/")
                
                # Determine if the order is completed
                if completed_input == "Yes":
                    order.complete = "Workdone"
                elif completed_input == "No":
                    order.complete = "Cantbedone"
                
                # Hash the email after encoding
                hash_mail = hashlib.md5(order.mail.encode('utf-8')).hexdigest()
                
                # Prepare the message
                current_site = get_current_site(request)
                message = (
                    "Hello,\r\n\r\n"
                    f"Your Workshop request has been {'completed' if order.complete else 'updated'}. "
                    "Please use the link below to track the Work order status:\r\n\r\n"
                    f"{current_site.domain}/details/{order.id}/{hash_mail}/\r\n\r\n"
                    "Thanking You,\r\n"
                    "IITH CWS\r\n"
                )
                
                mail_subject = 'IITH CWS Work Request'
                to_email = order.mail
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                
                # Save the Status and Order objects
                new_object.save()
                order.save()

                return HttpResponseRedirect("/status_list")
            else:
                return render(request, 'app/status_form.html', {'statusform': statusform, 'order': order})
        else:
            statusform = StatusForm()
            return render(request, 'app/status_form.html', {'statusform': statusform, 'order': order})
    else:
        return HttpResponseRedirect("/login")

def prof_decision_form(request,order_id,prof_hash):
	order = Order.objects.get(id= order_id)
	hash_object = hashlib.md5(order.prof_mail)
	if hash_object.hexdigest() == prof_hash:
		if order.approval1 == 'Pending':
			decisionform = DecisionForm()
			return render(request,'app/decision.html',{'order':order,'decisionform':decisionform,'prof_hash':prof_hash})
		else:
			return HttpResponseRedirect("/detail/"+order_id)
	else:
		return HttpResponse("Something wrong")

def prof_decision(request,order_id,prof_hash):
	order = Order.objects.get(id= order_id)
	decisionform = DecisionForm(request.POST)
	if decisionform.is_valid():
		data = decisionform.cleaned_data
		decision = data['decision']
		remark = data['remarks']
		if decision == "Reject":
			order.approval1 = 'Rejected'
			order.approval2 = 'Rejected'
			order.approval3 = 'Rejected'
			order.remarks = remark
			current_site = get_current_site(request)
			hash_mail = hashlib.md5(order.mail)
			message =  "Hello \r\n\r\n Your Work request to CWS is rejected by the faculty Guide/Incharge.Please use below link for more detials and track the Work request status. \r\n\r\n" + current_site.domain  + '/details'+'/' + str(order.id) + '/' + hash_mail.hexdigest() + '/' +  "\r\n\r\nThanking You\r\nIITH CWS\r\n"
			mail_subject = 'IITH CWS Work request'
			to_email = order.mail
			email = EmailMessage(mail_subject, message, to=[to_email])
			email.send()
		else:
			order.remarks = remark
			order.approval1 = 'Accepted'
			current_site = get_current_site(request)
			hash_mail = hashlib.md5(order.mail)
			message =  "Hello \r\n\r\n Your Work request to CWS is approved by the faculty Guide/Incharge.Please use below link for more detials and track the Work request status. \r\n\r\n" + current_site.domain  + '/details'+'/' + str(order.id) + '/' + hash_mail.hexdigest() + '/' +  "\r\n\r\nThanking You\r\nIITH CWS\r\n"
			mail_subject = 'IITH CWS Workorder'
			to_email = order.mail
			email = EmailMessage(mail_subject, message, to=[to_email])
			email.send()
		order.save()

		return render(request,'app/recorded.html')
	else:
		return render(request,'app/decision.html',{'order':order,'decisionform':decisionform,'prof_hash':prof_hash})

def detail_hash(request,order_id,mail_hash):
	order = Order.objects.get(id= order_id)
	hash_object = hashlib.md5(order.mail)
	if hash_object.hexdigest() == mail_hash:
		status_list = Status.objects.filter(order=order_id)
		return render(request,'app/detail.html',{'order':order,'status_list':status_list})
	else:
		return HttpResponse("Something went wrong !!!")


# def export_orders_to_excel(request):
#     # Create an in-memory output file for the new workbook
#     output = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#     output['Content-Disposition'] = 'attachment; filename=orders.xlsx'

#     # Create a workbook and add a worksheet
#     workbook = xlsxwriter.Workbook(output)
#     worksheet = workbook.add_worksheet()

#     # Add headers
#     headers = ['Order Name', 'Email', 'Uploaded At', 'Approval Status']
#     for col_num, header in enumerate(headers):
#         worksheet.write(0, col_num, header)

#     # Get the data you want to export
#     orders = Order.objects.all()

#     # Write data to Excel
#     for row_num, order in enumerate(orders, start=1):
#         worksheet.write(row_num, 0, order.name)
#         worksheet.write(row_num, 1, order.mail)
#         worksheet.write(row_num, 2, order.uploaded_at.strftime('%d/%m/%Y'))
#         worksheet.write(row_num, 3, order.approval_status)

#     workbook.close()

#     return output

