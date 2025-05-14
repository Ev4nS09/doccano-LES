from rest_framework import generics
from projects.models import Perspective, UserPerspective
from projects.serializers import PerspectiveSerializer, UserPerspectiveSerializer

class PerspectiveListCreateView(generics.ListCreateAPIView):
    queryset = Perspective.objects.all()
    serializer_class = PerspectiveSerializer


class PerspectiveDeleteView(generics.DestroyAPIView):
    queryset = Perspective.objects.all()
    serializer_class = PerspectiveSerializer
    lookup_field = 'perspective_id'

class UserPerspectiveListCreateView(generics.ListCreateAPIView):
    queryset = UserPerspective.objects.all()
    serializer_class = UserPerspectiveSerializer


class UserPerspectiveDeleteView(generics.DestroyAPIView):
    queryset = UserPerspective.objects.all()
    serializer_class = UserPerspectiveSerializer
    lookup_field = 'pk'
