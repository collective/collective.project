from zope import interface, schema
from z3c.form import form, field, button
from plone.app.z3cform.layout import wrap_form
from collective.project import projectMessageFactory as _
from zope.app.component.hooks import getSite
from zope.schema import vocabulary
from zope.interface import directlyProvides
from zope.schema.interfaces import IVocabularyFactory

projectsField = schema.Choice(
    title=u'Projects',
    description=u'Projects field.',
    vocabulary='projects_vocab'
)

class ConfigureIterationSchema(interface.Interface):
    iteration = schema.TextLine(title=_(u"Iteration id"), description=_(u"E.g. 'May 2009'"))
    projects = schema.Set(
        title=u'Projects',
        description=u"Select projects or not, I really don't care at this point",
        value_type=projectsField,
        )

class ConfigureIterationForm(form.Form):
    fields = field.Fields(ConfigureIterationSchema)
    ignoreContext = True # don't use context to get widget data
    label = _(u"Create an iteration for the projects selected below")
    def configure_iteration(self, action, data):
        if data['iteration']:
            iteration = data['iteration']
            iteration_norm = iteration.lower().replace(' ','-')
        clients = find_projects()
        for client in clients:
            c = client.getObject()
            if c.getId() in data['projects']:
                try:
                    c.invokeFactory('Iteration',iteration_norm)
                except:
                    print "Cannot create iteration %s for client %s." % (iteration, c)
                try:
                    new_iteration = c[iteration_norm]
                    new_iteration.setTitle(iteration)
                    new_iteration.reindexObject()
                except:
                    print "Cannot create iteration %s." % (iteration)

    @button.buttonAndHandler(u'Submit')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = form.EditForm.formErrorsMessage
        else:
            self.configure_iteration(action, data)

def projectsVocab(context):
    projects = {}
    for p in find_projects():
        obj = p.getObject()
        projects[obj.getId()] = obj.getId()
    items = projects.items()
    return vocabulary.SimpleVocabulary.fromItems(items)

def find_projects():
    site = getSite()
    return site.portal_catalog(portal_type='project')

directlyProvides(projectsVocab, IVocabularyFactory)
ConfigureIteration = wrap_form(ConfigureIterationForm)
