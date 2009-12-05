from five import grok
from plone.directives import form

class IBase(form.Schema):
    pass

class View(grok.view):
    grok.context(grok.View)
    grok.require('zope2.View')

    def disable_border(self):
        return self.context.portal_properties.project_properties.disable_border

    def reviewStateIsActive(self,iter):
        wftool = self.context.portal_workflow
        if wftool.getInfoFor(iter, 'review_state') == 'active':
            return True
        else:
            return False

    def getOddEven(self,counter):
        if counter % 2 == 0:
            return 'even'
        else:
            return 'odd'
