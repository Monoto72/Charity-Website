# DripDrop Charity APP

A quick reference to how to use github to its full extent. Please ensure you follow these practices, so that we can obtain the highest mark. If you have any questions in regards to this, don't be hesitant to message me :P - Sam

# Work flow

When working on a feature, **you should not** work directly in master. You should make a new branch and work on it within said area. Once your branch is complete and you are content with it, you should then open a merge request, and then merge it to master. *However, if you are not confident with merging, you should contact another team member and hhave them review the merge request.*

## Branch Conventions

When working on a **Feature** you should create a new branch with the following convetion:

* feature/branch_name

When working on a **Fix** you should create a new branch with the following convetion:

* fix/branch_name

## Creating a new branch

* **If** you're in another branch already, that's not `main` run `git checkout main`
* In your git/ bash terminal run the command `git fetch --all`
* Run `git reset --hard origin/main` to get the latest version of master
* run `git checkout -b "feature/branch_name"` to create a new branch which will take you to `feature/branch_name`
* Now you can simply work on your feature/ fix

## Rebasing to get the latest version of `main` into your branch_name

If you are at a point where you have been working on a **Feature** or **Fix** for a hot minute, and `main` has had changes since. You should rebase your branch, to ensure the new `main` works correctly with your branch.

* **If** you're in another branch already, that's not `main` run `git checkout main`
* Open a bash terminal in the code base and run `git fetch --all`
* Run `git reset --hard origin/main` to get the latest version of main
* Run `git checkout "feature/BRANCH-NAME` to go to your branch you want to rebase.
* Run `git rebase origin/main` which will incoperate all of the `main` branch to yours.
* **If** you have conflicts deal with them, thus, accepting the incoming pieces of code, then follow `i`. If you don't have any conflicts, follow `ii`.
    * i: `git rebase --continue` if no conflicts arise, follow `ii`
    * ii: `git push --force`
* Now you can simply work on your feature/ fix again, or make the merge request :P

# Django

Much like over web-frameworks, these have their own niche functions which can help us to develop the app easily. On top of that, as we've gone over already, Django provides us with a multi-use language, thus, we can use as many languages as you want, though in our case only JS and Python. I understand that this may be your first time using Django, but please if you get confused, just reach out to me and I'll assist you. (Sam)

## What you need installed

* Python 3 for the majority of Django, please install this @ [Python Download](https://www.python.org/downloads/)
* Django Google maps for the back-end, please run `pip install django-google-maps`
* To be added...

## Running Django and Small commands needed when compiling your application

### Server Commands

* To run the server, you will simply want to run `python manage.py runserver`
* If at some point you want to create a new model (*Schema*), you will need to run `python manage.py makemigration`
* If at some point you need to rework your model, you will need to run `python manage.py migrate`

## Django views

As Django loads pages using a URL handler, you will need to set-up the back-end to allow for your page to be hosted. To do this follow the next few steps.

* In the `charitymap.views` you will want to add the following function
```python
def page_name(request):
    # Data you want to be sent i.e. test = "Hello World!"
    return render(request, 'page_name.html', test)
```

* In the `DripDrop.urls` you will want to add the following to urlpatterns
```python
urlpatterns = [
    ...
    path('page_name/', include('charitymap.urls')),
]
```

* In the `charitymap.urls` you will want to add the following to urlpatterns
```python
urlpatterns = [
    ...
    path('page_name/', views.page_name, name='page_name')
]
```

### Django Variables

* Please ensure that when working on a view, you incorperate `{% load static %}`
    * This ensures you can incoperate all static files to your view, for example: `<link type="text/css" href="{% static '/css/style.css' %}">` which will include the **Tailwind CSS location**
    * If you incoperated data in your render function to be used in front end code, just add this to your HTML `{{ test | json_script:'jsfile' }}`
        * If you want data to be displayed differantly please refer to this guide @ [Data Usability](https://mkdev.me/en/posts/fundamentals-of-front-end-django)