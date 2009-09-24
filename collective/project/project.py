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

    def total_hours(self):
        try:
            hours = 0.0
            tasks = self.context.aq_inner.objectValues()
            for task in tasks:
                hours += task.hours
        except:
            hours = 0.0

        return self.format_float(hours)

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

    def total_billable(self):
        return self.format_float(self.calculate_billable())

    def total_income(self):
        try:
            return self.format_float(self.calculate_billable() * self.context.aq_inner.rate)
        except:
            return self.format_float(self.calculate_billable() * 0.0)

    def project_title(self):
        project = self.context.aq_inner.Title()
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

    def getHours(self,task):
#        return self.format_float(task.hours)
        return 'Calculate me.'

    def getRate(self):
        return self.format_float(self.context.aq_inner.rate)

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

@form.default_value(field=IProject['start'])
def startDate(data):
    return datetime.datetime.today()

@form.default_value(field=IProject['stop'])
def stopDate(data):
    return datetime.datetime.today() + datetime.timedelta(365)
