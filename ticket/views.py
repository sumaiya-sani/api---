from django.db.models import query
from django.http import response
from django.shortcuts import render
from django.http.response import Http404, JsonResponse
from.models import*
from.serializer import GuestSerializer,MovieSerializer,ReservationSerializer
from rest_framework import status,filters
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import generics,mixins
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from ticket import serializer
#1 without REST and no model query FBV 
def no_rest_no_model(request):
    guests=[
        {
            'id':1,
            'name':'Omar',
            'mobile':78887,
        },
        {
            'id':2,
            'name':'yassin',
            'mobile':64355566,
        }

    ]
    return JsonResponse(guests,safe=False)

#2 with model and query without Rest 
def no_rest_from_model(request):
    data=Guest.objects.all()
    response={
        'guests':list(data.values('name','mobile'))

    }
    return JsonResponse(response)







#GET 
@api_view(['GET','POST'])
def FBV_List(request):

    if request.method=='GET':
        guests=Guest.objects.all()
        serializer= GuestSerializer(guests,many=True)
        return Response(serializer.data)
        #POST
    elif request.method=='POST':
        serializer=GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)        


#3.1 GET PUT DELETE

@api_view (['GET','PUT','DELETE'])

def FBV_pk(request,pk):
    guest=Guest.objects.get(pk=pk)
    if request.method=='GET':
        serializer= GuestSerializer(guest)
        return Response(serializer.data)
#PUT      
    elif request.method=='PUT':
        serializer=GuestSerializer(guest,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)        

#DELETE
    if request.method=='GET':
       guest.delete()     
       return Response(status=status.HTTP_204_NO_CONTENT)
#CBV CLASS BASEAD VIEW 
# LIST CREATE 

class CBV_List(APIView):
    def get(self,request):
        gustes=Guest.objects.all()
        serializer=GuestSerializer(gustes,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer=GuestSerializer(data=request.data)
        if serializer.is_valid():
           serializer.save()
           return Response(
            serializer.data, status.HTTP_201_CREATED
        )
        return Response(serializer.data ,status=status.HTTP_400_BAD_REQUEST
        )

#GET PUT DELETE
class CBV_PK(APIView):
    def get_object(self,pk):
        try:
            return Guest.objects.all()
        except Guest.DoesNoxtExist:
            raise Http404

    def get(self,request,pk):
        guest=self.get_object(pk)
        serializer=GuestSerializer(guest) 
        return Response(serializer.data)
    def put(self,request,pk):
        guest=self.get.object(pk)
        serializer=GuestSerializer(guest,data=request.data)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk):
        guest=self.get_object(pk)  
        guest.delete()   
        return Response(status=status.HTTP_204_NO_CONTENT) 
#mixins
#mixins_list
class mixins_list(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset=Guest.objects.all()
    serializer_class=GuestSerializer
    def get(self,request):
        return self.list(request)
    def post(self,request):
        return self.create(request)
    authentication_classes=[BasicAuthentication]
    permission_classes=[IsAuthenticated]    
#5.2 mixins get put delete 

class mixins_pk(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset=Guest.objects.all()
    serializer_class=GuestSerializer
    def get(self,request,pk):
        return self.retrieve(request)
    def post(self,request,pk):
        return self.update(request)
    def delete(self,request,pk):
        return self.destroy(request)




