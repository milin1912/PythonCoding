from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import AlbumForm, UserForm
from .models import Album

ImageFiles = ['png', 'jpg', 'jpeg']



def create_album(request):
    if not request.user.is_authenticated():
        return render(request, 'myapp/login.html')
    else:
        form = AlbumForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            album = form.save(commit=False)
            album.user = request.user
            album.upload = request.FILES['upload']
            file_type = album.upload.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in ImageFiles:
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'myapp/create_album.html', context)
            album.save()
            return render(request, 'myapp/detail.html', {'album': album})
        context = {
            "form": form,
        }
        return render(request, 'myapp/create_album.html', context)




def delete_album(request, album_id):
    album = Album.objects.get(pk=album_id)
    album.delete()
    albums = Album.objects.filter(user=request.user)
    return render(request, 'myapp/index.html', {'albums': albums})


def detail(request, album_id):
    if not request.user.is_authenticated():
        return render(request, 'myapp/login.html')
    else:
        user = request.user
        album = get_object_or_404(Album, pk=album_id)
        return render(request, 'myapp/detail.html', {'album': album, 'user': user})


def index(request):
    if not request.user.is_authenticated():
        if not request.email.is_authenticated():
            return render(request, 'myapp/login.html')
    else:
        albums = Album.objects.filter(user=request.user)
        query = request.GET.get("q")
        if query:
            albums = albums.filter(
                Q(album_title__icontains=query) |
                Q(artist__icontains=query)
            ).distinct()
            return render(request, 'myapp/index.html', {
                'albums': albums,
            })
        else:
            return render(request, 'myapp/index.html', {'albums': albums})


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'myapp/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'myapp/index.html', {'albums': albums})
            else:
                return render(request, 'myapp/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'myapp/login.html', {'error_message': 'Invalid login'})
    return render(request, 'myapp/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'myapp/index.html', {'albums': albums})
    context = {
        "form": form,
    }
    return render(request, 'myapp/register.html', context)
