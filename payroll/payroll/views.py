from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.decorators import login_required
from employee_management.forms import FirmProfileForm,EditFirmProfileForm
from employee_management.models import FirmProfile

def base(request):
    return render(request,"base.html")

@login_required(login_url="/authentication/login")
def create_firm_profile(request):
    if request.method=="POST":
        form = FirmProfileForm(request.POST,request.FILES)

        if form.is_valid():
            form.save()
            return redirect('profile_firm_edit')
        else:
            return HttpResponse(form.errors)

    else:

        form = FirmProfileForm(initial={"firm_name":request.user.firm_name})
    return render(request,"firm_profile.html",{"form":form})

@login_required(login_url="/authentication/login")
def view_firm_profile(request):
    firm_profile = FirmProfile.objects.get(firm_name=request.user.firm_name)

    return render(request,"view_firm_profile.html",{"profile":firm_profile})

@login_required(login_url="/authentication/login")
def edit_firm_profile(request):
    firm_profile = FirmProfile.objects.get(firm_name=request.user.firm_name)

    if request.method=="POST":
        form = EditFirmProfileForm(request.POST or None,request.FILES,instance=firm_profile)

        if form.is_valid():
            form.save()
            return redirect('profile_firm_edit')
        else:
            return HttpResponse(form.errors)

    else:

        form = EditFirmProfileForm(instance=firm_profile)
    return render(request,"edit_firm_profile.html",{"form":form})

@login_required(login_url="/authentication/login")
def firm_profile(request):
    is_absent = list(FirmProfile.objects.filter(firm_name=request.user.firm_name))==[]
    if is_absent==False:
        return redirect('profile_firm_view')

    return render(request,"firm_initial.html")
