from django.test import TestCase
from django.core import mail

class FeedTest(TestCase):
    fixtures = ['test_data',]
    
    def test_email(self):
        from models import FlatEmail
        self.assertTrue(FlatEmail.objects.send_mail('test', ['testperson@example.com']))
        self.assertEquals(len(mail.outbox), 1)
        email = mail.outbox.pop()
        self.assertEquals(email.subject, 'Test Email')
        self.assertEquals(len(email.attachments), 1)
        self.assertEquals(email.attachments[0][2], 'text/html')