from five import grok
from zope import schema
from plone.directives import form
from collective.project import projectMessageFactory as _
import datetime

class ITask(form.Schema):
    start = schema.Datetime(
            title=_(u"Start time"),
            required=False,
        )

    stop = schema.Datetime(
            title=_(u"Stop time"),
            required=False,
        )

@form.default_value(field=ITask['start'])
def startDate(data):
    return datetime.datetime.today()

@form.default_value(field=ITask['stop'])
def stopDate(data):
    # stop in one hour
    return datetime.datetime.today() + datetime.timedelta(hours=1)
