from five import grok
from zope import schema
from plone.directives import form
from collective.project import projectMessageFactory as _
import datetime

class IClient(form.Schema):
    email = schema.TextLine(
            title=_(u"Email address"),
            required=False,
        )
