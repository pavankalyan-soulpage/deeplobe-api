from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from ..serializers import (
    UserSerializer
)
from ...db.models import User

class UserCreate(APIView):

    # permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):

        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):

        request.data["author"] = request.user.id
        serializer = BlogSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogDetail(APIView):
    """
    Retrieve, delete a blog
    """

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        """
        Return blog object if pk value present.
        """
        try:
            return Blog.objects.get(pk=pk)
        except Blog.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        Return blog.
        """
        blog = self.get_object(pk)

        serializer = BlogSerializer(blog)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):

        blog = self.get_object(pk)
        serializer = BlogSerializer(blog, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Delete product.
        """
        blog = self.get_object(pk)
        blog.delete()
        return Response({"message": "Delete Success"}, status=status.HTTP_200_OK)

