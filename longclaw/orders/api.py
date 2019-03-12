from rest_framework.decorators import detail_route
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from longclaw.orders.models import Order, OrderItem
from longclaw.orders.serializers import OrderSerializer
from os import environ
import requests
import datetime
import hashlib
import smtplib
from email.mime.text import MIMEText


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Order.objects.all()


    def send_mail_link(self, new_response, data):
        #new_response['PAY_LINK'] = 'HTTPS://TEST.RU'  #УДАЛИТЬ ПРИ ПРОДАКШНЕ
        msg = MIMEText('Ссылка для оплаты вашего заказа: "{}"'.format(new_response['PAY_LINK']))
        msg['Subject'] = ("Ссылка для оплаты заказа")
        msg['From'] = environ['SMTP_HOST_LOGIN']
        msg['To'] = data.email
        s = smtplib.SMTP_SSL(environ['SMTP_HOST'], environ['SMTP_PORT'])
        s.login(environ['SMTP_HOST_LOGIN'], environ['SMTP_HOST_PASSWORD'])
        s.sendmail(msg['From'], msg['To'], msg.as_string())
        s.quit()

    def analyze_response(self, data, order):
        #data['RESULT'] = '0'
        #data['PAY_ID'] = '1111'
        if data['RESULT'] == '105':
            print('Партнер заблокирован для проведения Платежей')
            return
        elif data['RESULT'] == '0':
            print('Операция успешно выполнена')
            order.transaction_id = data['PAY_ID']
            order.save()
            self.send_mail_link(data, order)
        elif data['RESULT'] == '2':
            print('Wrong parameter {}'.format(data['RESULT_DESC']))
            return
        elif data['RESULT'] == '3':
            print('Smth wrong with system')
            return
        elif data['RESULT'] == '106':
            print('Payment in progress or already done')
            print(data['PAY_ID'], data['STATUS'], data['SDCODE'])
            return
        elif data['RESULT'] == '108':
            print('Wrong operation')
            return
        else:
            print('another error')
            return

    def create_params(self, data):
        price = data.total*100
        now = datetime.datetime.now()
        hashed_data = hashlib.md5(
            str.encode(
                environ['ID_TERMINAL'] +
                environ['LOGIN'] +
                environ['PASSWORD']))
        params = {
            'OPERATION': 'CreatePayment',
            'TERMINAL_ID': environ['ID_TERMINAL'],
            'ARTICLE_ID': environ['ID_ARTICLE'],
            'MPAY_ID': data.mpay_id,
            'MDATETIME': now.isoformat(),
            'AMOUNT': price,
            'CURRENCY': 'RUR',
            'RETURN_URL': environ['RETURN_URL'],
            'FAIL_URL': environ['FAIL_URL'],
            'IDENTITY': hashed_data.hexdigest()}
        return params

    def response_to_dict(self, data):
        splitted_list = data.text.split('&')
        new_splitted_list = []
        for item in splitted_list:
            new_splitted_list.append(item.split('='))
        return dict(new_splitted_list)


    @detail_route(methods=['post'])
    def shipped_order(self, request, pk):
        """Refund the order specified by the pk
        """
        order = Order.objects.get(id=pk)
        order.shipped()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @detail_route(methods=['post'])
    def fulfill_order(self, request, pk):
        """Mark the order specified by pk as fulfilled
        """
        order = Order.objects.get(id=pk)
        order.mpay_id = order.id
        response = requests.post(
            'https://w.red-pay.ru/partner/3/acquiring',
            data=self.create_params(order))
        new_response = self.response_to_dict(response)
        self.analyze_response(new_response, order)

        order.fulfill()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @detail_route(methods=['post'])
    def in_process_order(self, request, pk):
        """Mark the order specified by pk as fulfilled
        """
        order = Order.objects.get(id=pk)
        order.in_process()
        return Response(status=status.HTTP_204_NO_CONTENT)
