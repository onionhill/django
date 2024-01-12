from django.shortcuts import render, get_object_or_404

# Create your views here.

from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Question, Choice
from django.template import loader
from django.urls import reverse

def index(request):
    question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"question_list": question_list }
    ##using Shortcut version
    return render(request, "polls/index.html", context)


    ##No shortcut
    template = loader.get_template("polls/index.html")
    
    return HttpResponse(template.render(context, request))

def details(request, question_id):

    #using 404 shortcut
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})


    #No shortcut 
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, "polls/detail.html",{'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {'question': question} )

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        print("data", request.POST["choice"])
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a valid choice"
            }    
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()


        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    

