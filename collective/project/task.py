from five import grok
from zope import schema
from plone.directives import form, dexterity
from collective.project import projectMessageFactory as _
import datetime
from BTrees.Length import Length

class ITask(form.Schema):
    form.mode(id='hidden')
    id = schema.TextLine(
            title=_(u"Id"),
        )

    title = schema.TextLine(
            title=_(u"Title"),
        )

    summary = schema.Text(
            title=_(u"Summary"),
            description=_(u"A short summary of the content."),
            required=False,
        )

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

@form.default_value(field=ITask['id'])
def getNextCounter(self): # Some (slightly modified) Joel Burton Fu, from SimpleCollector.
        """Get next ID. Lazily creates counter if neccessary.
        """
        self = self.context
        if not hasattr(self, '_counter'):
            self._counter = Length(0)
        self._counter.change(+1)
        return self._counter()
