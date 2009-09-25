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

    def getStartDate(self,task):
        return self.format_date(task.start)

    def getStopDate(self,task):
        return self.format_date(task.stop)

    def format_date(self,d):
        try:
            d = d.strftime('%Y-%m-%d')
            return d
        except:
            return None

    def getHours(self,task):
#        return self.format_float(task.hours)
        return self.calculate_billable()

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
