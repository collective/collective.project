"""This interface is used by the example.schemapage type. The interface
below is "real", and you can register views and adapters for it. It
will be populated with schema fields read from page.xml in this 
directory when the package is grokked.

It is possible to amend/customise the interface with new fields in addition
to those found in the model file, although without a class we normally can't
promise new methods.

We also register a custom view, called @@view. The template for this is found
in page_templates/view.pt, because this module is called "page.py" and the
view class is called "View". We specify that it is a view for any IPage
(grok.context) and requires the View permission (grok.require).
"""

from five import grok
from zope import schema
from plone.directives import form
from collective.project import projectMessageFactory as _
import datetime

class IProject(form.Schema):
#    form.model("models/project.xml")
    
    # It is possible to add additional fields and methods can be added here
    # if necessary. However, without a custom class, we usually can't
    # promise new methods.

    start = schema.Datetime(
            title=_(u"Start date"),
            required=False,
        )

    stop = schema.Datetime(
            title=_(u"End date"),
            required=False,
        )

class View(grok.View):
    grok.context(IProject)
    grok.require('zope2.View')


@form.default_value(field=IProject['start'])
def startDefaultValue(data):
    return datetime.datetime.today() + datetime.timedelta(7)


@form.default_value(field=IProject['stop'])
def stopDefaultValue(data):
    return datetime.datetime.today() + datetime.timedelta(10)

