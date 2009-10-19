from five import grok
from zope import schema
from plone.directives import form
from collective.project import projectMessageFactory as _
import datetime

class IClient(form.Schema):
    title = schema.TextLine(
            title=_(u"Title"),
            default=_(u"Client"),
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
