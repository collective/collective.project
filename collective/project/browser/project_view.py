
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime

class ProjectView(BrowserView):

    __call__ = ViewPageTemplateFile('project_view.pt')

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
        return self.format_date(task.date)

    def getStopDate(self,task):
        return self.format_date(task.stop)

    def getHours(self,task):
        return self.format_float(task.hours)

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
