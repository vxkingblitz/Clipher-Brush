from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category, MarkersSet
from .serializers import CategorySerializer, MarkersSetSerializer


class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class MarkersSetListView(APIView):
    def get(self, request):
        markers_sets = MarkersSet.objects.all()
        serializer = MarkersSetSerializer(markers_sets, many=True)
        return Response(serializer.data)
