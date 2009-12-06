
class View(object):

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

    def format_date(self,d):
        try:
            d = d.strftime('%Y-%m-%d')
            return d
        except:
            return None
