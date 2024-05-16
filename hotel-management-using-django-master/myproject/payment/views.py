from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction, IntegrityError
from django.http import Http404
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import DetailView
from myapp.models import Reservation
from django.views import generic

from myapp.models import Facility, Staff
from .forms import CheckoutRequest
from .models import CheckIn, Checkout
from django.urls import reverse


@permission_required("myapp:can_view_staff", login_url='login')
def payment_index(request):
    title = "Payment Dashboard"
    total_reservations = Reservation.objects.all().count()
    total_check_in = CheckIn.objects.all().count()
    # total_check_out = Checkout.objects.all.count()
    last_checked_in = CheckIn.objects.none()
    if total_check_in > 0:
        last_checked_in = CheckIn.objects.get_queryset().latest('check_in_date_time')

    context = {
        'title': title,
        'total_reservations': total_reservations,
        'total_check_in': total_check_in,
        'last_checked_in': last_checked_in,

    }
    return render(request, 'Backend/payment/payment_index.html', context)


class CheckinListView(PermissionRequiredMixin, generic.ListView, generic.FormView):
    model = CheckIn
    # paginate_by = 5
    queryset = CheckIn.objects.all().order_by('-check_in_date_time')
    allow_wmpty = True
    permission_required = 'myapp:can_view_customer'
    title = 'Ckeck In List'
    form_class = CheckoutRequest
    template_name = 'Backend/payment/checkin_list.html'
    extra_context = {
        'title': title,
    }

    def form_valid(self, form):
        try:
            with transaction.atomic():
                checkout = form.save()
                checkout.user = self.request.user
                print(checkout.user)
                checkout.save()
                print(checkout)
                for room in checkout.check_in.reservation.room_set.all():
                    room.reservation = None
                    room.save()
        except IntegrityError:
            raise Http404

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('payment:CheckinListView')


class CheckInDetailView(PermissionRequiredMixin, generic.DetailView):
    model = CheckIn
    template_name = 'Backend/payment/checkin_details.html'
    permission_required = 'myapp:can_view_customer'
    total_facilities = Facility.objects.count()
    title = "CheckIn Detail"

    if not total_facilities:
        facilities = Facility.objects.none()
    else:
        facilities = Facility.objects.all()

    extra_context = {
        'total_facilities': total_facilities,
        'title': title,
        'facilities': facilities,
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        checkin = context['checkin']
        rooms = checkin.rooms
        staff = Staff.objects.filter(user=checkin.user)
        if not staff.count():
            staff = Staff.objects.none()
        else:
            staff = Staff.objects.get(user=checkin.user)

        context['staff'] = staff
        if rooms:
            new_rooms = checkin.rooms.split(", ")
            new_rooms = list(map(int, new_rooms))
            context['rooms'] = new_rooms
        return context


class checkoutList(PermissionRequiredMixin, generic.ListView):
    title = 'Check Out List'
    model = Checkout
    template_name = 'Backend/payment/checkout_list.html'
    # paginate_by = 5
    allow_empty = True
    permission_required = 'myapp:can_view_customer'
    extra_context = {
        'title': title,
    }


class CheckoutDetails(PermissionRequiredMixin, generic.DetailView):
    model = Checkout
    template_name = 'Backend/payment/checkout_detail.html'
    permission_required = 'myapp:can_view_customer'
    title = 'Check Out Detail'
    extra_context = {
        'title':title,
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        checkout = context['checkout']
        staff = Staff.objects.filter(user=checkout.user)
        if not staff.count():
            staff = Staff.objects.none()
        else:
            staff = Staff.objects.get(user=checkout.user)

        context['staff'] = staff
        return context


def checkin_show(request, check_id):
    checkin = CheckIn.objects.filter(id=check_id)
    return render(request, 'Backend/payment/checkin_show.html', {'checkin': checkin})


def checkout_show(request, check_id):
    checkout = Checkout.objects.filter(id=check_id)
    return render(request, 'Backend/payment/checkout_show.html', {'checkout': checkout})

