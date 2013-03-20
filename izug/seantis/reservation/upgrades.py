from Products.CMFCore.utils import getToolByName


def upgrade_to_10(context):

    css_registry = getToolByName(context, 'portal_css')

    # there are no more stylesheets in izug.seantis.reservation for now
    stylesheets = css_registry.getResourcesDict()
    ids = [i for i in stylesheets if 'izug.seantis.reservation' in i]

    map(css_registry.unregisterResource, ids)

    # reapply the izug.seantis.reservation profile
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile(
        'profile-izug.seantis.reservation:default'
    )
