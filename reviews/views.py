from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, CreateView

from .forms import ReviewForm
from .models import Review


# Create your views here.

class ReviewView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "reviews/review.html"
    success_url = "/thank-you"


'''
Parte do código que usa FormView
class ReviewView(FormView):
    form_class = ReviewForm
    template_name = "reviews/review.html"
    success_url = "/thank-you"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    essa parte do código é para usar com View
    def get(self, request):
        form = ReviewForm()

        return render(request, "reviews/review.html", {
            "form": form
        })

    def post(self, request):
        form = ReviewForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/thank-you")
        
        return render (request, "reviews/review.html", {
            "form": form
        })
'''

class thankYouView(TemplateView):
    template_name = "reviews/thank_you.html" #nome do caminho

    def get_context_data(self, **kwargs): #guarda dicionário com dados de contexto para usar nos templates
        context = super().get_context_data(**kwargs)
        context['message'] = "this works"
        return context
    

class ReviewsListView(ListView):
    template_name = 'reviews/review_list.html'
    model = Review
    context_object_name = "reviews"

    def get_queryset(self):
        query_based = super().get_queryset()
        data = query_based.filter(rating__gt = 1)
        return data



class SingleReviewView(DetailView):
    template_name = "reviews/single_review.html"
    model = Review

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loaded_review = self.object
        request = self.request
        favorite_id = request.session.get("favorite_review")
        context["is_favorite"] = favorite_id == str(loaded_review.id)
        return context


class AddFavoriteView(View):
    def post(self, requests):
        review_id = requests.POST['review_id']#pegamos a nossa review
        requests.session["favorite_review"] = review_id #salvamos em uma session, django automaticamente salva em um banco
        return HttpResponseRedirect("/reviews/"+review_id)#redirecionamos a página




