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

class View(grok.View):
    grok.context(IIteration)
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
        hours = datetime.timedelta(0)
        tasks = self.context.objectValues()
        for task in tasks:
            hours += task.stop - task.start
        return hours

    def total_hours_billable(self):
        hours = datetime.timedelta(0)
        tasks = self.context.objectValues()
        for task in tasks:
            if task.billable:
                hours += task.stop - task.start
        return hours

    def format_float(self,f):
        try:
            f = '%.2f' % f
            return f
        except:
            return None

    def getRate(self):
        return self.context.aq_inner.aq_parent.rate

    def total_income(self):
        days = self.total_hours_billable().days
        seconds = days * 86400
        hours = float((self.total_hours_billable().seconds + seconds)/3600)
        rate = self.getRate()
        try:
            return self.format_float(hours * rate)
        except:
            return self.format_float(hours * 0.0)

    def getOddEven(self,counter):
        if counter % 2 == 0:
            return 'even'
        else:
            return 'odd'

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
        return task.stop - task.start

@form.default_value(field=IIteration['start'])
def startDate(data):
    return datetime.datetime.today()

@form.default_value(field=IIteration['stop'])
def stopDate(data):
    # stop in one month
    return datetime.datetime.today() + datetime.timedelta(days=calendar.mdays[datetime.date.today().month])

@form.default_value(field=IIteration['title'])
def iterTitle(data):
    return datetime.datetime.today().strftime('%B %Y')
