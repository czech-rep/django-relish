from django.shortcuts import render, redirect
from django.http import HttpResponse # thats for returning plain text, like:
    # return HttpResponse("return this string")

from .resizer import *

from .models import TagName, Image

def hello(request):
    return HttpResponse('hello from hello view function')


# def post_image(request):
#     if request.method == "POST":
#         print('start')
#         img = request.POST.get('image')
#         i = Image(image=img, title='test')
#         i.save()
#         img_id = i.id
#         print(img_id)
#         print(type(i.image))
#         print(i.image.url)
#         info = 'successfully uploaded'

#         # return redirect()
#         return HttpResponse('zapisano obrazek')
#         # render(request, 'meme_sorter/image_details.html')

#     return render(request, 'meme_sorter/post_image.html')

def index(request):
    tags = TagName.objects.all().order_by('name')
    memes = Image.objects.exclude(image='').all()
    mem_count = memes.count()
    args = {
        'tags' : tags
        , 'memes': memes
        , 'mem_count': mem_count
    }
    return render(request, 'meme_sorter/index.html', args)


from .forms import ImageForm
def post_image_form(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES) 
        if form.is_valid():
            # print(request.FILES)
            # print(type(request.FILES))
            # print(request.FILES[filename].size)
            author = request.user
            print(author)
            form.instance.added_by = author
            task = form.save()

            title, adres = form.cleaned_data['title'], form.cleaned_data['image'] # thats one way
            id_ = task.id
            info = f'zapisano obrazek: {title} , adres: {adres} , id: {id_}'
            # print(info)
            return redirect('image_details', id_)

    form = ImageForm()
    args = {
        'form' : form
    }
    return render(request, 'meme_sorter/post_image_form.html', args)

def image_details(request, img_id):
    meme = Image.objects.filter(id=img_id).first()

    current_tags = TagName.objects.filter(pk__in=meme.tags.all()).order_by('name')
    tags = TagName.objects.all().order_by('name')
    info = ''

    if request.method == "POST": # so we wrote a tag name
        # content = request.POST.get('new_tag')
        # print(request.body) # raw

        name = request.POST.get('tag_name')
        num_results = TagName.objects.filter(name = name).count() # check if tag exists
        if num_results == 0:        # tag is totally new
            id_ = new_tag(name)
        else:
            id_ = TagName.objects.filter(name=name).first().id # tag already exists - extract its id
        return redirect('add_chosen_tag', img_id, id_, 'add')

    args = {
        'meme': meme
        , 'current_tags': current_tags
        , 'tags_count': len(current_tags)
        , 'tags': tags
    }
    return render(request, 'meme_sorter/image_details.html', args)


def image_resize(request, img_id):

    meme = Image.objects.get(id=img_id)
    name = meme.image.url.split('/')[-1]
    extention = name.split('.')[-1]
    ext_len = len(extention)
    new_name = name[:-ext_len+1] + '_resized.' + extention # add '_resized' to filename - move that to function
    # print(new_name)
    dane = {
        'height': meme.image.height
        , 'width': meme.image.width
        , 'size': meme.image.size
        , 'name': name
    }
    args = {
        'meme': meme
        , 'dane': dane
        # , 'resized_files': []
        , 'new_dims': None
    }
    new_dims = {'height':'primary'}

    if request.method == 'POST':
        # also after check here corrected parameters will be provided
        dimentions = request.POST.get('height'), request.POST.get('width')
        new_dims['height'], new_dims['width'] = [int(value) if value else None for value in dimentions ]

        preserve = request.POST.get('preserve_ratio')

        if 'calculate' in request.POST: # so check input parameters
            try:
                ratio = meme.image.height / meme.image.width            # we may need original ratio
                new_height, new_width = calculate_dims(new_dims, preserve, ratio)   # returns integers - computed dimentions
                new_dims = {'height': new_height, 'width': new_width}
                
                args['new_dims'] = new_dims                                     # means we have new correct dims
                args['set_readonly'] = 'readonly="true"'             # lock input fields
            except resize_params_error as e:
                new_dims = None
                args['calculate_info'] = e.ms

        elif 'download' in request.POST: # so input is checked
            print(new_dims)
            return resize_and_send(meme.image.url, (new_dims['height'], new_dims['width']), name)
        elif 'unlock' in request.POST: # so input is checked
            None        # just refresh page to clear fields

    return render(request, 'meme_sorter/image_resize.html', args)



# lets create functions: add tag to database, assign tag to image
def new_tag(name):
    t = TagName(name=name)
    t.save()
    return t.id


def add_chosen_tag(request, img_id, tag_pk, action): # only for tags from database
    try:
        tag = TagName.objects.get(id=tag_pk) # tag object we have
    except TagName.DoesNotExist:
        return redirect('error_page', 'tag does not exist')
    try:
        img = Image.objects.get(id=img_id) # image object
    except Image.DoesNotExist:
        return redirect('error_page', 'image not exists')
    

    if action == 'add':    
        if img.tags.filter(id=tag_pk):
            return redirect('error_page', 'tag already added') # this is not working

        img.add_tag(tag_pk) # functions from .models
    elif action == 'del':
        img.remove_tag(tag_pk)          # czy na pewno chcesz usunąć?
    else:
        return redirect('error_page', 'incorrect action')
    return redirect('image_details', img_id)


def tag(request, tag_name):
    try:
        id_ = TagName.objects.get(name=tag_name).id # do zmiany - tagi unikalne
    except TagName.DoesNotExist:
        return redirect('error_page', f'tag {tag_name} nie istnieje')

    memes = Image.objects.filter(tags=id_).all()
    mem_count = len(memes)
    tags = TagName.objects.all().order_by('name')
    args = {
        'tag_name': tag_name
        ,'mem_count': mem_count
        ,'tags': tags
        , 'memes': memes
    }
    return render(request, 'meme_sorter/tag_page.html', args)


def delete_image(request, img_id):
    try:
        img = Image.objects.get(id=img_id) # image object
    except Image.DoesNotExist:
        return redirect('error_page', 'image not found')
    
    # title = img.title
    for tag in img.tags.all():
        print('del ', tag.name)
        img.remove_tag(tag.id) 
        
    img.delete()
    return redirect('index')


def count_memes(request, tag_name):
    id_ = TagName.objects.filter(name=tag_name).first().id

# def tags(request):
#     return render(request, 'meme_sorter/tags.html')