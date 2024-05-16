
from django import forms
from django.contrib.admin.widgets import AdminSplitDateTime
from django.contrib.auth.models import User

from django.utils.translation import gettext_lazy as _
from payment.models import CheckIn
from .widgets import MySplitDateTime, FilteredSelectMultiple
from pagedown.widgets import PagedownWidget
from .models import *


class SingUp(forms.Form):
    """
    This is the signup form.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
        'id_not_found': _("This ID is not available."),
        'info_not_matched': _("The information didn't match."),
        'username_exists': _("The username already exists."),
        'staff_username_exists': _("This staff already has an account please login to it."),
    }

    staff_id = forms.IntegerField(
        label=_('ID'),
        help_text=_("Enter your staff ID"),
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Enter your ID'),
            }
        )
    )
    first_name = forms.CharField(
        label=_("First Name"),
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Enter your first name'),
            }
        )
    )
    middle_name = forms.CharField(
        label=_('Middle Name'),
        required=False,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Enter your middle name'),
            }
        )
    )
    last_name = forms.CharField(
        label=_("Last Name"),
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Enter your last name'),
            }
        )
    )
    contact_number = forms.CharField(
        label=_('Contact Number'),
        max_length=15,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Enter your contact number'),
            }
        )
    )
    email = forms.EmailField(
        label=_("Email"),
        max_length=50,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Enter your email'),
            }
        )
    )
    username = forms.CharField(
        label=_("Username"),
        max_length=32,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Username'),
            }
        )
    )
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Password')
            }
        )
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Confirm Password')
            }
        ),
        help_text=_("Enter the same password as above, for verification."))

    def clean(self):
        staff_id = self.cleaned_data.get('staff_id')
        first_name = self.cleaned_data.get('first_name')
        middle_name = self.cleaned_data.get('middle_name')
        last_name = self.cleaned_data.get('last_name')
        contact_number = self.cleaned_data.get('contact_number')
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        s = Staff.objects.filter(staff_id__exact=staff_id)
        u = User.objects.filter(username__iexact=username)
        if s.count():
            st = Staff.objects.get(staff_id__exact=staff_id)
            if st.user:
                raise forms.ValidationError(
                    self.error_messages['staff_username_exists'],
                    code='staff_username_exits',
                )
            elif first_name != st.first_name or email != st.email_address:
                raise forms.ValidationError(
                    self.error_messages['info_not_matched'],
                    code='info_not_matched',
                )
        else:
            raise forms.ValidationError(
                self.error_messages['id_not_found'],
                code='id_not_found',
            )

        if u.count():
            raise forms.ValidationError(
                self.error_messages['username_exists'],
                code='username_exists',
            )

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )

    def save(self):
        user = User.objects.create(
            username=self.cleaned_data['username'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
        )
        return user



class RoomUpdateForm(forms.ModelForm):
    facility = forms.ModelMultipleChoiceField(queryset=Facility.objects.all(), required=False)

    class Meta:
        model = Room
        fields = [
            'room_no',
            'room_type',
            'reservation',
            'facility',
        ]
        labels = {
            'room_no': 'Room Number :',
            'room_type': 'Room Type :',
            'reservation': 'Reservation :',
        }

        def __init__(self, *args, **kwargs):
            if kwargs.get('instance'):
                initial = kwargs.setdefault('initial', {})
                if kwargs['instance'].groups.all():
                    initial['facility'] = kwargs['instance'].groups.all()[0]
                else:
                    initial['facility'] = None
            forms.ModelForm.__init__(self, *args, **kwargs)

        def save(self):
            facility = self.cleaned_data.pop('facility')
            u = super().save()
            u.groups.set([facility])
            u.save()
            return u


class ReservationForm(forms.Form):
    error_message = {
        'date_time_error': 'Departure time earlier than Arrival time',
    }
    first_name = forms.CharField(
        label=_("First Name"),
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _("Enter first name "),
            }
        )
    )
    middle_name = forms.CharField(
        label=_("Middle Name "),
        required=False,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _("Enter Middle name "),
            }
        )
    )
    last_name = forms.CharField(
        label=_("Last Name"),
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': ' form-control',
                'placeholder': _("Enter Last name "),
            }
        )
    )
    contact_number = forms.CharField(
        label=_("Contact Number"),
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'class': ' form-control',
                'placeholder': _("Enter Contact Number"),
            }
        )
    )
    email_address = forms.EmailField(
        label=_("Email"),
        max_length=50,
        required=False,
        widget=forms.EmailInput(
            attrs={
                'class': ' form-control',
                'placeholder': _("Enter Email "),
            }
        )
    )
    address = forms.CharField(
        label=_("Address"),
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': ' form-control',
                'placeholder': _("Enter address "),
            }
        )
    )
    no_of_adults = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': ' form-control',
                'placeholder': _("Enter Number of Adults "),

            }
        )
    )

    no_of_childrens = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': ' form-control',
                'placeholder': _("Enter Number of Children "),
            }
        )
    )

    rooms = forms.ModelMultipleChoiceField(
        queryset=Room.objects.filter(reservation__isnull=True),
        widget=FilteredSelectMultiple(
            is_stacked=True,
            verbose_name="Room",
            attrs={
                'class': 'form-control',
            },
        ),
    )

    # expected_arrival_date_time = forms.SplitDateTimeField(
    #     label='',
    #     widget=AdminSplitDateTime(attrs={'placeholder': _('From date')}),
    #     localize=True,
    #     required=False
    #
    # )
    #
    # expected_departure_date_time = forms.SplitDateTimeField(
    #     label='',
    #     widget=AdminSplitDateTime(attrs={'placeholder': _('To date')}),
    #     localize=True,
    #     required=False
    #
    # )


    expected_arrival_date_time = forms.SplitDateTimeField(
        widget=MySplitDateTime(
        )
    )

    expected_departure_date_time = forms.SplitDateTimeField(
        widget=MySplitDateTime(
        )
    )


class CheckInRequestForm(forms.ModelForm):
    class Meta:
        model = CheckIn
        fields = ['reservation']
        widgets = {'reservation': forms.HiddenInput()}


class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = '__all__'

class RoomTypeNameForm(forms.ModelForm):
    class Meta:
        model = RoomTypeName
        fields = '__all__'

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = '__all__'


class RoomTypeForm(forms.ModelForm):
    description = forms.CharField(widget=PagedownWidget)
    class Meta:
        model = RoomType
        fields =['name', 'category', 'price', 'size','capacity','pets','breakfast','features','description','extras']
