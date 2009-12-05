from five import grok
from zope import schema
from plone.directives import form
from collective.project import projectMessageFactory as _
import datetime
import calendar
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
from Products.CMFCore.utils import getToolByName
from collective.project import base

class IClient(form.Schema):

    title = schema.TextLine(
            title=_(u"Name"),
            required=True,
        )

    email = schema.TextLine(
            title=_(u"Email"),
            required=False,
        ) 

    address = schema.TextLine(
            title=_(u"Address"),
            required=False,
        ) 

    website = schema.TextLine(
            title=_(u"Website"),
            required=False,
        ) 

    description = schema.Text(
            title=_(u"Notes"),
            required=False,
        )

class View(base.View, grok.View):
    grok.context(grok.View)
    grok.require('zope2.View')
