from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from.models import Reg_tbl,Pass_tbl,Bike_tbl,Feed_tbl
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(req):
    return render(req,"index.html")

def worker_dashboard(request):
    return render(request, "workertemp/worker.html")

def reg(req):
    if req.method=="POST":
        fnm=req.POST.get('fn')
        lnm=req.POST.get('ln')
        eml=req.POST.get('em')
        gend=req.POST.get('gen') or 'user'
        unm=req.POST.get('un')
        pas=req.POST.get('ps')
        is_app=req.POST.get('isapp') in [ 'True']
        obj=Reg_tbl.objects.create(fn=fnm,ln=lnm,em=eml,gen=gend,un=unm,ps=pas,is_approved=is_app)#<--1.models name
        obj.save()
        if obj:
            msg = "Details entered successfull..."
            return render(req,"login.html",{"success":msg})
        else:
            return render(req,"register.html")
    return render(req,"register.html")

def log(req):
    if req.method == "POST":
        unm = req.POST.get('un')
        pas = req.POST.get('ps')
        gend = req.POST.get('gen')
        isapp = req.POST.get('is_approved')

        # Check credentials
        obj = Reg_tbl.objects.filter(un=unm, ps=pas,gen=gend,is_approved=True).first()

        if obj:
            # Set session data
            req.session['uid'] = obj.id
            req.session['una'] = obj.un
            req.session['is_approved'] = True 
            # Redirect based on role
            if gend == 'admin':
                return render(req, 'admintemp/admin.html')
            elif gend == 'worker':
                return redirect('worker_dashboard')  # You can also use redirect to a named URL
            elif gend == 'user':
                return render(req,'customertemp/custlocation.html')  # 'apply' should be a named URL in your urls.py
            else:
                messages.error(req, "Unknown user role.")
                return render(req, 'login.html')
        else:
            # Invalid login
            msg = "Invalid Username, Password, Role! or Not approved"
            req.session['un'] = ''
            req.session['ps'] = ''
            return render(req, "login.html", {'error': msg})
    else:
        return render(req, 'login.html')
        
def sign_out(req):
    return redirect('/')
  
def edit1(request,idno):
    obj=Reg_tbl.objects.filter(id=idno)
    return render(request,"admintemp/listofworker2.html",{"data":obj})
def edit2(request,idno):
    obj=Reg_tbl.objects.filter(id=idno)
    return render(request,"customertemp/customer.html",{"data":obj})

def loc(req):
    obb = Reg_tbl.objects.filter(gen='user')
    return render(req,"admintemp/listofcustom.html",{"data":obb})

def low(req):
    obj=Reg_tbl.objects.filter(gen='worker')
    return render(req,"admintemp/listofworker.html",{"data":obj})
    
def approve_request(request,idno):
    updated = Reg_tbl.objects.filter(id=idno).update(is_approved=True)
    if updated:
        messages.success(request, "User Rejected!")
    else:
        messages.error(request, "User not found.")
    return redirect('loc')
   

def reject_request(request, idno):
    updated = Reg_tbl.objects.filter(id=idno).update(is_approved=False)
    if updated:
        messages.success(request, "User Rejected!")
    else:
        messages.error(request, "User not found.")
    return redirect('loc')

def approve_reqwork(request,idno):
    updated = Reg_tbl.objects.filter(id=idno).update(is_approved= True)
    if updated:
            messages.success(request, "User Rejected!")
    else:
            messages.error(request, "User not found.")
    return redirect('low')

def reject_reqwork(request, idno):
    updated = Reg_tbl.objects.filter(id=idno).update(is_approved=False)
    if updated:
        messages.success(request, "User Rejected!")
    else:
        messages.error(request, "User not found.")
    return redirect('low')

def delete_user(request, idno):
   obj = Reg_tbl.objects.filter(id=idno)
   obj.delete()

def cust(req):
    if req.method=="POST":
        pik=req.POST.get('pi')#<--(input name in the form)
        drp=req.POST.get('dr')
        nam=req.POST.get('na')
        opt=req.POST.get('op')

        if not all([pik, drp, nam, opt]):
            return render(req,"customertemp/customer.html",{"error": "All fields are required!"})
        obj=Pass_tbl.objects.create(pick=pik,drop=drp,name=nam,options=opt)#<--1.models name
        obj.save()
        if obj:
            msg = "Driver on the way"
            return render(req,"customertemp/matches.html",{"success":msg})
        else:
            return render(req,"customertemp/customer.html",{"error": "Something went wrong"})
    return render(req,"customertemp/common_picks.html")



def profile(req):
    if 'uid' in req.session:
        uid = req.session['uid']
        try:
            user = Reg_tbl.objects.get(id=uid)
        except Reg_tbl.DoesNotExist:
            return render(req, 'workertemp/profile.html', {'error': 'User not found'})
        
        bikes = Bike_tbl.objects.filter(worker=user) if user.gen == "worker" else None

        return render(req, 'workertemp/profile.html', {
            'user': user,
            'bikes': bikes
        })
    
    return redirect('login')


def cprofile(req):
    # Check if the user is logged in via session
    if 'uid' in req.session:
        uid = req.session['uid']
        user = Reg_tbl.objects.get(id=uid)

        if user:
            return render(req, 'customertemp/custprofile.html', {'user': user})
        else:
            return render(req, 'customertemp/custprofile.html', {'error': 'User not found'})
    
    # If not logged in, redirect to login page
    return redirect('login') 


def go_back(request):
    return redirect(request.META.get('http://127.0.0.1:8000/', '/'))

def location(req):
    if req.method == "POST":
        pi = req.POST.get('pik')
        uid = req.session.get('uid')  # get logged in user's id

        if uid:  # make sure session exists
            # update the logged-in user's pick
            obj = Reg_tbl.objects.filter(id=uid).first()
            if obj:
                obj.pick = pi
                obj.save()
                msg = "Location updated successfully!"
                return render(req, "workertemp/worker.html", {"success": msg})
            else:
                msg = "User not found!"
                return render(req, "workertemp/location.html", {"error": msg})
        else:
            msg = "Session expired. Please login again."
            return render(req, "login.html", {"error": msg})

    return render(req, 'workertemp/location.html')

def custlocation(req):
    if req.method == "POST":
        pi = req.POST.get('pik')
        uid = req.session.get('uid')  # get logged in user's id

        if uid:  # make sure session exists
            # update the logged-in user's pick
            obj = Reg_tbl.objects.filter(id=uid).first()
            if obj:
                obj.pick = pi
                obj.save()
                msg = "Location updated successfully!"
                return redirect('match_pickup')
            else:
                msg = "User not found!"
                return render(req, "customertemp/custlocation.html", {"error": msg})
        else:
            msg = "Session expired. Please login again."
            return render(req, "login.html", {"error": msg})

    return render(req, 'customertemp/custlocation.html')

def match_pickup(request):
    uid = request.session.get('uid')  # logged in user's id
    matches = []

    if not uid:
        return render(request, "login.html", {"error": "Session expired. Please login again."})

    user_obj = Reg_tbl.objects.filter(id=uid).first()
    if not user_obj:
        return render(request, "login.html", {"error": "User not found."})

    location = user_obj.pick

    if user_obj.gen == "user":
        # Show workers at same location
        workers = Reg_tbl.objects.filter(gen="worker", pick=location)
        for w in workers:
            matches.append({
                "user": user_obj.un,
                "worker": w.un,
                "location": location
            })

    elif user_obj.gen == "worker":
        # Show users at same location
        users = Reg_tbl.objects.filter(gen="user", pick=location)
        for u in users:
            matches.append({
                "user": u.un,
                "worker": user_obj.un,
                "location": location
            })

    return render(request, "customertemp/matches.html", {"matches": matches})



def bikes(req):
    if 'uid' not in req.session:   # make sure user is logged in
        return redirect('login')

    uid = req.session['uid']
    worker = Reg_tbl.objects.get(id=uid)

    if worker.gen != "worker":   # only workers can upload bikes
        return render(req, "workertemp/bikes.html", {"error": "Only workers can upload bikes."})

    if req.method == "POST":
        bnam = req.POST.get('bikenm')
        bmod = req.POST.get('bikeml')
        bage = req.FILES.get('bikeimg')

        obj = Bike_tbl.objects.create(
            worker=worker,
            bnm=bnam,
            bml=bmod,
            bimg=bage
        )

        msg = "Details Uploaded"
        return render(req, "workertemp/bikes.html", {"success": msg})

    return render(req, "workertemp/bikes.html")

def add_feedback(req):
    if req.method == "POST":
        message = req.POST.get("message")
        rating = req.POST.get("rating")

        # Check session login
        uid = req.session.get("uid")
        if not uid:
            messages.error(req, "Please log in first.")
            return redirect("log")   # your login view name

        # Get logged in user
        reg_user = Reg_tbl.objects.get(id=uid)

        # Allow only customers
        if reg_user.gen != "user":
            messages.warning(req, "Only customers can submit feedback.")
            return redirect("cprofile")  # or wherever you want non-users to go

        # Save feedback
        Feed_tbl.objects.create(
            user=reg_user,
            message=message,
            rating=rating
        )
        messages.success(req, "Thank you for your feedback!")
        return redirect("feedbacks")

    return render(req, "customertemp/feedback.html")

@login_required(login_url='sign-in')
def feedback_list(request):
    feedbacks = Feed_tbl.objects.all().order_by('-submitted_at')
    return render(request, 'customertemp/feedback_list.html', {'feedbacks': feedbacks})

def custfeed(req):
    obj=Feed_tbl.objects.all()
    return render(req,"admintemp/custfeedback.html",{"feedbacks":obj})
 
# def work(request):
#     obj=Pass_tbl.objects.all
#     return render(request,"workertemp/assigned.html",{"data":obj})


def book_ride(request, worker_username):
    # Check login/session
    user_id = request.session.get("uid")
    if not user_id:
        return redirect("log")  # Redirect to login if not logged in

    # Get user (role: user) and worker (role: worker)
    user = get_object_or_404(Reg_tbl, id=user_id, gen="user")
    worker = get_object_or_404(Reg_tbl, un=worker_username, gen="worker")

    if request.method == "POST":
        pik = request.POST.get("pi")
        drp = request.POST.get("dr")
        opt = request.POST.get("op")

        # Validation
        if not drp or not opt:
            return render(request, "customertemp/customer.html", {
                "worker": worker,
                "msg": "Please fill all fields."
            })

        Pass_tbl.objects.create(
            customer=user,
            worker=worker,
            drop=drp,
            options=opt
        )
        return render(request, "customertemp/success.html", {
            "msg": f"Cab booked with {worker.un}!"
        })

    # GET method: show booking form
    return render(request, "customertemp/customer.html", {"worker": worker})

def booking_list(request):
    user_id = request.session.get("uid")
    if not user_id:
        return redirect("log")

    bookings = Pass_tbl.objects.filter(customer_id=user_id)
    return render(request, "customertemp/booking_list.html", {"bookings": bookings})

def worker_work_list(request):
    worker_un = request.session.get("una")  # worker's username from session
    if not worker_un:
        return render(request, "error.html", {"msg": "Worker not logged in"})

    # Find worker
    worker = get_object_or_404(Reg_tbl, un=worker_un, gen="worker")

    # Get all customers who booked this worker
    customer_ids = Pass_tbl.objects.filter(worker=worker).values_list("customer_id", flat=True).distinct()
    customers = Reg_tbl.objects.filter(id__in=customer_ids, gen="user")

    return render(request, "workertemp/work_list.html", {"customers": customers})


def worker_assigned_work(request, customer_username):
    worker_un = request.session.get("una")
    if not worker_un:
        return render(request, "error.html", {"msg": "Worker not logged in"})

    # Get worker and customer
    worker = get_object_or_404(Reg_tbl, un=worker_un, gen="worker")
    customer = get_object_or_404(Reg_tbl, un=customer_username, gen="user")

    # Get only rides from this customer assigned to this worker
    bookings = Pass_tbl.objects.filter(customer=customer, worker=worker)

    return render(request, "workertemp/user_assigned.html", {
        "customer": customer,
        "bookings": bookings
    })


# def approve_request(request,idno):
#     updated = Reg_tbl.objects.filter(id=idno).update(is_approved=True)
#     if updated:
#         messages.success(request, "User Rejected!")
#     else:
#         messages.error(request, "User not found.")
#     return redirect('loc')


# def get_nearby_drivers(passenger_id):
#     passenger = Pass_tbl.objects.get(id=passenger_id)
#     drivers = Wloc_tbl.objects.filter(pick__iexact=passenger.pick)  # case-insensitive match
#     return drivers
# def some_view(request):
#     nearby_drivers = get_nearby_drivers(passenger_id=1)
#     return render(request, 'template.html', {'nearby_drivers': nearby_drivers})


# # Example usage
# nearby_drivers = get_nearby_drivers(passenger_id=1)
