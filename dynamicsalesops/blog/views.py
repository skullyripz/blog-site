from django.shortcuts import render
from forms import CommentForm

# Create your views here.

def view_post(request, slug):
    post = get_object_or_404(BlogPage, slug=slug)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return redirect(request.path)
    return render_to_response('/blog/blog_page.html',
                              {
                                  'post': post,
                                  'form': form,
                              },
                              context_instance=RequestContext(request))
