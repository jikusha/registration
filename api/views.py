from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.views import APIView
from .models import *
from .serializer import *
from rest_framework.response import *
from rest_framework import status
# Create your views here.
from django.core.mail import send_mail

from django.views.decorators.csrf import csrf_exempt

import xlwt
import csv
from reportlab.pdfgen import canvas
from io import BytesIO

class UserList(APIView):
    def get(self,request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetail(APIView):
    def get_object(self, id):
        return get_object_or_404(User, pk=id)

    def get(self, request, id):
        user = self.get_object(id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def delete(self, request, id):
        user = self.get_object(id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContactList(APIView):
    def get(self,request):
        contacts = Contact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ContactDetail(APIView):
    def get_object(self, id):
        return get_object_or_404(Contact, pk=id)

    def get(self, request, id):
        contact = self.get_object(id)
        serializer = ContactSerializer(contact)
        return Response(serializer.data)

    def put(self, request, id):
        contact = self.get_object(id)
        serializer = ContactSerializer(contact, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        contact = self.get_object(id)
        contact.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PersonList(APIView):

    def get(self, request):
        persons = Person.objects.all()
        serializer = PersonSerializer(persons, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PersonDetail(APIView):

    def get_object(self, id):
        return get_object_or_404(Person, pk=id)

    def get(self, request, id):
        person = self.get_object(id)
        serializer = PersonSerializer(person)
        return Response(serializer.data)

    def put(self, request, id):
        person = self.get_object(id)
        serializer = PersonSerializer(person, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        person = self.get_object(id)
        person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def index(request, email):
    users = User.objects.all()
    for user in users:
        if user.email == email:
            password = user.password
    send_mail(
            'Hello From Jiku',
            password,
            'jikushandilya@gmail.com',
            [email],
            fail_silently=False
        )

    return HttpResponse(email)



@csrf_exempt
def export_contacts_xls(request, userId):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="contacts.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Contacts')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Name', 'Email', 'Phone' ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()



    rows = Contact.objects.all().filter(user = userId).values_list('name', 'email', 'phone')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def export_contacts_csv(request, userId):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="contacts.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name','Email','Phone'])

    contacts = Contact.objects.all().filter(user = userId).values_list('name', 'email', 'phone')
    for contact in contacts:
        writer.writerow(contact)

    return response


def export_contacts_xls_selected(request, ids):
    ids = ids[:-1]
    lst = [int(s) for s in ids.split(',')]
    print(lst)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="contacts.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Contacts')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Name', 'Email', 'Phone' ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()



    rows = Contact.objects.all().filter(id__in = lst).values_list('name', 'email', 'phone')




    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


