from zope import schema
from collective.project import projectMessageFactory as _
from collective.project import common
from plone.dexterity.browser import edit
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.supermodel import model


class IClient(model.Schema):

    title = schema.TextLine(
            title=_(u"Name"),
            required=True,
        )

    email = schema.TextLine(
            title=_(u"E-mail"),
            required=False,
        )

    website = schema.TextLine(
            title=_(u"Website"),
            required=False,
        )

    address = schema.Text(
            title=_(u"Address"),
            required=False,
        )

    description = schema.Text(
            title=_(u"Notes"),
            required=False,
        )


class View(common.View):

    def getStartDate(self, project):
        return self.format_date(project.start)

    def getStopDate(self, project):
        return self.format_date(project.stop)

    def getInfo(self):
        info = []
        # Order fields
        for field in IClient.namesAndDescriptions():
            if not (field[1].title == 'Name' or field[1].title == 'Notes'):
                info.append('<p><b>%s</b>: %s</p>' % (
                    field[1].title, getattr(self.context, field[0])))
        info.reverse()
        info.append('<p><b>%s</b>: %s</p>' % (
            'Notes', self.context.description))
        return info


class EditForm(edit.DefaultEditForm):
    template = ViewPageTemplateFile('client_templates/edit.pt')
