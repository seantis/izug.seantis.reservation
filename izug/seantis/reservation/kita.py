from StringIO import StringIO

from five import grok

from zope.schema import Int, TextLine
from zope.interface import Interface, alsoProvides

from plone.directives import form
from plone.autoform.interfaces import IFormFieldProvider

from collective.dexteritytextindexer import searchable

from seantis.dir.base.interfaces import IExportProvider
from seantis.dir.base.schemafields import Email, AutoProtocolURI
from seantis.dir.base.xlsexport import xls_response, export_xls
from seantis.dir.base.fieldmap import FieldMap, add_category_binds
from seantis.dir.base.utils import get_current_language
from seantis.dir.facility.item import (
    ItemDetailViewletManager,
    IFacilityDirectory
)
from izug.seantis.reservation import _


class IKitaSpecific(Interface):
    """Marker interface for the kita profile."""


class IKitaZugFields(Interface):

    searchable('affix')
    affix = TextLine(
        title=_(u'Name Affix'),
        required=False
    )

    spots = Int(
        title=_(u'Number of Daycare Spots'),
        required=False
    )

    searchable('address')
    address = TextLine(
        title=_(u'Address'),
        required=False
    )

    searchable('zipcode')
    zipcode = TextLine(
        title=_(u'Zipcode'),
        required=False
    )

    searchable('location')
    location = TextLine(
        title=_(u'Town'),
        required=False
    )

    searchable('phone')
    phone = TextLine(
        title=_(u'Phone'),
        required=False
    )

    searchable('email')
    email = Email(
        title=_(u'Email'),
        required=False
    )

    searchable('url')
    url = AutoProtocolURI(
        title=_(u'Homepage'),
        required=False
    )

    searchable('fax')
    fax = TextLine(
        title=_(u'Fax'),
        required=False
    )

    searchable('age')
    age = TextLine(
        title=_(u'Age'),
        required=False
    )

    searchable('holidays')
    holidays = TextLine(
        title=_(u'Holidays'),
        required=False
    )

    searchable('contact_first_name')
    contact_first_name = TextLine(
        title=_(u'Contact First Name'),
        required=False
    )

    searchable('contact_last_name')
    contact_last_name = TextLine(
        title=_(u'Contact Last Name'),
        required=False
    )

    searchable('contact_phone')
    contact_phone = TextLine(
        title=_(u'Contact Phone'),
        required=False
    )

    searchable('contact_email')
    contact_email = TextLine(
        title=_(u'Contact Email'),
        required=False
    )

    searchable('correspondence_first_name'),
    correspondence_first_name = TextLine(
        title=_(u'Correspondence First Name'),
        required=False
    )

    searchable('correspondence_first_name'),
    correspondence_last_name = TextLine(
        title=_(u'Correspondence First Name'),
        required=False
    )

    searchable('correspondence_last_name'),
    correspondence_last_name = TextLine(
        title=_(u'Correspondence Last Name'),
        required=False
    )

    searchable('correspondence_address'),
    correspondence_address = TextLine(
        title=_(u'Correspondence Address'),
        required=False
    )

    searchable('correspondence_zipcode')
    correspondence_zipcode = TextLine(
        title=_(u'Correspondence Zipcode'),
        required=False
    )

    searchable('correspondence_town')
    correspondence_town = TextLine(
        title=_(u'Correspondence town'),
        required=False
    )

    form.fieldset(
        'facility_fields',
        label=_(u'Facility Information'),
        fields=['image', 'age', 'spots', 'holidays']
    )

    form.fieldset(
        'contact_fields',
        label=_(u'Contact'),
        fields=[
            'contact_first_name',
            'contact_last_name',
            'contact_phone',
            'contact_email'
        ]
    )

    form.fieldset(
        'correspondence_fields',
        label=_(u'Correspondence'),
        fields=[
            'correspondence_first_name',
            'correspondence_last_name',
            'correspondence_address',
            'correspondence_zipcode',
            'correspondence_town'
        ]
    )

alsoProvides(IKitaZugFields, IFormFieldProvider)


class Viewlet(grok.Viewlet):
    grok.baseclass()

    data = None

    def update(self):
        if not self.data:
            self.data = self.get_data()

    def fetch_values(self, keys):
        parent = self.context.aq_inner.aq_parent
        context = self.context

        values = {}
        for key in keys:
            if hasattr(context, key) and getattr(context, key):
                values[key] = getattr(context, key)
            elif hasattr(parent, key) and getattr(parent, key):
                values[key] = getattr(parent, key)
            else:
                values[key] = None

        return values

    def available(self):
        return any(self.data.values())


class KitaInfoViewlet(Viewlet):
    grok.context(Interface)
    grok.name('seantis.dir.kitazug.detail.info')
    grok.require('zope2.View')
    grok.viewletmanager(ItemDetailViewletManager)
    grok.layer(IKitaSpecific)

    grok.order(100)

    template = grok.PageTemplateFile('templates/info.pt')

    def get_data(self):
        return self.fetch_values(['age', 'spots', 'holidays'])


class KitaAddressViewlet(Viewlet):
    grok.context(Interface)
    grok.name('seantis.dir.kitazug.detail.address')
    grok.require('zope2.View')
    grok.viewletmanager(ItemDetailViewletManager)
    grok.layer(IKitaSpecific)

    grok.order(101)

    template = grok.PageTemplateFile('templates/address.pt')

    def get_data(self):
        return self.fetch_values([
            'address',
            'zipcode',
            'location',
            'phone',
            'fax',
            'email',
            'url'
        ])


class KitaContactViewlet(Viewlet):
    grok.context(Interface)
    grok.name('seantis.dir.kitazug.detail.contact')
    grok.require('zope2.View')
    grok.viewletmanager(ItemDetailViewletManager)
    grok.layer(IKitaSpecific)

    grok.order(102)

    template = grok.PageTemplateFile('templates/contact.pt')

    def get_data(self):
        return self.fetch_values([
            'contact_first_name',
            'contact_last_name',
            'contact_phone',
            'contact_email'
        ])


class KitaZugExport(grok.Subscription):

    grok.context(IFacilityDirectory)
    grok.provides(IExportProvider)

    layer = IKitaSpecific

    id = 'kita-zug'
    title = _(u'Kita Zug Export')

    description = _(
        u'Custom export of the daycare centers in the canton of Zug'
    )

    url = None

    def export(self, request):

        fields = [
            ('title', _(u'Name')),
            ('affix', _(u'Name affix')),
            ('notes', _(u'Description')),
            ('spots', _(u'Total number of places')),
            ('address', _(u'Address')),
            ('zipcode', _(u'Zipcode')),
            ('location', _(u'Location')),
            ('phone', _(u'Phone')),
            ('email', _(u'Email')),
            ('url', _(u'Homepage')),
            ('fax', _(u'Fax')),
            ('cat1', _(u'Type')),
            ('cat2', _(u'Location (Daycare Center)')),
            ('age', _(u'Age')),
            ('cat4', _(u'Language')),
            ('cat3', _(u'Subsidized')),
            ('holidays', _(u'Holidays')),
            ('opening_hours', _(u'Opening Hours')),
            ('contact_first_name', _(u'Contact first name')),
            ('contact_last_name', _(u'Contact last name')),
            ('contact_phone', _(u'Contact phone')),
            ('contact_email', _(u'Contact email')),
            ('correspondence_first_name', _(u'Correspondence first name')),
            ('correspondence_last_name', _(u'Correspondence last name')),
            ('correspondence_address', _(u'Correspondence address')),
            ('correspondence_zipcode', _(u'Correspondence zipcode')),
            ('correspondence_town', _(u'Correspondence town')),
            ('latitude', _(u'Latitude')),
            ('longitude', _(u'Longitude'))
        ]

        fieldmap = FieldMap()
        fieldmap.root = True
        fieldmap.keyfields = ('title',)
        fieldmap.typename = 'seantis.dir.facility.item'
        fieldmap.add_fields(f[0] for f in fields)

        for field, title in fields:
            fieldmap.add_title(field, title)

        add_category_binds(fieldmap)

        to_str = lambda o: str(o) if o is not None else ''

        fieldmap.bind_wrapper('spots', to_str)
        fieldmap.bind_wrapper('latitude', to_str)
        fieldmap.bind_wrapper('longitude', to_str)

        xlsfile = StringIO()

        export_xls(
            directory=self.context,
            filehandle=xlsfile,
            language=get_current_language(self.context, request),
            as_template=False,
            fieldmap=fieldmap
        )

        return xls_response(request, 'kitas_export.xls', xlsfile)


class KitaZugDistribution(grok.Subscription):

    grok.context(IFacilityDirectory)
    grok.provides(IExportProvider)

    layer = IKitaSpecific

    id = 'kita-zug-distribution'
    title = _(u'Kita Zug Distribution')

    description = _(
        u'Custom export of the daycare centers in the canton of Zug '
        u'for distribution'
    )

    url = None

    def export(self, request):

        fields = [
            ('title', _(u'Name')),
            ('address', _(u'Address')),
            ('zipcode', _(u'Zipcode')),
            ('location', _(u'Location')),
            ('email', _(u'Email')),
            ('cat1', _(u'Type')),
            ('cat2', _(u'Location (Daycare Center)')),
            ('correspondence_first_name', _(u'Correspondence first name')),
            ('correspondence_last_name', _(u'Correspondence last name')),
            ('correspondence_address', _(u'Correspondence address')),
            ('correspondence_zipcode', _(u'Correspondence zipcode')),
            ('correspondence_town', _(u'Correspondence town')),
        ]

        fieldmap = FieldMap()
        fieldmap.root = True
        fieldmap.keyfields = ('title',)
        fieldmap.typename = 'seantis.dir.facility.item'
        fieldmap.add_fields(f[0] for f in fields)

        for field, title in fields:
            fieldmap.add_title(field, title)

        add_category_binds(fieldmap)

        xlsfile = StringIO()

        export_xls(
            directory=self.context,
            filehandle=xlsfile,
            language=get_current_language(self.context, request),
            as_template=False,
            fieldmap=fieldmap
        )

        return xls_response(request, 'kitas_export_versand.xls', xlsfile)
