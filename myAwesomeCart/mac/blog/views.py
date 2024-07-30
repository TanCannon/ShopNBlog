#imported manually
from django.shortcuts import render, HttpResponse, redirect
from .models import Blogpost, BlogComment
from django.contrib import messages #to use inbuilt message passing to template function
from django.contrib.auth.models import User #for using the inbuilt "making user" related functions
from django.contrib.auth import authenticate, login, logout
from blog.templatetags import extras

# Create your views here.
def index(requests):
    if (requests.user.is_authenticated):
        user_profile = requests.user
        print(user_profile.first_name, user_profile.last_name,"hello")
    else:
        print("ananomous user")
    # return HttpResponse('blog index it is')
    post = Blogpost.objects.all()
    # print(post)
    

    # messages.success(requests,'Welcome to My Awesome Cart Blog Page :)')
    return render(requests,'blog/index.html', {'post': post}) 

def search(requests):
    query = requests.GET.get('search')
    print(f'query - {query}')
    post = Blogpost.objects.filter(tilte__icontains=query) # (fieldname__icontains = query) finds the match for objects having stuff similar to query
    # print(post)
    # post = [item for item in post_temp if searchMatch(query,item)]
    # post = Blogpost.objects.all()
    post_cnt = len(post)
    if (post_cnt>0):
        messages.success(requests,f"Search results for '{query}', total {post_cnt} results were found")
    else:
        messages.warning(requests,"No results found")
    
    return render(requests,"blog/search.html",{"post":post,"query":query,"post_cnt": post_cnt})

def blogpost(requests,id):
    post = Blogpost.objects.filter(post_id = id)[0] #returns a list so using [0] to access elment
    # print(post)
    total_posts = Blogpost.objects.count()
    comments = BlogComment.objects.filter(post=post, parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict = {}
    for reply in replies:
        if reply.parent.comment_id not in replyDict.keys():
            replyDict[reply.parent.comment_id] = [reply]
        else:
            replyDict[reply.parent.comment_id].append(reply)
    # print(replyDict)

    params = {'total_posts': total_posts,'post':post, 'comments':comments, 'replyDict':replyDict}
    # print(total_posts)
    return render(requests,'blog/blogpost.html', params)    

def handelSignup(requests):
    if requests.method=="POST":
        # Get the post parameters
        username=requests.POST.get('username')
        email=requests.POST.get('email')
        fname=requests.POST.get('fname')
        lname=requests.POST.get('lname')
        pass1=requests.POST.get('pass1')
        pass2=requests.POST.get('pass2')

        # check for errorneous input
        # if len(username)<10:
        #     messages.warning(requests, " Your user name must be under 10 characters")
        #     return redirect('/blog')

        if not username.isalnum():
            messages.warning(requests, " User name should only contain letters and numbers")
            return redirect('/blog')
        if (pass1!= pass2):
            messages.warning(requests, " Passwords do not match")
            return redirect('/blog')
        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name= fname
        myuser.last_name= lname
        myuser.save()
        messages.success(requests, " Your Account has been successfully created")
        return redirect('/blog')

    else:
        return HttpResponse("404 - Not found")
    
def handelLogin(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST.get('loginusername')
        loginpassword=request.POST.get('loginpassword')

        user=authenticate(username= loginusername, password= loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("/blog")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("/blog")

    return HttpResponse("404- Not found")

#to post comments in a particular Blogpost
def postComment(requests):
    if requests.method == "POST":
        #what is the comment
        comment=requests.POST.get("comment")
        print(comment)
        #who has made the comment
        user = requests.user
        #in which post the comment has been made
        postId = requests.POST.get("postId")
        #in which comment is this comment has been made
        parentId = requests.POST.get("parentId")
        parent = BlogComment.objects.get(comment_id = parentId)
        
        post = Blogpost.objects.get(post_id= postId)
        if (parentId != ""): #i.e it a comment to another comment (a reply)
            comment = BlogComment( comment = comment, user = user, post = post, parent = parent)
            comment.save()
            messages.success(requests, "Your reply has been posted successfully")
        else:  #i.e it is a parent comment
            comment = BlogComment( comment = comment, user = user, post = post)
            comment.save()
            messages.success(requests, "Your comment has been posted successfully")

    return redirect(f"/blog/blogpost/{post.post_id}")

def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/blog')
'''making the logout button is yet to be finshed'''


