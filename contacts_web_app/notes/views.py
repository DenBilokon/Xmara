from datetime import date
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import NoteForm, TagForm
from .models import Tag, Note
from users.views import currency_parse, weather_parse



def main(request):
    currency_info = currency_parse()
    weather_info = weather_parse()
    notes = Note.objects.filter(user=request.user).all() if request.user.is_authenticated else []
    return render(request, 'notes/index.html', context={'notes': notes, 'currency_info': currency_info,
                                                        'date': date.today().strftime('%d.%m.%Y'),
                                                        'weather_info': weather_info})

@login_required
def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
            return redirect(to='notes:main')
        else:
            return render(request, 'notes/tag.html', {'form': form})

    return render(request, 'notes/tag.html', {'form': TagForm()})

@login_required
def note(request):
    tags = Tag.objects.filter(user=request.user).all()

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            new_note = form.save(commit=False)
            new_note.user = request.user
            new_note.save()
            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'), user=request.user)
            for tag in choice_tags.iterator():
                new_note.tags.add(tag)

            return redirect(to='notes:main')
        else:
            return render(request, 'notes/note.html', {'tags': tags, 'form': form})

    return render(request, 'notes/note.html', {'tags': tags, 'form': NoteForm()})

@login_required
def detail(request, note_id):
    note = get_object_or_404(Note, pk=note_id, user=request.user)
    return render(request, 'notes/detail.html', {'note': note})

@login_required
def set_done(request, note_id):
    Note.objects.filter(pk=note_id, user=request.user).update(done=True)
    return redirect(to='notes:main')

@login_required
def delete_note(request, note_id):
    Note.objects.get(pk=note_id, user=request.user).delete()
    return redirect(to='notes:main')