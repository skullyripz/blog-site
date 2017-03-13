from __future__ import absolute_import, unicode_literals

from django.db import models
from django import forms

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, FieldRowPanel, InlinePanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailforms.models import AbstractEmailForm, AbstractFormField
from modelcluster.fields import ParentalKey


class HomePage(Page):
	logo_image = models.ForeignKey(
		'wagtailimages.Image',
		null = True,
		blank = True,
		on_delete=models.SET_NULL,
		related_name='+')
	logo_alt_text = models.CharField(max_length=250,blank=True)
	hero_main_text = models.CharField(max_length=250)
	hero_sub_text = models.CharField(max_length=250)
	body = RichTextField(blank=True)
	
	content_panels = Page.content_panels + [
		MultiFieldPanel([
			ImageChooserPanel('logo_image'),
			FieldPanel('logo_alt_text'),
		], heading="Site Logo:"),
		MultiFieldPanel([
			FieldPanel('hero_main_text'),
			FieldPanel('hero_sub_text'),
		], heading='Hero Information:'),
		FieldPanel('body', classname="full"),
	]

class AboutPage(Page):
	hero_main_text = models.CharField(max_length=250)
	hero_sub_text = models.CharField(max_length=250)
	body = RichTextField(blank=True)
	
	content_panels = Page.content_panels + [
		MultiFieldPanel([
			FieldPanel('hero_main_text'),
			FieldPanel('hero_sub_text'),
		], heading="Hero information:"),
		FieldPanel('body', classname="full"),
	]

class FormField(AbstractFormField):
	page = ParentalKey('FormPage', related_name='form_fields')

class FormPage(AbstractEmailForm):
	intro = RichTextField(blank=True)
	thank_you_text = RichTextField(blank=True)
	
	content_panels = AbstractEmailForm.content_panels + [
		FieldPanel('intro', classname='full'),
		InlinePanel('form_fields', label='Form fields'),
		FieldPanel('thank_you_text', classname='full'),
		MultiFieldPanel([
			FieldRowPanel([
				FieldPanel('from_address', classname='col6'),
				FieldPanel('to_address', classname='col6'),
			]),
			FieldPanel('subject'),
		], "Email"),
	]
