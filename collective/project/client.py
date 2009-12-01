from five import grok
from zope import schema
from plone.directives import form
from collective.project import projectMessageFactory as _
import datetime
import calendar
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
from Products.CMFCore.utils import getToolByName

class IClient(form.Schema):

    name = schema.Text(
            title=_(u"Name"),
            description=_(u"First Last."),
            required=True,
        )

    summary = schema.Text(
            title=_(u"Summary"),
            description=_(u"A short summary of the content."),
            required=False,
        )

    email = schema.TextLine(
            title=_(u"Email address"),
            required=False,
        )

class View(grok.View):
    grok.context(IClient)
    grok.require('zope2.View')

    def disable_border(self):
        return self.context.portal_properties.project_properties.disable_border
