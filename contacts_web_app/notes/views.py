from datetime import date
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from .forms import NoteForm, TagForm
from .models import Tag, Note

from users.models import Avatar

def main(request):
    """
    The main function is the view for the main page of our site.
    It displays all notes and tags that belong to a user if they are logged in, or an empty list otherwise.
    It also paginates notes so that only 9 are displayed per page.
    
    :param request: Get the current request object
    :return: A render function
    :doc-author: Trelent
    """
    avatar = Avatar.objects.filter(user_id=request.user.id).first()
    notes = Note.objects.filter(user=request.user).all() if request.user.is_authenticated else []
    tags = Tag.objects.filter(user=request.user).all() if request.user.is_authenticated else []
    paginator = Paginator(notes, 9)
    page_number = request.GET.get('page', 1)
    try:
        pages = paginator.page(page_number)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)
    return render(request, 'notes/index.html', context={'notes': pages, 'tags': tags, 'avatar': avatar})



@login_required
def tag(request):
    """
    The tag function is used to create a new tag.
        It takes in the request and returns a rendered template of the form.
        If it's a POST request, then it will save the data from that form into our database.
    
    :param request: Get the current request object
    :return: A redirect to the main page
    :doc-author: Trelent
    """
    avatar = Avatar.objects.filter(user_id=request.user.id).first()
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
    """
    The note function is responsible for creating a new note.
    It first gets all the tags that belong to the user and passes them to the template.
    Then it checks if there was a POST request, which means that someone submitted data through our form.
    If so, we create an instance of NoteForm with this data and check if it's valid (if all fields are filled correctly). If not, we render our template again but this time with errors in form fields (they will be highlighted). Otherwise we save our new note without committing changes yet because we need to add some tags first. Then we get all chosen tags from request body and
    
    :param request: Get the data from the form
    :return: The note
    :doc-author: Trelent
    """
    avatar = Avatar.objects.filter(user_id=request.user.id).first()
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
    """
    The detail function is used to display a single note.
    It takes the request and the note_id as parameters, and returns a rendered template with the requested note.
    If no such note exists, it raises an Http404 exception.
    
    :param request: Get the current user
    :param note_id: Retrieve the note from the database
    :return: A httpresponseredirect object
    :doc-author: Trelent
    """
    avatar = Avatar.objects.filter(user_id=request.user.id).first()
    note = get_object_or_404(Note, pk=note_id, user=request.user)
    return render(request, 'notes/detail.html', {'note': note})


@login_required
def set_done(request, note_id):
    """
    The set_done function takes a request and note_id as arguments.
    It then filters the Note objects by the primary key of note_id, 
    and updates the done field to True. It then redirects to 'notes:main'. 
    
    :param request: Get the user from the request object
    :param note_id: Find the note that we want to mark as done
    :return: A redirect to the main page
    :doc-author: Trelent
    """
    Note.objects.filter(pk=note_id, user=request.user).update(done=True)
    return redirect(to='notes:main')


@login_required
def delete_note(request, note_id):
    """
    The delete_note function takes in a request and note_id,
        then deletes the Note object with the given id.
        It redirects to 'notes:main' after deleting.
    
    :param request: Get the user information from the request object
    :param note_id: Find the note to delete
    :return: A redirect to the main view
    :doc-author: Trelent
    """
    Note.objects.get(pk=note_id, user=request.user).delete()
    return redirect(to='notes:main')


@login_required
def edit_note(request, note_id):
    """
    The edit_note function is responsible for editing a note.
    It takes the request and note_id as parameters, gets the Note object with that id or returns 404 if it doesn't exist,
    gets all tags of this user and checks if the request method is POST. If so, it creates a form from NoteForm class with
    the data from POST request and instance of edited note (note). If form is valid then we create an edited_note variable 
    with data from form but without saving to database yet. Then we set its user attribute to current logged in user 
    (request.user) and save it to database using .
    
    :param request: Get the request object
    :param note_id: Get the note object from the database
    :return: The render function
    :doc-author: Trelent
    """
    avatar = Avatar.objects.filter(user_id=request.user.id).first()
    note = get_object_or_404(Note, pk=note_id, user=request.user)
    tags = Tag.objects.filter(user=request.user).all()

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            edited_note = form.save(commit=False)
            edited_note.user = request.user
            edited_note.save()
            edited_note.tags.clear()
            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'), user=request.user)
            for tag in choice_tags.iterator():
                edited_note.tags.add(tag)

            return redirect(to='notes:main')
        else:
            return render(request, 'notes/edit_note.html', {'note': note, 'tags': tags, 'form': form})

    form = NoteForm(instance=note)
    return render(request, 'notes/edit_note.html', {'note': note, 'tags': tags, 'form': form})

@login_required
def search(request):
    """
    The search function takes a request and returns the search results.
    If there is no query in the request, it redirects to main.
    Otherwise, it filters notes by name or description and renders them.
    
    :param request: Pass the request object to the view
    :return: A list of notes that match the query
    :doc-author: Trelent
    """
    avatar = Avatar.objects.filter(user_id=request.user.id).first()
    if 'query' in request.GET:
        query = request.GET['query']
        notes = Note.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query),
            user=request.user
        )
        return render(request, 'notes/search_results.html', {'notes': notes})
    else:
        return redirect(to='notes:main')

@login_required
def sort(request):
    """
    The sort function takes in a request object and returns the search_results.html template with notes that have been filtered by tags selected by the user.
    
    :param request: Get the request object
    :return: A list of notes that have the selected tags
    :doc-author: Trelent
    """
    avatar = Avatar.objects.filter(user_id=request.user.id).first()
    if request.method == 'GET':
        selected_tags = request.GET.getlist('selected_tags')
        notes = Note.objects.filter(tags__name__in=selected_tags, user=request.user).distinct()
        return render(request, 'notes/search_results.html', {'notes': notes, 'selected_tags': selected_tags})
    else:
        return redirect(to='notes:main')
