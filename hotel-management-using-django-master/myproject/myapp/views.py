from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group, User
from django.db import transaction, IntegrityError
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views import generic
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView

from .forms import *
from .models import Room, Reservation, Staff, Customer, Facility, RoomTypeName, RoomCatagory
from django.core.exceptions import ValidationError

from django.views.decorators.csrf import csrf_protect


@csrf_protect
@transaction.atomic
def signup(request):
    title = "Signup"
    if request.user.is_authenticated:
        request.session.flush()
    if request.method == 'POST':
        form = SingUp(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # staffs_group = get_object_or_404(Group, name__iexact="Staff")
                    form.save()
                    print("form", form)
                    staff_id = form.cleaned_data['staff_id']
                    print("staff id", staff_id)
                    username = form.cleaned_data['username']
                    print("username", username)
                    s = get_object_or_404(Staff, staff_id__exact=staff_id)
                    s.user = get_object_or_404(User, username__iexact=username)
                    s.user.set_password(form.cleaned_data['password1'])
                    # s.user.groups.add(staffs_group)
                    print(s)
                    s.user.save()
                    s.save()
            except IntegrityError:
                raise Http404
            return redirect('/')
    else:
        form = SingUp()

    return render(
        request, 'Backend/signup.html', {'form': form, 'title': title}, )


@login_required
def main_backend_page(request):
    page_title = "Hotel Management system"
    page = "Hotel Management"
    totle_number_rooms = Room.objects.all().count()
    total_number_reservations = Reservation.objects.all().count()
    available_number_rooms = Room.objects.exclude(reservation__isnull=False).count()
    total_number_staffs = Staff.objects.all().count()
    total_number_customer = Customer.objects.all().count()
    if total_number_reservations == 0:
        last_reservation = Reservation.objects.none()
    else:
        last_reservation = Reservation.objects.get_queryset().latest('reservation_date_time')
    context = {
        'totle_number_rooms': totle_number_rooms,
        'page_title': page_title,
        'page': page,
        'total_number_reservations': total_number_reservations,
        'available_number_rooms': available_number_rooms,
        'total_number_staffs': total_number_staffs,
        'total_number_customer': total_number_customer,
        'last_reservation': last_reservation,
    }
    return render(request, 'Backend/home.html', context)


@permission_required('main.add_reservation', 'login', raise_exception=True)
@transaction.atomic
def Reserve(request):
    title = "Reservation  Form"
    reservation = Reservation.objects.none()
    if request.method == 'POST':
        reservation_form = ReservationForm(request.POST)
        if reservation_form.is_valid():
            try:
                with transaction.atomic():
                    customer = Customer(
                        first_name=reservation_form.cleaned_data.get('first_name'),
                        middle_name=reservation_form.cleaned_data.get('middle_name'),
                        last_name=reservation_form.cleaned_data.get('last_name'),
                        email_address=reservation_form.cleaned_data.get('email_address'),
                        contact_number=reservation_form.cleaned_data.get('contact_number'),
                        address=reservation_form.cleaned_data.get('address'),
                    )
                    print('customer = ', customer)
                    customer.save()
                    staff = request.user
                    print(staff)
                    # staff.save()
                    reservation = Reservation(
                        # staff = request.user,
                        staff=get_object_or_404(Staff, user=staff),
                        customer=customer,
                        no_of_childrens=reservation_form.cleaned_data.get('no_of_childrens'),
                        no_of_adults=reservation_form.cleaned_data.get('no_of_adults'),
                        expected_arrival_date_time=reservation_form.cleaned_data.get('expected_arrival_date_time'),
                        expected_departure_date_time=reservation_form.cleaned_data.get('expected_departure_date_time'),
                        reservation_date_time=timezone.now(),
                    )
                    print(reservation)

                    reservation.save()
                    for room in reservation_form.cleaned_data.get('rooms'):
                        room.reservation = reservation
                        room.save()
            except IntegrityError:
                raise Http404
            return HttpResponseRedirect(reverse('myapp:ReservationListView'))
            # return render(request,'Backend/reservation/reserve_success_msg.html', {'reservation': reservation,'title': title,})
    else:
        reservation_form = ReservationForm()

    return render(
        request, 'Backend/reservation/reserve_form.html', {'title': title, 'reservation_form': reservation_form})


def reserve_success(request):
    pass


############## Room Information Management #####################################
class RoomListView(PermissionRequiredMixin, generic.ListView):
    model = Room
    # paginate_by = 5
    title = _("Room List")
    permission_required = "myapp.can_view_room"
    extra_context = {'title': title}
    template_name = 'Backend/room/room_list.html'

    def get_queryset(self):

        filter_value = self.request.GET.get('filter', 'all')
        if filter_value == 'all':
            filter_value = 0
        elif filter_value == 'avail':
            filter_value = 1
        try:
            new_context = Room.objects.filter(availability__in=[filter_value, 1])
        except ValidationError:
            raise Http404(_('Wrong filter argument given '))
        return new_context

    def get_context_data(self, **kwargs):
        context = super(RoomListView, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', 'all')
        # print(context)
        return context


def room_serach(request):
    list = Room.objects.all()
    if request.user.is_staff or request.user.is_superuser:
        list = Room.objects.all()

    query = request.GET.get("q")
    if query:
        list = list.filter(
            Q(room_no__icontains=query)
        ).distinct()

    context = {
        "list": list,

    }
    return render(request, "Backend/room/room_search.html", context)


class RoomDetailView(PermissionRequiredMixin, generic.DetailView):
    model = Room
    context_object_name = 'room'
    title = _("Room Detail Information")
    permission_required = 'myapp.can_view_room'
    extra_context = {'title': title}
    template_name = 'Backend/room/room_details.html'

class RoomEdit(PermissionRequiredMixin, generic.UpdateView):
    model = Room
    permission_required = "myapp.can_view_room"
    fields = ['room_no', 'room_type', 'reservation', 'facility']
    template_name = 'Backend/room/room_edit.html'
    def get_success_url(self):
        return reverse('myapp:RoomListView')

def RoomAdd(request):
    if request.method == 'POST':
        form_room = RoomUpdateForm(request.POST, request.FILES)
        if form_room.is_valid():
            try:
                form_room_info = form_room.save()
                note = "Room Add Successfully"
                new_form_room = RoomUpdateForm()
            except IntegrityError:
                raise Http404
        return HttpResponseRedirect(reverse('myapp:RoomListView'))
    else:
        form_room = RoomUpdateForm()
    return render(request,'Backend/room/room_add.html', {'form':form_room})


############## end Room Information Management #####################################

class ReservationListView(PermissionRequiredMixin, generic.ListView, generic.FormView):
    model = Reservation
    queryset = Reservation.objects.all().order_by('-reservation_date_time')
    title = _("Reservation List")
    # paginate_by = 5
    allow_empty = True
    form_class = CheckInRequestForm
    # success_url = reverse_lazy("check_in-list")
    permission_required = 'myapp:can_view_reservation'
    extra_context = {'title': title}
    template_name = 'Backend/reservation/reservation_list.html'

    @transaction.atomic
    def form_valid(self, form):
        try:
            with transaction.atomic():
                checkin = form.save(commit=False)
                checkin.user = self.request.user
                checkin.save()
        except IntegrityError:
            raise Http404
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('myapp:ReservationListView')


class ReservationDetailView(PermissionRequiredMixin, generic.DetailView):
    model = Reservation
    title = _("Reservation Information")
    permission_required = 'myapp.can_view_reservation'
    template_name = 'Backend/reservation/reservation_detail.html'
    raise_exception = True
    extra_context = {
        'title': title,
    }


########################################################

# Customer Details

class CustomerDetailView(PermissionRequiredMixin, generic.DetailView):
    model = Customer
    title = _("Customer Information")
    permission_required = 'main.can_view_customer'
    template_name = 'Backend/reservation/customer_detail.html'
    raise_exception = True
    extra_context = {
        'title': title,
    }


class StaffDetailView(PermissionRequiredMixin, generic.DetailView):
    model = Staff
    title = _("Staff Information ")
    template_name = 'Backend/reservation/staff_detail.html'
    permission_required = 'main.can_view_staff_detail'
    extra_context = {'title': title}

########## Facility ############
def AddFacility(request):
    if request.method == 'POST':
        form_facility = FacilityForm(request.POST, request.FILES)
        if form_facility.is_valid():
            form_facility_info = form_facility.save()
            note = "Facility Add Successfully"
            new_form_facility = FacilityForm()
        else:
            note = "Failed. Try again!!!!!!"
        return HttpResponseRedirect(reverse('myapp:FacilityList'))
    else:
        form_facility = FacilityForm()
    return render(request,'Backend/room/add_facility.html', {'facilityForm':form_facility})


class FacilityList(PermissionRequiredMixin, generic.ListView):
    title = 'Facility List'
    model = Facility
    template_name = 'Backend/room/facility_list.html'
    paginate_by = 5
    allow_empty = True
    permission_required = 'myapp:can_view_customer'
    extra_context = {
        'title': title,
    }

def FacilityEdit(request, pk):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    # if not request.user.is_authenticated():
    #     raise Http404
    instance = get_object_or_404(Facility, id=pk)

    form = FacilityForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect('myapp:FacilityList')

    context = {
        "instance": instance,
        "form": form,
    }
    return render(request, 'Backend/room/facility_edit.html', context)

#########################

################ Room Type ##################
class RoomTypeNameList(PermissionRequiredMixin, generic.ListView):
    title = 'Room Type Name List'
    model = RoomTypeName
    queryset = RoomTypeName.objects.all().order_by("-id")
    template_name = 'Backend/room/room_type_name_list.html'
    # paginate_by = 5
    allow_empty = True
    permission_required = 'myapp:can_view_customer'
    extra_context = {
        'title': title,
    }

def AddRoomTypeName(request):
    if request.method == 'POST':
        form_room_type_name = RoomTypeNameForm(request.POST, request.FILES)
        if form_room_type_name.is_valid():
            form_room_type_name_info = form_room_type_name.save()
            note = "Facility Add Successfully"
            new_form_room_type_name = RoomTypeNameForm()
        else:
            note = "Failed. Try again!!!!!!"
        return HttpResponseRedirect(reverse('myapp:RoomTypeNameList'))
        # return render(request,'Backend/room/add_room_type_name.html',{'AddRoomTypeNameForm':new_form_room_type_name, 'note':note})
    else:
        form_room_type_name = RoomTypeNameForm()
    return render(request,'Backend/room/add_room_type_name.html', {'AddRoomTypeNameForm':form_room_type_name})


def RoomTypeNameEdit(request, pk):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    # if not request.user.is_authenticated():
    #     raise Http404
    instance = get_object_or_404(RoomTypeName, id=pk)

    form = RoomTypeNameForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect('myapp:RoomTypeNameList')

    context = {
        "instance": instance,
        "form": form,
    }
    return render(request, 'Backend/room/edit_room_type_name.html', context)
#######################

class StaffList(PermissionRequiredMixin, generic.ListView):
    title = 'Room Type List'
    model = Staff
    queryset = Staff.objects.all().order_by("-staff_id")
    template_name = 'Backend/staff_list.html'
    paginate_by = 5
    allow_empty = True
    permission_required = 'myapp:can_view_customer'
    extra_context = {
        'title': title,
    }

def AddStaff(request):
    if request.method == 'POST':
        form_staff = StaffForm(request.POST, request.FILES)
        if form_staff.is_valid():
            form_staff_info = form_staff.save()
            note = "Facility Add Successfully"
            new_form_staff = StaffForm()
        else:
            note = "Failed. Try again!!!!!!"
        return HttpResponseRedirect(reverse('myapp:StaffList'))
    else:
        form_staff = StaffForm()
    return render(request,'Backend/staff_form.html', {'staff_form':form_staff})

def StaffEdit(request, pk):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    # if not request.user.is_authenticated():
    #     raise Http404
    instance = get_object_or_404(Staff, staff_id=pk)

    form = StaffForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect('myapp:StaffList')

    context = {
        "instance": instance,
        "form": form,
    }
    return render(request, 'Backend/staff_edit.html', context)


################## Room Type ###########

class RoomTypeList(PermissionRequiredMixin, generic.ListView):
    title = 'Room Type List'
    model = RoomType
    queryset = RoomType.objects.all().order_by("-room_type_id")
    template_name = 'Backend/room/room_type_list.html'
    paginate_by = 5
    allow_empty = True
    permission_required = 'myapp:can_view_customer'
    extra_context = {
        'title': title,
    }
class RoomTypeDetail(PermissionRequiredMixin, generic.DetailView):
    model = RoomType
    title = _("Room Type Information")
    permission_required = 'myapp.can_view_reservation'
    template_name = 'Backend/room/room_type_detail.html'
    raise_exception = True
    extra_context = {
        'title': title,
    }
def AddRoomType(request):
    if request.method == 'POST':
        form_room_type = RoomTypeForm(request.POST, request.FILES)
        if form_room_type.is_valid():
            form_room_type_info = form_room_type.save(commit=False)
            print(form_room_type_info)
            form_room_type_info.save()
            note = "Room Type Add Successfully"
            form_room_type_staff = RoomTypeForm()
        else:
            note = "Failed. Try again!!!!!!"
        return HttpResponseRedirect(reverse('myapp:RoomTypeList'))
    else:
        form_room_type = RoomTypeForm()
    return render(request,'Backend/room/room_type_form.html', {'room_type_form':form_room_type})


@login_required
def EditRoomType(request, pk):
    room_type = RoomType.objects.get(room_type_id=pk)
    if request.POST:
        form = RoomTypeForm(request.POST, instance=room_type)
        if form.is_valid():
            if form.save():
                return redirect(reverse('myapp:RoomTypeList'), messages.success(request, 'Room Type was successfully updated.', 'alert-success'))
            else:
                return redirect(reverse('myapp:RoomTypeList'), messages.error(request, 'Data is not saved', 'alert-danger'))
        else:
            return redirect(reverse('myapp:RoomTypeList'), messages.error(request, 'Form is not valid', 'alert-danger'))
    else:
        form = RoomTypeForm(instance=room_type)
        return render(request, 'Backend/room/room_type_edit.html', {'form':form})

# class EditRoomType(PermissionRequiredMixin, generic.UpdateView):
#     model = RoomTypeForm
#     permission_required = "myapp.can_view_room"
#     fields = ['name', 'category', 'price', 'size','capacity','pets','breakfast','features','description','extras']
#     template_name = 'Backend/room/room_type_edit.html'
#     def get_success_url(self):
#         return reverse('myapp:RoomTypeList',)

