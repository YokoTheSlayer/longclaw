import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from os import environ

from django.core.mail import send_mail
from django.db import models
from longclaw.settings import PRODUCT_VARIANT_MODEL
from longclaw.shipping.models import Address


class Order(models.Model):
    SUBMITTED = 1
    FULFILLED = 2
    PAID_UP = 3
    IN_PROCESS = 4
    SHIPPED = 5
    ORDER_STATUSES = ((SUBMITTED, 'Cформирован'),
                      (FULFILLED, 'Подтвержден'),
                      (PAID_UP, 'Оплачен'),
                      (IN_PROCESS, 'В процессе оплаты'),
                      (SHIPPED, 'Отгружен'))
    payment_date = models.DateTimeField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=ORDER_STATUSES, default=SUBMITTED)
    status_note = models.CharField(max_length=128, blank=True, null=True)

    transaction_id = models.CharField(max_length=256, blank=True, null=True)
    mpay_id = models.CharField(max_length=150, blank=True, null=True)

    # contact info
    email = models.EmailField(max_length=128, blank=True, null=True)
    # shipping info
    shipping_address = models.ForeignKey(
        Address, blank=True, null=True, related_name="orders_shipping_address", on_delete=models.PROTECT)

    def __str__(self):
        return "Order #{} - {}".format(self.id, self.email)

    @property
    def total(self):
        """Total cost of the order
        """
        total = 0
        for item in self.items.all():
            total += item.total
        return total

    @property
    def total_items(self):
        """The number of individual items on the order
        """
        return self.items.count()


    def send_email_sc(self):
        """
        Send email to user with info about status change
        """
        msg = MIMEText('Status of your order now: "{}"'.format(self.ORDER_STATUSES[self.status][1]))
        msg['Subject'] = ("Your status was changed")
        msg['From'] = environ['SMTP_HOST_LOGIN']
        msg['To'] = self.email
        s = smtplib.SMTP_SSL(environ['SMTP_HOST'], environ['SMTP_PORT'])
        s.login(environ['SMTP_HOST_LOGIN'], environ['SMTP_HOST_PASSWORD'])
        s.sendmail(msg['From'], msg['To'], msg.as_string())
        s.quit()

    def fulfill(self):
        """Mark this order as being fulfilled
        """
        self.send_email_sc()
        self.status = self.FULFILLED
        self.save()

    def paid_up(self):
        """Mark this order as being paid_up
        """
        self.send_email_sc()
        self.status = self.PAID_UP
        self.save()

    def shipped(self):
        """Mark this order as being shipped
        """
        self.send_email_sc()
        self.status = self.SHIPPED
        self.save()

    def in_process(self):
        """Mark this order as being in process
        """
        self.send_email_sc()
        self.status = self.IN_PROCESS
        self.save()

class OrderItem(models.Model):
    product = models.ForeignKey(PRODUCT_VARIANT_MODEL, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(default=1)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)

    @property
    def total(self):
        return self.quantity * self.product.price

    def __str__(self):
        return "{} x {}".format(self.quantity, self.product.get_product_title())
