# encoding: utf-8

from five import grok
from zope import schema
from plone.directives import form
from collective.project import projectMessageFactory as _
from collective.project import common


class IClient(form.Schema):

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


class View(common.View, grok.View):
    grok.context(IClient)
    grok.require('zope2.View')

    def getStartDate(self, project):
        return self.format_date(project.start)

    def getStopDate(self, project):
        return self.format_date(project.stop)

    def getInfo(self):
        info = []
        # XXX How do I order these fields The Right Way™?
        for field in IClient.namesAndDescriptions():
            if not (field[1].title == 'Name' or field[1].title == 'Notes'):
                info.append('<p><b>%s</b>: %s</p>' % (field[1].title, getattr(self.context, field[0])))
        info.reverse()
        info.append('<p><b>%s</b>: %s</p>' % (
            'Notes', self.context.description))
        return info
