import httplib2
from apiclient import discovery
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.password_validation import validate_password
from django import forms
from . import mailrepo
from .settings import ALLOWED_HOSTS,COMPANY_NAME,DEFAULT_USER_PASSWORD



class TimeUserManager(BaseUserManager):
    use_in_migrations = True
    def create_user(self, email, password=None):
        """
            Creates and saves a User with the given email, date of
            birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
                email=self.normalize_email(email),
                )
        user.set_password(password)
        user.save(using=self._db)
        return user  

    def create_superuser(self, email,  password):
        """
            Creates and saves a superuser with the given email, date of
            birth and password.
        """
        user = self.create_user(email,
                password=password,
                )
        user.is_staff = True
        user.save(using=self._db)
        return user          

class TimeUser(AbstractBaseUser):
    email = models.EmailField(
            verbose_name='email address',
            max_length=255,
            unique=True,
            )
    is_active = models.BooleanField(
            _('active'),
            default=True,
            help_text=_(
                'Designates whether this user should be treated as active. '
                'Unselect this instead of deleting accounts.'
                ),
            )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_staff = models.BooleanField(
            _('staff status'),
            default=False,
            help_text=_('Designates whether the user can log into this admin site.'),
            )
    date_of_birth = models.DateField(_('date of birth'), null=True)
    cost_per_hr = models.DecimalField(_('cost per hour'),default=0.0,max_digits=8,decimal_places=2)
    objects = TimeUserManager()

    USERNAME_FIELD = 'email'
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        abstract = False
        db_table = 'timeuser'
        app_label = 'timecapture'

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    
    def __str__(self):              
        if self.first_name and self.last_name:
            return '%s %s' % (self.first_name,self.last_name)
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

class TimeUserForm(forms.ModelForm):
    error_css_class = 'error'
    password1 = forms.CharField(required=True)
    password2 = forms.CharField(required=True)
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        validate_password(password1)
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(TimeUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    class Meta:
        model = TimeUser
        fields = ['first_name','last_name',]

@receiver(post_save,sender=TimeUser)
def send_email_to_new_user(sender, **kwargs):
    if kwargs['created']:
        user = kwargs['instance']
        subject = 'Welcome to ' + COMPANY_NAME
        content = 'Here are your login credentials\nusername: '+user.email+'\npassword: '+DEFAULT_USER_PASSWORD+'\n\n'
        if ALLOWED_HOSTS:
            content += 'The server address is: http://%s\n' % ALLOWED_HOSTS[0]

        credentials = mailrepo.get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('gmail', 'v1', http=http)
        message = mailrepo.CreateMessage('timesheet.tenet.bot@gmail.com',user.email,subject,content)
        mailrepo.SendMessage(service,'me',message)
