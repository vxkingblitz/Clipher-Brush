from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category, MarkersSet
from .serializers import CategorySerializer, MarkersSetSerializer


class CategoryListView(APIView):
    def get(self, request, category_id=None):
        if category_id is not None:
            category = get_object_or_404(Category, pk=category_id)
            serializer = CategorySerializer(category)
            return Response(serializer.data)

        
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class MarkersSetListView(APIView):
    def get(self, request):
        markers_sets = MarkersSet.objects.all()
        serializer = MarkersSetSerializer(markers_sets, many=True)
        return Response(serializer.data)
