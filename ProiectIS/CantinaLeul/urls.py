from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.Index, name='home'), #url care ne redirecteaza acasa pe pagina principala
    path('logged_in', views.LoggedIn, name='home_logged_in'), #url care ne redirecteaza acasa pe pagina principala dupa logare
    path('locatie/', views.Locatie, name='locatie'), #url care ne redirecteaza pe pagina locatiei
    path('ajutor/', views.Obtinere_cont, name='ajutor'),#url care ne redirecteaza pe pagina de obtinere cont
    path('register/',views.createAccount, name='register'),#url care ne redirecteaza acasa pe pagina de inregistrare
    path('login/',views.loginPersoana, name='login'),#url care ne redirecteaza acasa pe pagina de accesare cont
    path('logout/',views.logoutPersoana, name='logout'), #url care ne redirecteaza acasa pe pagina de accesare cont dupa deconectare
    path('adauga_produs_meniu/', views.addProduct, name='adaugare_produs_meniu'),#url care ne redirecteaza pe pagina unde adauga bucatrii produse in meniu
    path('meniu/',views.paginaMeniu, name='meniu'),#url care ne redirecteaza pe pagina meniului
    path('adauga_in_cos/<str:PrimaryKey>', views.adaugareCos, name='adauga_in_cos'),#url care ne redirecteaza pe pagina in care adaugam in cos
    path('vizualizareCos/', views.vizualizareCos, name='vizualizareCos'),#url care ne redirecteaza pe pagina cosului
    path('elimina_din_cos/<str:PrimaryKey>', views.eliminareCos, name='elimina_din_cos'),#url care ne redirecteaza pe pagina de eliminare produselor
    path('elimina_din_meniu/<str:PrimaryKey>', views.eliminareMeniu, name='elimina_produs'),#url care ne redirecteaza la pagina de eliminare produselor din meniu de catre bucatari
    path('modifica_produs/<str:PrimaryKey>', views.modifyProduct, name='modifica_produs'),#url care ne redirecteaza pe modificarea produsului de catre bucatar
    path('dateUtilizator/', views.accountSettings, name='dateUtilizator'),#url care ne redirecteaza pe editarea datelor utilizator
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('password_reset', views.password_reset_request, name='password_reset'),
    #url care ne redirecteaza pe diferitele pagini pentru resetarea parolei
    path('abonament/', views.abonament, name='abonament'),#url care ne redirecteaza pe pagina specifica abonamentului
    path('finalizareComanda/<str:PrimaryKey>', views.finalizareComanda, name='finalizareComanda')#url care ne redirecteaza dupa apasarea butonului finalizareComanda

]
