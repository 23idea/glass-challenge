from django.shortcuts import render
from django.views import generic
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render_to_response
from django.template import RequestContext
from challenge import models as db
from challenge import form


def index(request):
    
    if request.user.is_authenticated() and not request.user.challenge_user.added_username:
        return HttpResponseRedirect(reverse_lazy('user_edit'))

    challenges = db.Challenge.objects.annotate(votecount=Sum("vote__direction"))

    if request.GET.get("cat"):
        challenges = challenges.filter(category__pk=request.GET.get("cat"))

    uncomplete = challenges.filter(status="Uncomplete")
    complete = challenges.filter(status="Finished")

    if request.GET.get("sort-complete"):
        if request.GET.get("sort-complete") == "votecount":
            complete = complete.filter(votecount__isnull=False)

        if request.GET.get("dir") == "d":
            complete = complete.order_by("-"+request.GET.get("sort-complete"))
        else:
            complete = complete.order_by(request.GET.get("sort-complete"))

    if request.GET.get("sort-uncomplete"):
        if request.GET.get("sort-uncomplete") == "votecount":
            uncomplete = uncomplete.filter(votecount__isnull=False)
        if request.GET.get("dir") == "d":
            uncomplete = uncomplete.order_by("-"+request.GET.get("sort-uncomplete"))
        else:
            uncomplete = uncomplete.order_by(request.GET.get("sort-uncomplete"))

    categories = db.Category.objects.all()

    for challenge in uncomplete:
        try:
            vote = db.Vote.objects.get(user=request.user, challenge=challenge)
        except (db.Vote.DoesNotExist,  TypeError):
            setattr(challenge, "vote", "none")
        else:
            if vote.direction == 1:
                setattr(challenge, "vote", "up")
            elif vote.direction == -1:
                setattr(challenge, "vote", "down")

    return render(request, 'challenge/index.jade', {
        'complete': complete,
        'uncomplete': uncomplete,
        'user': request.user,
        'categories': categories
    })


class UserView(generic.DetailView):
    """
    my challenges
    """
    model = db.User
    context_object_name = "cuser"
    template_name = 'challenge/user.jade'

    def get_context_data(self, **kwargs):
        context = super(UserView, self).get_context_data(**kwargs)
        context['challenges'] = db.Challenge.objects.filter(author=kwargs['object'])
        context['claims'] = db.Claim.objects.filter(author=kwargs['object'])
        return context


class ChallengeDetail(generic.DetailView):
    """
    details on a challenge
    """
    model = db.Challenge
    template_name = 'challenge/details.jade'

    def get_context_data(self, **kwargs):
        context = super(ChallengeDetail, self).get_context_data(**kwargs)
        context['claims_pending'] = db.Claim.objects.filter(challenge=kwargs['object'], status="Pending" )

        context['claims_accepted'] = db.Claim.objects.filter(challenge=kwargs['object'], status="Accepted" )
        #check if use has a claim on  this challenge yet
        if self.request.user.is_authenticated() and db.Claim.objects.filter(author=self.request.user, challenge=kwargs['object']).count():
            context['has_claim'] = db.Claim.objects.get(author=self.request.user, challenge=kwargs['object']).id
        return context


class ChallengeCreate(generic.CreateView):
    """
    submit a new challenge
    """
    template_name = 'challenge/challenge_form.jade'
    form_class = form.ChallengeForm
    model = db.Challenge

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(ChallengeCreate, self).form_valid(form)


class ChallengeUpdate(generic.UpdateView):
    """
    edit challenge
    reate a form instance with POST data.
    >>> a = Author()
    >>> f = AuthorForm(request.POST, instance=a)

    >>> new_author = f.save()
    """
    model = db.Challenge
    template_name = 'challenge/challenge_form.jade'
    fields = ["title", "content", "category"]

    def get_success_url(self):
        return self.object.get_absolute_url()


class ClaimDetail(generic.DetailView):
    template_name = 'challenge/claim_detail.jade'
    model = db.Claim


class ClaimCreate(generic.CreateView):
    """
    submit a new challenge
    """
    model = db.Claim
    template_name = 'challenge/claim_form.jade'
    form_class = form.ClaimForm

    def get_context_data(self, **kwargs):
        context = super(ClaimCreate, self).get_context_data(**kwargs)
        context['challenge'] = db.Challenge.objects.get(id=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        challenge = db.Challenge.objects.get(id=self.kwargs['pk'])
        form.instance.challenge = challenge
        form.instance.author = self.request.user
        return super(ClaimCreate, self).form_valid(form)


class ClaimUpdate(generic.UpdateView):
    """
    edit challenge
    reate a form instance with POST data.
    >>> a = Author()
    >>> f = AuthorForm(request.POST, instance=a)

    >>> new_author = f.save()
    """
    model = db.Claim
    fields = ['content', 'proof_url', 'project_url']
    template_name = 'challenge/claim_form.jade'


class ProfileUpdate(generic.View):
    """
    edit challenge
    reate a form instance with POST data.
    >>> a = Author()
    >>> f = AuthorForm(request.POST, instance=a)

    >>> new_author = f.save()
    """
    def post(self, request):
        profileForm = form.ProfileForm(request.POST, instance=request.user.challenge_user)
        if profileForm.is_valid():
            model = profileForm.save()
            return HttpResponseRedirect("/user/"+str(request.user.id))
        else:
            return render_to_response(
                'challenge/user_form.jade',
                {'form': profileForm},
                context_instance=RequestContext(request))


    def get(self, request):
        profileForm = form.ProfileForm(instance=request.user.challenge_user)
        return render_to_response(
            'challenge/user_form.jade',
            {'form': profileForm},
            context_instance=RequestContext(request))


class ClaimDelete(generic.DeleteView):
    """
    delete challenge
    """
    model = db.Claim


def vote(request):
    challenge_id = request.GET.get('challenge')
    challenge = db.Challenge.objects.get(id=challenge_id)
    user = request.user

    if request.GET.get('dir') and request.GET.get('dir') != '':
        if request.GET.get('dir') == "up":
            direction = 1
        else:
            direction = -1

        vote, created = db.Vote.objects.get_or_create(user=user, challenge=challenge, defaults={'direction': direction})

        if not created:
            vote.direction = direction
            vote.save()
    else:
        db.Vote.objects.filter(user=user, challenge=challenge).delete()

    return HttpResponse("{voted:true}", content_type="application/json")
