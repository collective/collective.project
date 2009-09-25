from five import grok
from zope import schema
from plone.directives import form
from collective.project import projectMessageFactory as _
import datetime

class IProject(form.Schema):

    title = schema.TextLine(
            title=_(u"Title"),
            default=_(u"Consulting"),
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

    rate = schema.Float(
            title=_(u"Rate"),
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
    grok.context(IProject)
    grok.require('zope2.View')

    def total_hours(self,iter):
        hours = datetime.timedelta(0)
        tasks = iter.objectValues()
        for task in tasks:
            hours += task.stop - task.start
        return hours

    def total_hours_billable(self,iter):
        hours = datetime.timedelta(0)
        tasks = iter.objectValues()
        for task in tasks:
            if task.billable:
                hours += task.stop - task.start
        return hours

    def total_income(self,iter):
        days = self.total_hours_billable(iter).days
        seconds = days * 86400
        hours = float((self.total_hours_billable(iter).seconds + seconds)/3600)
        rate = self.getRate()
        try:
            return self.format_float(hours * rate)
        except:
            return self.format_float(hours * 0.0)

    def project_title(self):
        project = self.context.Title()
        return '%s' % (project)

    def client_breadcrumbs(self,project):
        results = []
        path = list(project.getPhysicalPath())[2:]
        for i in range(len(path)):
            results.append(self.context.restrictedTraverse('/'.join(path)).Title())
            path.pop()
        results.reverse()
        return ' &rarr; '.join(results)

    def format_float(self,f):
        try:
            f = '%.2f' % f
            return f
        except:
            return None

    def format_date(self,d):
        try:
            d = d.strftime('%Y-%m-%d')
            return d
        except:
            return None

    def getStartDate(self,task):
        return self.format_date(task.start)

    def getStopDate(self,task):
        return self.format_date(task.stop)

    def getHours(self,iter):
        total_hours = self.total_hours(iter)
        total_hours_billable = self.total_hours_billable(iter)
        return 'Total: %s, Billable: %s' % (total_hours, total_hours_billable)

    def getRate(self):
        return self.context.rate

    def getOddEven(self,counter):
        if counter % 2 == 0:
            return 'even'
        else:
            return 'odd'

    def getIterTitle(self,project):
        client_breadcrumbs = self.client_breadcrumbs(project)
        try:
            return self.context.portal_properties.project_properties.iteration + ' &rarr; ' + client_breadcrumbs
        except:
            return 'Active Projects &rarr; ' + client_breadcrumbs

    def reviewStateIsActive(self,iter):
        wftool = self.context.portal_workflow
        if wftool.getInfoFor(iter, 'review_state') == 'active':
            return True
        else:
            return False

@form.default_value(field=IProject['start'])
def startDate(data):
    return datetime.datetime.today()

@form.default_value(field=IProject['stop'])
def stopDate(data):
    # stop in one year
    return datetime.datetime.today() + datetime.timedelta(days=365)
