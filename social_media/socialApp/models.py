from django.db import models
from django.contrib.auth.models import User #Esta es una tabla propia de django
                                            #Nosotros solo tomaremos el dato User de ella
from django.utils import timezone #Con esto nos permitira utilizar el timestamp para que Nosotros
                                  #de el momento exacto en que el usuario publica un post


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='batman.png')

    def __str__(self):
        return f'Profile of {self.user.username}'

    def following(self):
        user_ids = Relationship.objects.filter(from_user=self.user)\
                                .values_list('to_user_id', flat=True)
        return User.objects.filter(id__in=user_ids)

    def followers(self):
        user_ids = Relationship.objects.filter(to_user=self.user)\
                                .values_list('from_user_id', flat=True)
        return User.objects.filter(id__in=user_ids)

class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    timestamp = models.DateTimeField(default=timezone.now)
    content = models.TextField()

    class Meta: #La clase meta sirve para establece el corpontamiento de la clase
        ordering = ['-timestamp']#Ordena los post de manera descendente
    def __str__(self):
        return f'{self.user.username} : {self.content}'
        #Con esto identificamos el usuario con su contenido generado

class Relationship(models.Model):
    from_user = models.ForeignKey(User, related_name='relationships', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='related_to', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.from_user} to {self.to_user}'

    class Meta:
        indexes = [
           models.Index(fields=['from_user', 'to_user',]),
        ]
