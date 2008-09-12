from django.db import models
from django.core import mail
from django.template import loader, Context, Template
from django.contrib.sites.models import Site
from django.utils.safestring import mark_safe

DEFAULT_TEMPLATE = 'flatemails/default.txt'

# Create your models here.
class FlatEmailManager(models.Manager):
    def get_email(self, key):
        site = Site.objects.get_current()
        return super(FlatEmailManager, self).get_query_set().get(key=key, sites=site)
    
    def send_mail(self, key, *args, **kwargs):
        try:
            email = self.get_email(key)
        except self.model.DoesNotExist:
            return False
        else:
            email.send_mail(*args, **kwargs)
            return True

class FlatEmail(models.Model):
    key = models.CharField(max_length=128)
    title = models.CharField(max_length=255)
    from_email = models.EmailField(max_length=255)
    to_email = models.EmailField(max_length=255, blank=True)
    content = models.TextField()
    sites = models.ManyToManyField(Site)
    template_name = models.CharField(max_length=70, blank=True,
        help_text="Example: 'flatemails/contact.txt'. If this isn't provided, the system will use 'flatemails/default.txt'.")
    
    objects = FlatEmailManager()
    
    def render_content(self, recipient_list, context_dict, from_email=None):
        t = loader.get_template(self.template_name or DEFAULT_TEMPLATE)
        context_dict = dict(context_dict)
        context_dict['flat_email'] = self
        context_dict['from_email'] = from_email
        context_dict['recipient_list'] = recipient_list
        context_dict['site'] = Site.objects.get_current()
        c = Context(context_dict)
        context_dict['content'] = mark_safe(Template(self.content).render(c))
        return t.render(Context(context_dict))
    
    def get_routing_emails(self, recipient_list, from_email):
        if not from_email:
            from_email = self.from_email
        if self.to_email:
            if not hasattr(recipient_list, 'append'):
                recipient_list = list(recipient_list)
            recipient_list.append(self.to_email)
        return recipient_list, from_email

    def send_mail(self, recipient_list, context_dict, from_email=None, fail_silently=False, auth_user=None, auth_password=None):
        recipient_list, from_email = self.get_routing_emails(recipient_list, from_email)
        content = self.render_content(recipient_list, context_dict, from_email)
        mail.send_mail(self.title, content, from_email, recipient_list, fail_silently, auth_user, auth_password)
        
    def send_mass_mail(self, data, context_dict, from_email=None, fail_silently=False, auth_user=None, auth_password=None):
        datalist = list()
        for from_email, recipient_list in data:
            recipient_list, from_email = self.get_routing_emails(recipient_list, from_email)
            content = self.render_content(recipient_list, context_dict, from_email)
            datalist.append((self.title, content, from_email, recipient_list))
        mail.send_mass_mail(datalist, fail_silentlty, auth_user, auth_password)
        
    def __unicode__(self):
        return self.key
