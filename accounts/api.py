# accounts/api.py
from rest_framework import serializers, viewsets
from .models import Mensaje

class MensajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mensaje
        fields = ['cliente', 'mensaje', 'fecha_envio']

class MensajeViewSet(viewsets.ModelViewSet):
    queryset = Mensaje.objects.all()
    serializer_class = MensajeSerializer
