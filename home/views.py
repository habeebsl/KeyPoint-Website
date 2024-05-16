from django.shortcuts import render, redirect
from .utils import KeyPoint
import json
from .forms import EmphasisDataForm, SaveDataForm, ChangeUsername
from .models import SavedData
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse


@login_required
def generateEmphasisView(request):
    processed = None
    processed_data = None
    form = EmphasisDataForm(request.POST or None)

    try:
        if request.method == 'POST' and form.is_valid():
            input=form.cleaned_data['text']
            instance = KeyPoint(input)
            processed = instance.emphasizer()
            processed_data = processed[0]

            if processed[1] == None or "":
                save_data = SavedData(title="No Title", data=processed[0], author=request.user)
                save_data.save()
            else:
                save_data = SavedData(title=processed[1], data=processed[0], author=request.user)
                save_data.save()
        return render(request, 'emphasize_text.html', {'emphasized_text':processed_data, 'form':form})
    except (json.decoder.JSONDecodeError, ValueError):
        print(Exception)
        return TemplateResponse(request, 'error_page.html')

    


def homePageView(request):
    if request.user.is_authenticated:
        user_data = SavedData.objects.filter(author=request.user)
        reversed_user_data = user_data[::-1]
        context = {
            'historical_chats':reversed_user_data
        }

        return render(request, 'home.html', context)
    else:
        return render(request, 'home.html')



def emphasisHistoryView(request, slug):
    get_saved_data = SavedData.objects.get(slug=slug)

    return render(request, 'detail_page.html', {"data":get_saved_data})


class EditTitle(UpdateView):
    template_name = 'edit_title.html'
    model = SavedData
    form_class = SaveDataForm
    success_url = '/'
    context_object_name = 'savedata'


def settings_page(request):
    if request.method == 'POST':
        form = ChangeUsername(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

            return redirect('/')  # Redirect to profile page or any other page
    else:
        form = ChangeUsername(instance=request.user)


    return render(request, 'settings.html', {'form': form})


class DeleteHighlightView(DeleteView):
    template_name = 'delete_highlight.html'
    model = SavedData
    success_url = reverse_lazy('home')
    context_object_name = 'savadata'
