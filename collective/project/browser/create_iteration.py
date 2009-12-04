from zope import interface, schema
from z3c.form import form, field, button
from plone.app.z3cform.layout import wrap_form
from collective.project import projectMessageFactory as _
from zope.app.component.hooks import getSite
from zope.schema import vocabulary
from zope.interface import directlyProvides
from zope.schema.interfaces import IVocabularyFactory

import datetime
import calendar

projectsField = schema.Choice(
    title=u'Projects',
    description=u'Projects field.',
    vocabulary='projects_vocab')


def breadcrumbs(context, project):
    results = []
    path = list(project.getObject().getPhysicalPath())[2:]
    for i in range(len(path)):
        results.append(context.restrictedTraverse('/'.join(path)).Title())
        path.pop()
    return ' > '.join(results)


class CreateIterationSchema(interface.Interface):

    iteration = schema.TextLine(
        title=_(u"Iteration"),
        default=_(unicode(datetime.datetime.today().strftime('%B %Y'))))

    projects = schema.Set(
        title=u'Project(s)',
        value_type=projectsField,
        )


class CreateIterationForm(form.Form):
    fields = field.Fields(CreateIterationSchema)
    ignoreContext = True # don't use context to get widget data
    label = _(u"Iteration tool")
    description = _(u"Create iteration for selected projects")

    def deactivate_iteration(self, action, data):
        wftool = self.context.portal_workflow
        iterations = find_iterations()
        for iteration in iterations:
            if data['iteration']:
                data_iter = data['iteration']
                new_iter = data_iter.lower().replace(' ', '-')
            iter = iteration.getObject()
            if not unicode(iter.id) == new_iter: # Don't deactive the current iter
                if wftool.getInfoFor(iter, 'review_state') == 'active':
                    wftool.doActionFor(iter,'deactivate')

    def create_iteration(self, action, data):
        if data['iteration']:
            data_iter = data['iteration']
            new_iter = data_iter.lower().replace(' ', '-')
        projects = find_projects()
        for project in projects:
            proj = project.getObject()
            if proj in data['projects']:
                try:
                    proj.invokeFactory('iteration', new_iter)
                except:
                    print "Cannot create iteration %s for project %s." % (new_iter, proj.absolute_url())
                try:
                    iter_new = proj[new_iter]
                    iter_new.setTitle(data_iter)
                    iter_new.start = startDate()
                    iter_new.stop = stopDate()
                    iter_new.reindexObject()
                except:
                    print "Cannot create iteration %s for project %s." % (new_iter, proj.absolute_url())

    @button.buttonAndHandler(u'Create')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = form.EditForm.formErrorsMessage
        else:
            self.create_iteration(action, data)
            self.deactivate_iteration(action, data)

def projectsDict(context):
    projects = {}
    for p in find_projects():
        obj = p.getObject()
        bc = breadcrumbs(context,p)
        projects[bc] = obj
    return projects

def projectsVocab(context):
    projects = projectsDict(context)
    items = sorted(projects.items())
    return vocabulary.SimpleVocabulary.fromItems(items)

def find_iterations():
    site = getSite()
    return site.portal_catalog(portal_type='iteration')

def find_projects():
    site = getSite()
    return site.portal_catalog(portal_type='project')

def startDate():
    # start on first day of current month
    now = datetime.datetime.now()
    first_day = datetime.datetime(now.year, now.month, 1)
    return first_day

def stopDate():
    # stop in one month
    now = datetime.datetime.now()
    last_day = calendar.monthrange(now.year, now.month)[1]
    return datetime.datetime(now.year, now.month, last_day)

directlyProvides(projectsVocab, IVocabularyFactory)
CreateIteration = wrap_form(CreateIterationForm)
