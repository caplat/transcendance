from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, UserManager
# from django.shortcuts import  HttpResponseRedirect


LANGUAGE_CHOICES = (
    ('en', "english"),
    ('fr', "french"),
    ('es', "spanish"),
)

STATUS_CHOICES = (
    ('in game', "in game"),
    ('online', "online"),
    ('offline', "offline"),
)

# ************ >>>>>  placer dans game *****************************
class Player(models.Model):
    name = models.CharField(unique=True, max_length=50)
    points = models.IntegerField()  


class Score(models.Model):
    # pseudo = models.ForeignKey(User42, on_delete=models.CASCADE)         
    # points = models.IntegerField()     
    # player1 = models.CharField( max_length=50)
    players = models.ManyToManyField(Player)
    game_type = models.CharField(max_length=50)          
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player_name} - {self.points} points in {self.game_type} on {self.date_time.strftime('%Y-%m-%d %H:%M:%S')}"
# ************ placer dans game <<<<<  *****************************


class IDScore(models.Model):
    numberID = models.IntegerField()


class User42(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(unique=True, max_length=50)
    email = models.EmailField(unique=True)
    creation = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_connected = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    # toutes les donnees sont enregistrees dans games, on peut les recuperer via ID 
    # de la partie ? comme ca enregistre que une fois
    scores = models.ManyToManyField(IDScore, blank=True)

    status = models.CharField(choices=STATUS_CHOICES, default='offline')
    description = models.CharField(default='')
    image = models.ImageField(default="img/profil.png", null=True, blank=True, upload_to="img/")
    language = models.CharField(choices=LANGUAGE_CHOICES, default='en')
    friends = models.ManyToManyField('self', blank=True)
    blackList = models.ManyToManyField('self', blank=True, symmetrical=False)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FILEDS = []

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
  
    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def set_id_cookie(self, response):
        response.set_cookie(
            'user_id',
            self.id,
            secure=True,
            max_age=3600)
        return response

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = ("User")
        verbose_name_plural = ("Users")


class Friend_request(models.Model):
    from_user = models.ForeignKey(
        User42, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(
        User42, related_name='to_user', on_delete=models.CASCADE)
