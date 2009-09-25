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

    billable = schema.Bool(
            title=_(u"Billable?"),
            required=True,
            default=True,
        )

class View(grok.View):
    grok.context(ITask)
    grok.require('zope2.View')

    def getIterTitle(self,project):
        client_breadcrumbs = self.client_breadcrumbs(project)
        try:
            return self.context.portal_properties.project_properties.iteration + ' &rarr; ' + client_breadcrumbs
        except:
            return 'Active Projects &rarr; ' + client_breadcrumbs

    def client_breadcrumbs(self,project):
        results = []
        path = list(project.getPhysicalPath())[2:]
        for i in range(len(path)):
            results.append(self.context.restrictedTraverse('/'.join(path)).Title())
            path.pop()
        results.reverse()
        return ' &rarr; '.join(results)

    def total_hours(self):
        try:
            hours = 0.0
            tasks = self.context.aq_inner.objectValues()
            for task in tasks:
                hours += task.hours
        except:
            hours = 0.0

        return self.format_float(hours)

    def format_float(self,f):
        try:
            f = '%.2f' % f
            return f
        except:
            return None

    def getRate(self):
        return self.format_float(self.context.aq_inner.rate)

    def total_income(self):
        try:
            return self.format_float(self.calculate_billable() * self.context.aq_inner.rate)
        except:
            return self.format_float(self.calculate_billable() * 0.0)

    def calculate_billable(self):
        try:
            hours = 0.0
            tasks = self.context.aq_inner.objectValues()
            for task in tasks:
                if task.billable:
                    hours += task.hours
        except:
            hours = 0.0

        return hours

    def getOddEven(self,counter):
        if counter % 2 == 0:
            return 'even'
        else:
            return 'odd'

    def getStartDate(self):
        return self.format_date(self.context.start)

    def getStopDate(self):
        return self.format_date(self.context.stop)

    def format_date(self,d):
        try:
            d = d.strftime('%Y-%m-%d %I:%M')
            return d
        except:
            return None

    def getHours(self):
        return str(self.context.stop - self.context.start)

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
