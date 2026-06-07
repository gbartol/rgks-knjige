from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['display_name', 'avatar_url']
        read_only_fields = ['user']


class UserSummarySerializer(serializers.ModelSerializer):
    # Prikaz korisnika (rezultati pretrage, autor recenzije...).
    # Baziran na Profile-u: display_name/avatar_url su njegova polja, a id/username
    # dolaze s povezanog User-a.
    id = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'username', 'display_name', 'avatar_url']
