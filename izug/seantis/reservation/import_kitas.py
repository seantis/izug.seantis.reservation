import transaction
import xlrd

from AccessControl.SecurityManagement import newSecurityManager
from plone.dexterity.utils import createContentInContainer
from Testing.makerequest import makerequest
from zope.component.hooks import setSite

from seantis.dir.base import utils


def number_cell(cell):
    if cell.ctype in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK):
        return 0
    if cell.ctype == xlrd.XL_CELL_TEXT:
        return int(float(cell.value))
    if cell.ctype == xlrd.XL_CELL_NUMBER:
        return int(cell.value)

    raise NotImplementedError


def load_xls(xls_path):
    workbook = xlrd.open_workbook(xls_path)
    sheet = workbook.sheet_by_name('Kitas')

    records = []
    for row in xrange(1, sheet.nrows):

        strcol = lambda col: unicode(sheet.cell(row, col).value).strip()
        intcol = lambda col: number_cell(sheet.cell(row, col))

        record = {}
        record['name'] = strcol(0)
        record['affix'] = strcol(1)
        record['notes'] = strcol(2)
        record['spots'] = intcol(3)
        record['address'] = strcol(4)
        record['zipcode'] = strcol(5)
        record['location'] = strcol(6)
        record['phone'] = strcol(7)
        record['email'] = strcol(8)
        record['url'] = strcol(9)
        record['fax'] = strcol(10)
        record['types'] = [s.strip() for s in strcol(11).split(',')]
        record['kita_location'] = strcol(12)
        record['age'] = strcol(13)
        record['languages'] = [s.strip() for s in strcol(14).split(',')]
        record['subsidized'] = not('Nicht' in strcol(15))
        record['holidays'] = strcol(16)
        record['opening_hours'] = strcol(17)
        record['contact'] = {
            'first_name': strcol(18),
            'last_name': strcol(19),
            'phone': strcol(20),
            'email': strcol(21),
        }
        record['correspondence'] = {
            'first_name': strcol(22),
            'last_name': strcol(23),
            'address': strcol(24),
            'zipcode': strcol(25),
            'town': strcol(26)
        }
        record['lat'] = strcol(27)
        record['lon'] = strcol(28)
        records.append(record)

    return records


def run_import(app, site_name, folder_path, records):
    # setup request and get plone site
    app = makerequest(app)
    site = app.unrestrictedTraverse(site_name)

    # setup user context
    admin = app.acl_users.getUserById("admin")
    newSecurityManager(app, admin)

    #setup site
    setSite(site)

    folder = site.unrestrictedTraverse(folder_path)
    assert folder.portal_type == 'seantis.dir.facility.directory'

    # clear folder
    for id in folder.contentIds():
        del folder[id]

    suggested_values = dict(cat1=set(), cat2=set(), cat3=set(), cat4=set())

    for record in records:
        facility = createContentInContainer(
            folder,
            'seantis.dir.facility.item',
            title=record['name'],
            description=''
        )

        facility.opening_hours = record['opening_hours']

        facility.cat1 = record['types']
        facility.cat2 = [record['kita_location']]
        facility.cat3 = record['subsidized'] and [u'Ja'] or [u'Nein']
        facility.cat4 = record['languages']

        map(suggested_values['cat1'].add, utils.flatten(facility.cat1))
        map(suggested_values['cat2'].add, utils.flatten(facility.cat2))
        map(suggested_values['cat3'].add, utils.flatten(facility.cat3))
        map(suggested_values['cat4'].add, utils.flatten(facility.cat4))

        facility.affix = record['affix']
        facility.spots = record['spots']
        facility.address = record['address']
        facility.zipcode = record['zipcode']
        facility.location = record['location']
        facility.phone = record['phone']
        facility.email = record['email']
        facility.url = record['url']
        facility.fax = record['fax']
        facility.age = record['age']
        facility.holidays = record['holidays']
        facility.contact_first_name = record['contact']['first_name']
        facility.contact_last_name = record['contact']['last_name']
        facility.contact_phone = record['contact']['phone']
        facility.contact_email = record['contact']['email']
        facility.correspondence_first_name = record['correspondence'][
            'first_name'
        ]
        facility.correspondence_last_name = record['correspondence'][
            'last_name'
        ]
        facility.correspondence_address = record['correspondence'][
            'address'
        ]
        facility.correspondence_zipcode = record['correspondence'][
            'zipcode'
        ]
        facility.correspondence_town = record['correspondence'][
            'town'
        ]
        facility.notes = record['notes']

        if record['lon'] and record['lat']:
            facility.set_coordinates('Point', map(
                float, (record['lon'], record['lat'])
            ))

        facility.image = None
        facility.contact = ''
        facility.infrastructure = ''
        facility.terms_of_use = ''

        facility.reindexObject()

    folder.cat1_suggestions = sorted(list(suggested_values['cat1']))
    folder.cat2_suggestions = sorted(list(suggested_values['cat2']))
    folder.cat3_suggestions = sorted(list(suggested_values['cat3']))
    folder.cat4_suggestions = sorted(list(suggested_values['cat4']))

    transaction.commit()


# If this script lives in your source tree, then we need to use this trick so
# that five.grok, which scans all modules, does not try to execute the script
# while modules are being loaded on the start-up
if "app" in locals():

    import sys

    site_name = sys.argv[-3]
    folder = sys.argv[-2]
    xls = sys.argv[-1]

    records = load_xls(xls)

    # access through locals to fool pylint
    run_import(locals()['app'], site_name, folder, records)
