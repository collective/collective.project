from zope import schema
from collective.project import projectMessageFactory as _
from collective.project import common
import datetime
from zope.schema.vocabulary import SimpleVocabulary
from Products.CMFCore.utils import getToolByName
from plone.supermodel import model


def projectTypes(context):
    terms = []
    pprop = getToolByName(context, 'portal_properties')
    for t in pprop.project_properties.project_types:
        terms.append(SimpleVocabulary.createTerm(t, str(t), t))
    return SimpleVocabulary(terms)


class IProject(model.Schema):

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

    hours = schema.Float(
            title=_(u"Hours"),
            description=_(
                u"The total number of hours available for this project."),
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


class View(common.View):

    def total_hours(self, iter, billable_only=False):
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
                if task.stop is not None and task.start is not None:
                    hours += task.stop - task.start
            return hours

    def total_income(self, iter):
        d = self.total_hours(iter, billable_only=True).days
        if not d >= 1:
            hours = float(
                self.total_hours(iter, billable_only=True).seconds)/float(3600)
        else:
            hours = (float(self.total_hours(
                                            iter, billable_only=True
                                            ).seconds)/float(3600)) + float(
                                                                            d *
                                                                            24)
        rate = self.getRate()
        if not (self.context.flat or iter.flat):
            try:
                return self.format_float(hours * rate)
            except:
                return self.format_float(hours * 0.0)
        else:
            try:
                return self.format_float(rate)
            except:
                return self.format_float(0.0)

    def project_title(self):
        project = self.context.Title()
        return '%s' % (project)

    def client_breadcrumbs(self, project):
        results = []
        path = list(project.getPhysicalPath())[2:]
        for i in range(len(path)):
            results.append(
                self.context.restrictedTraverse('/'.join(path)).Title())
            path.pop()
        results.reverse()
        return ' &rarr; '.join(results)

    def format_float(self, f):
        try:
            f = '%.2f' % f
            return f
        except:
            return None

    def format_date(self, d):
        try:
            d = d.strftime('%Y-%m-%d')
            return d
        except:
            return None

    def getStartDate(self, task):
        return self.format_date(task.start)

    def getStopDate(self, task):
        return self.format_date(task.stop)

    def getHours(self, iter):
        th = self.total_hours(iter)
        thb = self.total_hours(iter, billable_only=True)
        return 'Total: %s, Billable: %s' % (th, thb)

    def getRate(self):
        return self.context.rate

    def getOddEven(self, counter):
        if counter % 2 == 0:
            return 'even'
        else:
            return 'odd'

    def getIterTitle(self, project):
        client_breadcrumbs = self.client_breadcrumbs(project)
        try:
            portal_properties = self.context.portal_properties
            iteration = portal_properties.project_properties.iteration
            iter_title = ' &rarr; '.join([iteration, client_breadcrumbs])
            return iter_title
        except:
            return 'Active Projects &rarr; ' + client_breadcrumbs

    def reviewStateIsActive(self, iter):
        wftool = self.context.portal_workflow
        if wftool.getInfoFor(iter, 'review_state') == 'active':
            return True
        else:
            return False

    def disable_border(self):
        return self.context.portal_properties.project_properties.disable_border


def startDate(data):
    """
    Start on first day of current month
    """
    now = datetime.datetime.now()
    first_day = datetime.datetime(now.year, now.month, 1)
    return first_day


def stopDate(data):
    """
    Stop in one year-ish
    """
    now = datetime.datetime.now()
    return datetime.datetime(
        now.year + 1, now.month, 1) - datetime.timedelta(1)
