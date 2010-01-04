from five import grok
from zope import schema
from plone.directives import form
from collective.project import projectMessageFactory as _
import datetime
from BTrees.Length import Length
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget

class ITask(form.Schema):
    form.mode(id='hidden')
    form.widget(summary=WysiwygFieldWidget)

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

    def getIterTitle(self, project):
        client_breadcrumbs = self.client_breadcrumbs(project)
        try:
            iter = self.context.portal_properties.project_properties.iteration
            return iter + ' &rarr; ' + client_breadcrumbs
        except:
            return 'Active Projects &rarr; ' + client_breadcrumbs

    def client_breadcrumbs(self, project):
        results = []
        path = list(project.getPhysicalPath())[2:]
        for i in range(len(path)):
            title = self.context.restrictedTraverse('/'.join(path)).Title()
            results.append(title)
            path.pop()
        results.reverse()
        return ' &rarr; '.join(results)

    def total_hours(self):
        task = self.context
        hours = datetime.timedelta(0)
        hours = task.stop - task.start
        return hours

    def format_float(self, f):
        try:
            f = '%.2f' % f
            return f
        except:
            return None

    def getRate(self):
        task = self.context
        iteration = task.aq_inner.aq_parent
        project = iteration.aq_inner.aq_parent
        return project.rate

    def total_hours(self,billable_only=False):
        if billable_only:
            task = self.context
            hours = datetime.timedelta(0)
            if task.billable:
                if task.stop is not None and task.start is not None:
                    hours += task.stop - task.start
            return hours
        else:
            task = self.context
            hours = datetime.timedelta(0)
            if task.stop is not None and task.start is not None:
                hours = task.stop - task.start
            return hours

    def total_income(self):
        hours = float(self.total_hours(billable_only=True).seconds)/float(3600)
        rate = self.getRate()
        try:
            return self.format_float(hours * rate)
        except:
            return self.format_float(hours * 0.0)

    def getOddEven(self, counter):
        if counter % 2 == 0:
            return 'even'
        else:
            return 'odd'

    def getStartDate(self):
        return self.format_date(self.context.start)

    def getStopDate(self):
        return self.format_date(self.context.stop)

    def format_date(self, d):
        try:
            d = d.strftime('%Y-%m-%d %I:%M')
            return d
        except:
            return None

    def getHours(self):
        try:
            return str(self.context.stop - self.context.start)
        except:
            return None

    def disable_border(self):
        return self.context.portal_properties.project_properties.disable_border

@form.default_value(field=ITask['start'])
def startDate(data):
    return datetime.datetime.today()


@form.default_value(field=ITask['stop'])
def stopDate(data):
    # stop in one hour
    return datetime.datetime.today() + datetime.timedelta(hours=1)


@form.default_value(field=ITask['id'])
def getNextCounter(self): # Some (slightly modified) Joel Burton Fu,
    # from SimpleCollector.
        """Get next ID. Lazily creates counter if neccessary.
        """
        self = self.context
        if not hasattr(self, '_counter'):
            self._counter = Length(0)
        self._counter.change(+1)
        return self._counter()
