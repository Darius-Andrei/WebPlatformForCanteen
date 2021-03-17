from django.db import models
from django.contrib.auth.models import User
from datetime import date

#clasa specifica bucatarului
class newChef(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    nume = models.CharField(max_length=100, null=True)
    prenume = models.CharField(max_length=100, null=True)
    imagine = models.ImageField(upload_to='profiluri', null=True)

    def __str__(self):
        return self.user.username

#clasa specifica utilizatorului
class newUser(models.Model):

    TIP_UTILIZATOR=[
        ('student', "student"),
        ('profesor', "profesor"),
    ]
    user=models.OneToOneField(User,null=True,on_delete=models.CASCADE )

    tip=models.CharField(max_length=100, choices=TIP_UTILIZATOR, null=True)
    email=models.EmailField(null=True)
    nume=models.CharField(max_length=100, null=True)
    prenume = models.CharField(max_length=100, null=True)
    facultate = models.CharField(max_length=100, null=True)
    nr_matricol= models.CharField(max_length=100,null=True)
    nr_telefon= models.CharField(max_length=100,null=True)
    cerere_abonament=models.BooleanField(default=False)
    abonament =models.BooleanField(default=False)
    reducere= models.PositiveIntegerField(default=0)
    data_expirare= models.DateField(default=date.today())

    USERNAME_FIELD='user'

    def __str__(self):
        return self.user.username

#clasa specifica produsului din meniu
class newProduct(models.Model):
    bucatar=models.ForeignKey(User, on_delete=models.CASCADE)
    nume = models.CharField(max_length=100, null=True)
    pret = models.DecimalField(max_digits=4, decimal_places=2)
    ingrediente= models.CharField(max_length=300, null=True)
    alergeni = models.CharField(max_length=300, null=True)
    observatii= models.CharField(max_length=300, null=True)
    imagine=models.ImageField(upload_to='images', null=True)

    stoc=models.IntegerField(default=1)

    def __str__(self):
        return self.nume

#clasa specifica produsului din cos
class orderedItem(models.Model):
    product=models.ForeignKey(newProduct, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(newUser, on_delete=models.CASCADE, null=True)
    comandat = models.BooleanField(default=False)
    cantitate_comandata=models.IntegerField(default=1)

    def __str__(self):
        return self.product.nume

    def get_price(self):
        return self.cantitate_comandata * self.product.pret

#clasa specifica cosului
class cos(models.Model):
    produse = models.ManyToManyField(orderedItem, blank=True)
    user= models.ForeignKey(newUser, null=True,on_delete=models.CASCADE)
    dataComandare = models.DateTimeField(auto_now=True, null=True)

    def produse_cos (self):
        return self.produse.all()

    def nr_prod (self):
        return self.produse_cos().count()

    def pret_total (self):
        pretTotal= sum([item.get_price() for item in self.produse.all()])
        return pretTotal - (self.user.reducere*pretTotal/100)

#clasa specifica datelor legate de contact
class newContact(models.Model):
    locatie=models.CharField(max_length=300, null=True)
    email=models.EmailField(null=True)
    numele_strazii=models.CharField(max_length=300, null= True)


    def __str__(self):
        return self.numele_strazii












