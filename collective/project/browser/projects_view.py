
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
import datetime

class ProjectsView(BrowserView):

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
        proj = project.getObject()
        rate = proj.rate
        title = proj.Title()
        td = datetime.timedelta
        hours, start, stop = td(0), td(0), td(0)
        total = 0.0

        if proj.flat:
            start = proj.start
            stop = proj.stop
            diff = stop - start
            months = diff.days/30
            if months is not 0:
                amort = rate / months
            else:
                amort = rate
            total = amort

        projects = proj.objectValues()
        for iter in projects:
            if self.reviewStateIsActive(iter):
                start = iter.start
                stop = iter.stop
                tasks = iter.objectValues()
                flat = iter.flat
                if not flat:
                    for task in tasks:
                        days = self.total_hours(iter,billable_only=True).days
                        if not days >= 1:
                            hours = float(self.total_hours(iter,billable_only=True).seconds)/float(3600)
                        else:
                            hours = (float(self.total_hours(iter,billable_only=True).seconds)/float(3600)) + float(days * 24)
                        try:
                            total = hours * rate
                        except:
                            total = 0
                else: 
                    total = rate

        if not proj.billable:
            total = 0.0
        
        format_float = self.format_float
        hours, rate, total = format_float(hours), format_float(rate), format_float(total)
        format_date = self.format_date
        start, stop = format_date(start), format_date(stop)
        return ([title, hours, rate, start, stop, total])

    def format_float(self,f):
        # format float
        try:
            f = '%.2f' % f
            return f
        except:
            return None

    def format_date(self,d):
        try:
            #d = d.strftime('%Y-%m-%d')
            d = d.strftime('%Y-%m')
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

    def total_hours(self,iter,billable_only=False):
        if billable_only:
            hours = datetime.timedelta(0)
            tasks = iter.objectValues()
            for task in tasks:
                if task.billable:
                    if task.stop is not None and task.start is not None:
                        hours += task.stop - task.start
            return hours
        else:
            hours = datetime.timedelta(0)
            tasks = iter.objectValues()
            for task in tasks:
                hours += task.stop - task.start
            return hours

    def getPrintable(self):
        text=''
        for p in self.getProjects('sort-on-projects'):
            for col in self.project_totals(p):
                try: 
                    text = text + col
                except:
                    text = text + ' - '
            text = text + '\n'
        return text

    def reviewStateIsActive(self,iter):
        wftool = self.context.portal_workflow
        if wftool.getInfoFor(iter, 'review_state') == 'active':
            return True
        else:
            return False

    def disable_border(self):
        return self.context.portal_properties.project_properties.disable_border
