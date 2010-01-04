from five import grok
from zope import schema
from plone.directives import form
from collective.project import projectMessageFactory as _
import datetime
import calendar

class IIteration(form.Schema):
    title = schema.TextLine(
            title=_(u"Title"),
        )

    summary = schema.Text(
            title=_(u"Summary"),
            description=_(u"A short summary of the content."),
            required=False,
        )

    start = schema.Datetime(
            title=_(u"Start date"),
            required=False,
        )

    stop = schema.Datetime(
            title=_(u"End date"),
            required=False,
        )

    flat = schema.Bool(
            title=_(u"Flat"),
            required=False,
            default=False,
        )

    billable = schema.Bool(
            title=_(u"Billable"),
            required=False,
            default=True,
        )

class View(grok.View):
    grok.context(IIteration)
    grok.require('zope2.View')

    def getIterTitle(self,project):
        client_breadcrumbs = self.client_breadcrumbs(project)
        try:
            return self.context.portal_properties.project_properties.iteration + ' &rarr; ' + client_breadcrumbs
        except:
            return 'Active Projects &rarr; ' + client_breadcrumbs

    def getIterTitlePlain(self,project):
        client_breadcrumbs = self.client_breadcrumbs(project)
        try:
            return self.context.portal_properties.project_properties.iteration + ' -> ' + client_breadcrumbs
        except:
            return 'Active Projects -> ' + client_breadcrumbs

    def client_breadcrumbs(self,project):
        results = []
        path = list(project.getPhysicalPath())[2:]
        for i in range(len(path)):
            results.append(self.context.restrictedTraverse('/'.join(path)).Title())
            path.pop()
        results.reverse()
        return ' &rarr; '.join(results)

    def total_hours(self,billable_only=False):
        if billable_only:
            hours = datetime.timedelta(0)
            tasks = self.context.objectValues()
            for task in tasks:
                # Only add up billable hours
                if task.billable:
                    if task.stop is not None and task.start is not None:
                        hours += task.stop - task.start
            return hours
        else:
            hours = datetime.timedelta(0)
            tasks = self.context.objectValues()
            for task in tasks:
                # Add up everything
                if task.stop is not None and task.start is not None:
                    hours += task.stop - task.start
            return hours

    def total_income(self):
        days = self.total_hours(billable_only=True).days
        if not days >= 1:
            hours = float(self.total_hours(billable_only=True).seconds)/float(3600)
        else:
            hours = (float(self.total_hours(billable_only=True).seconds)/float(3600)) + float(days * 24)
        rate = self.getRate()
        if not self.context.flat:
            try:
                return self.format_float(hours * rate)
            except:
                return self.format_float(hours * 0.0)
        else:
            try:
                return self.format_float(rate)
            except:
                return self.format_float(0.0)

    def format_float(self,f):
        try:
            f = '%.2f' % f
            return f
        except:
            return None

    def getRate(self):
        return self.context.aq_inner.aq_parent.rate

    def getOddEven(self,counter):
        if counter % 2 == 0:
            return 'even'
        else:
            return 'odd'

    def getSummary(self,task):
        return task.summary

    def getStartDate(self,task):
        return self.format_date(task.start)

    def getStopDate(self,task):
        return self.format_date(task.stop)

    def format_date(self,d):
        try:
            d = d.strftime('%Y-%m-%d %I:%M')
            return d
        except:
            return None

    def getHours(self,task):
        if task.stop is not None and task.start is not None:
            return task.stop - task.start
        else:
            return None

    def disable_border(self):
        return self.context.portal_properties.project_properties.disable_border

@form.default_value(field=IIteration['start'])
def startDate(data):
    # start on first day of current month
    now = datetime.datetime.now()
    first_day = datetime.datetime(now.year, now.month, 1)
    return first_day

@form.default_value(field=IIteration['stop'])
def stopDate(data):
    # stop in one month
    now = datetime.datetime.now()
    last_day = calendar.monthrange(now.year, now.month)[1]
    return datetime.datetime(now.year, now.month, last_day)

@form.default_value(field=IIteration['title'])
def iterTitle(data):
    return datetime.datetime.today().strftime('%B %Y')
