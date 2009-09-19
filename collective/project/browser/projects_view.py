
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class ProjectsView(BrowserView):

    #__call__ = ViewPageTemplateFile('projects_view.pt')

    # Based on http://code.activestate.com/recipes/52306/
    def sortedDictValues3(self,adict):
        keys = adict.keys()
        keys.sort()
        return map(adict.get, keys)

    def getProjects(self,sort):
        results = {}
        projects = self.context.portal_catalog(review_state='active',
            path='/'.join(self.context.getPhysicalPath()),
            portal_type='project')
        for p in projects:
            if sort == 'sort-on-clients':
                results[self.breadcrumbs(p,'sort-on-clients','with-id')] = p
            else:
                results[self.breadcrumbs(p,'sort-on-projects','with-id')] = p
        return self.sortedDictValues3(results)

    def project_totals(self,project):
        obj = project.getObject()
        name,hours,rate,start,stop,tasks = (obj.Title(), 0.0, obj.rate, obj.start, 
            obj.stop, obj.objectValues())
        for task in tasks:
            if task.hours is not None:
                hours += task.hours
        if not obj.flat and rate is not None:
            name,hours,rate,start,stop,total = name,hours,rate,start,stop,hours * rate
        else:
            # amortize
            if start is not None and stop is not None and rate is not None:
                diff=stop-start
                months = diff.days/30
                amort = rate/months
                name,hours,rate,start,stop,total = name,hours,rate,start,stop,amort
            else:
                name,hours,rate,start,stop,total = name,hours,rate,start,stop,rate

        if not obj.billable:
            total = 0.0
            name,hours,rate,start,stop,total = name,hours,rate,start,stop,total

        total,hours,rate=(self.format_float(total),
                          self.format_float(hours),
                          self.format_float(rate))
        start,stop=self.format_date(start),self.format_date(stop)  

        return ([name,hours,rate,start,stop,total])

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

    def project_url(self,project):
        return project.getObject().absolute_url()

    def project_edit(self,project):
        return project.getObject().absolute_url() + '/edit'

    def breadcrumbs(self,project,sort,type):
        results = []
        path = list(project.getObject().getPhysicalPath())[2:]
        for i in range(len(path)):
            if type == 'with-id':
                results.append(self.context.restrictedTraverse('/'.join(path)).getId())
            else:
                results.append(self.context.restrictedTraverse('/'.join(path)).Title())
            path.pop()
        if sort == 'sort-on-clients':
            results.reverse()
        return ' &rarr; '.join(results)

    def projects_total(self,projects):
        total = 0.0
        for project in projects:
            if self.project_totals(project)[5] is not None:
                total += float(self.project_totals(project)[5])
        total='%.2f' % total
        return total

    def getOddEven(self,counter):
        if counter % 2 == 0:
            return 'even'
        else:
            return 'odd'

    def getIterTitle(self):
        try:
            return self.context.portal_properties.project_properties.iteration
        except:
            return 'Active Projects'
