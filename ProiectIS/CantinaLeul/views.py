import datetime

from django.contrib.auth import authenticate, logout, login
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from ProiectIS.settings import EMAIL_HOST_USER
from .models import *
from .forms import *
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from datetime import date
#acest view ne redirecteza pe primapagina al site-ului si trimite mai departe bucatarii
#                                     pe prima pagina pentru a afisa lista acestora
def Index(request):
    bucatari=newChef.objects.all()
    context={'bucatari': bucatari}
    return render(request, 'primaPagina.html', context)

#acest view ne redirecteza pe primapagina al site-ului dupa ce ne-am logat
def LoggedIn(request):
    return render(request, 'index.html')

#acest view ne redirecteza pe pagina cu Locatia
def Locatie(request):
    contact=newContact.objects.all()
    return render(request, 'locatie.html', {'contact':contact[0]})
#acest view ne redirecteza pe pagina html care ne explica cum sa facem cont
def Obtinere_cont(request):
    return render(request, 'ajutor.html')

#acest view ne completeaza casutele corespunzatoare fiecarui cont, formeaza o instanta
#                           a clasei newUser si il salveaza daca toate datele sunt in regula
#de asemenea se diferenteaza studentul de profesor caruia i se seteaza reducerea de 100%
def createAccount(request):
    if request.method == 'POST':
        tip=request.POST['tip']
        username = request.POST['username']
        nume = request.POST['nume']
        prenume = request.POST['prenume']
        facultate = request.POST['facultate']
        nr_matricol = request.POST['nr_matricol']
        nr_telefon = request.POST['nr_telefon']
        email = request.POST['email']
        parola= request.POST['parola']
        parola2= request.POST['parola2']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Utilizator existent deja")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email existent deja")
            return redirect('register')

        if parola!=parola2:
            messages.error(request, "Parolele nu coincid")
            return redirect('register')

        if len(parola) < 8:
            messages.error(request, "Parola prea scurta")
            return redirect('register')

        user= User.objects.create_user(username=username, password=parola)
        user.is_active=False
        user.save()
        if tip=='student':
            student=newUser(user=user, tip='student', nume=nume, prenume=prenume, facultate=facultate, nr_matricol=nr_matricol, nr_telefon=nr_telefon, email=email)
            student.save()
        else:
            profesor=newUser(user=user, tip='student', nume=nume, prenume=prenume, facultate=facultate, nr_matricol=nr_matricol, nr_telefon=nr_telefon, abonament=True,data_expirare=datetime.datetime(2120,12,31), reducere=100, email=email)
            profesor.save()
        return redirect('home')



    TIP_UTILIZATOR = [
        ('student', "student"),
        ('profesor', "profesor")
    ]
    context={
        'tip': TIP_UTILIZATOR,
    }
    return render(request,'register.html', context)


#acest view foloseste sistemul de login existent in Django
#pe baza unor requesturi, daca datele sunt corespunzatoare, utilizatorul este logat si trimis pe prima pagina dupa logare
def loginPersoana(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method=="POST":
            username=request.POST.get('username')
            password=request.POST.get('password')
            user=authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home_logged_in')
            else:
                messages.error(request, "User/Parola gresite")
                return redirect('login')
        return render(request, 'registration/login.html')

#acest view foloseste sistemul incorporat de Django pentru a face delogarea
def logoutPersoana(request):
    logout(request)
    return redirect('login')



#acest view  este folosit pentru adaugarea produsului in meniu
#avem nevoie de id-ul bcatarului pe care il conectam produsului, dupa care salvam un formular
#                       pe care il trimitem mai departe pe prima pagina dupa login
def addProduct(request):
    bucatar=request.user
    if request.method=='POST':
        formular = newProductForm(request.POST, request.FILES)

        if formular.is_valid():
            dummy=formular.save(commit=False)
            dummy.bucatar=bucatar
            dummy.save()
            return redirect('home_logged_in')
    else :
        formular = newProductForm()

    context={
        'formular':formular
    }
    return render(request, 'addProduct.html', context)

#acest view este folosit pentru modificarea produsului de catre bucatar
#se iau proprietatile obiectului, se modifica si se salveaza inapoi in baza de date
def modifyProduct(request, PrimaryKey):
    get_product=newProduct.objects.get(id=PrimaryKey)
    form = newProductForm(instance=get_product)
    if request.method=='POST':
        form=newProductForm(request.POST, request.FILES, instance=get_product)
        if form.is_valid():
            form.save()
    return render(request, 'modificareProdus.html', {'form':form})

#acest view randeaza pagina de meniu
#se trimit mai departe spre html pentru cos daca utilizatorul este de tip newUser sau newChef
#pentru a se stii ce fel de informatii se randeaza si ce anume se vede pentru fiecare categorie de utilizator
def paginaMeniu(request):
    produseBucatar=newProduct.objects.all()
    user = request.user
    bucatari=newChef.objects.all()
    emails=[bucatar.user.email for bucatar in bucatari]


    if user.email in emails:
        utilizatori = newChef.objects.get(user=user)
        return render(request, 'meniu.html', {'produseBucatar':produseBucatar, 'bucatari': utilizatori,'user': user,})
    else:
        notBucatari=newUser.objects.get(user=user)
        return render(request, 'meniu.html', {'produseBucatar': produseBucatar,'user':user, 'notBucatari':notBucatari,})


#acest view  este folosit la momentul in care se apasa pe Adauga de catre un utilizator
#acesta transforma un obiect de tip newProduct in tip orderedItem pentru cos
def adaugareCos(request, PrimaryKey):
    prod = get_object_or_404(newProduct, id=request.POST.get("adaugaButonCos"))
    get_client = newUser.objects.get(user=request.user)
    ordered_item,created=orderedItem.objects.get_or_create(product=prod, user=get_client, comandat=False)
    cos_get,created=cos.objects.get_or_create(user=get_client)
    if cos_get.produse.filter(product=prod).exists():
        ordered_item.cantitate_comandata += 1
        ordered_item.save()
        prod.stoc -= 1
        prod.save()
        return redirect('vizualizareCos')
    else:
        cos_get.produse.add(ordered_item)
        prod.stoc -= 1
        prod.save()
        return redirect('vizualizareCos')

# acest view este dedicat pentru eliminarea produselor din Cos de catre un utilizator
# cantitatea din cos se actualizeaza sau se sterge produsul cu totul si ne intoarcem tot pe vizualizareCos
def eliminareCos(request, PrimaryKey):
    prod = get_object_or_404(orderedItem, id=request.POST.get("stergereProdusCos"))
    get_client = newUser.objects.get(user=request.user)
    cos_get,created=cos.objects.get_or_create(user=get_client)
    if cos_get.produse.filter(product=prod.product, user=get_client).exists():
        if prod.cantitate_comandata>1:
            prod.cantitate_comandata -= 1
            prod.save()
            prod.product.stoc += 1
            prod.product.save()
            return redirect('vizualizareCos')
        else:
            prod.product.stoc += 1
            prod.product.save()
            cos_get.produse.remove(prod)
            return redirect('vizualizareCos')
    else:
        messages.info(request, "Produs inexistent in cos")
        return redirect('vizualizareCos')


#prin acest view se randeaza pagina html pentru cos unde ii trimitem
#obiectul de tip cos si clientul
def vizualizareCos(request):
    client=request.user
    get_client=newUser.objects.get(user=client)
    cos1 = cos.objects.get_or_create(user=get_client)
    produseCos=cos1[0].produse_cos()
    return render(request,'cos.html',{'user':get_client, 'produseCos':produseCos, 'cos':cos1[0]})


#prin acest view se permite schimbarea datelor de utilizator
#se iau datele din baza de date si se modifica, aceste modificari fiind posibile sa se modifice
def accountSettings(request):
    try:
        get_user=request.user.newuser
        form = myUserForm(instance=get_user)
        if request.method == 'POST':
            form = myUserForm(request.POST, instance=get_user)
            if form.is_valid():
                form.save()
        return render(request, 'dateUtilizator.html', {'form': form, 'user': get_user})
    except Exception:
        get_user = request.user.newchef
        form = myChefForm(instance=get_user)
        if request.method == 'POST':
            form = myChefForm(request.POST, instance=get_user)
            if form.is_valid():
                form.save()
        return render(request, 'dateUtilizator.html', {'form': form, 'user': get_user})

#acest view este dedicat modalitatii de schimbare a parolei
#datele email-ului corespunzator firmei sunt salvate in settings.
#datorita fisierului text care contine informatiile despre schimbarea codului se salveaza protocolul si domeniul
#                                                                 si se trimite prin functia send_mail emailul
def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "registration/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email,  EMAIL_HOST_USER , [user.email], fail_silently=False)
                        print("SUCCED")
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
                    return redirect("password_reset_done")
            messages.error(request, 'An invalid email has been entered.')
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="registration/password_reset.html", context={"password_reset_form": password_reset_form})


#acest view este responabil randarii paginilor privind abonarea
#in accest view se salveaza datele privind abonamentul si randeaza in functii de informatii
#daca avem sau nu abonament, data de expirare si reducerea
#in cazul in care nu avem abonament si se apasa pe butonul de cerere, se trimite un email cu instiintarea adminului
def abonament(request):
    myUser=newUser.objects.get(user=request.user)
    if myUser.abonament:
        if date.today()>myUser.data_expirare:
            myUser.abonament=False
            myUser.reducere=0
            myUser.save()
            return redirect('abonament')
        return render(request, 'abonament.html', {'user': myUser})
    else:
        if request.method=='POST':
            if myUser.cerere_abonament:
                messages.info(request, "Cererea a fost deja trimisă")
                return redirect('abonament')
            myUser.cerere_abonament=True
            myUser.save()
            messages.success(request, "Cererea ta a fost înregistrată")
            send_mail(
                'Cerere abonament',
                'Utilizatorul ' + myUser.user.username + ' dorește un abonament ',
                myUser.email,
                [EMAIL_HOST_USER,],
                fail_silently=False
            )
        return render(request, 'cerereAbonament.html')

#acest view reprezinta finalizarea Comenzii. Prin acesta se trimite un email cu detaliile atat adminului, cat si utilizatorului
def finalizareComanda(request, PrimaryKey):
    cosulMeu = cos.objects.get(id=PrimaryKey)
    produse=cosulMeu.produse.all()
    mesaj= "Produsele comandate de utilizatorul " + cosulMeu.user.user.username + " sunt:\n"

    for produs in produse:
        mesaj+= produs.product.nume + '\n'
    mesaj+="Preț total: " + str(cosulMeu.pret_total())
    send_mail(
        'Comanda noua',
        mesaj,
        EMAIL_HOST_USER,
        [EMAIL_HOST_USER, cosulMeu.user.email,],
        fail_silently= False

    )
    for produs in produse:
        cosulMeu.produse_cos().delete()

    return redirect('home_logged_in')


#acest view este folosit pentru eliminarea produselor din meniu de catre bucatari, dupa care ne redirecteaza tot pe aceasi pagina
def eliminareMeniu(request, PrimaryKey):
    print(PrimaryKey)
    produs=newProduct.objects.get(id=PrimaryKey)
    produs.delete()
    return redirect(reverse('meniu'))