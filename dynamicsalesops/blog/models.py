from __future__ import unicode_literals
import uuid

from django.db import models
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.template import RequestContext

from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailforms.edit_handlers import FormSubmissionsPanel
from wagtail.wagtailsearch import index
from wagtail.wagtailforms.models import AbstractFormField, AbstractForm

from django import forms
from django.forms import ModelForm

# Create your models here.


class BlogIndexPage(Page):
	intro = RichTextField(blank=True)
	
	def get_context(self, request):
		context = super(BlogIndexPage, self).get_context(request)
		blogpages = self.get_children().live().order_by('-first_published_at')
		context['blogpages'] = blogpages
		return context
	
	content_panels = Page.content_panels + [
		FieldPanel('intro', classname="full")
	]

class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('BlogPage', related_name='tagged_items')


class BlogPage(Page):
	date = models.DateField("Post date")
	intro = models.CharField(max_length=250)
	body = RichTextField(blank=True)
	#tag manager
	tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    
    #get feature image
	def main_image(self):
		gallery_item = self.gallery_images.first()
		if gallery_item:
			return gallery_item.image
		else:
			return None
	
	
	def serve(self, request):
		from .forms import CommentForm
		
		if request.method == 'POST':
			form = CommentForm(request.POST)
			
			if form.is_valid():
				comment = form.save(commit=False)
				comment.page_id = self.id
				comment.save()
				return redirect(self.url)
		else:
			form = CommentForm()
		
		return render(request, self.template, {
			'page': self,
			'form': form,
		})
	
	search_fields = Page.search_fields + [
		index.SearchField('intro'),
		index.SearchField('body'),
	]
	
	content_panels = Page.content_panels + [
		MultiFieldPanel([
			FieldPanel('date'),
			FieldPanel('tags'),
		], heading="Blog information"),
		FieldPanel('intro'),
		FieldPanel('body'),
		InlinePanel('gallery_images', label="Gallery images"),
	]

	
class BlogPageComment(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	page = models.ForeignKey('BlogPage', related_name='comments')
	comment_author = models.CharField(max_length=50)
	text = models.TextField()
	created_date = models.DateTimeField(default=timezone.now)
	approved_comment = models.BooleanField(default=False)
	

class BlogPageGallaryImage(Orderable):
	page = ParentalKey(BlogPage, related_name="gallery_images")
	image = models.ForeignKey(
		'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
	)
	caption = models.CharField(blank=True, max_length=250)
	
	panels = [
		ImageChooserPanel('image'),
		FieldPanel('caption'),
	]

class BlogTagIndexPage(Page):

    def get_context(self, request):

        # Filter by tag
        tag = request.GET.get('tag')
        blogpages = BlogPage.objects.filter(tags__name=tag)

        # Update template context
        context = super(BlogTagIndexPage, self).get_context(request)
        context['blogpages'] = blogpages
        return context
