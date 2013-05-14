import transaction
import xlrd

from AccessControl.SecurityManagement import newSecurityManager
from plone.dexterity.utils import createContentInContainer
from Testing.makerequest import makerequest
from zope.component.hooks import setSite


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
        record['description'] = strcol(2)
        record['spots'] = intcol(3)
        record['address'] = strcol(4)
        record['zipcode'] = intcol(5)
        record['city'] = strcol(6)
        record['phone'] = strcol(7)
        record['email'] = strcol(8)
        record['url'] = strcol(9)
        record['fax'] = strcol(10)
        record['types'] = [s.strip() for s in strcol(11).split(',')]
        record['location'] = strcol(12)
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
            'zipcode': intcol(25),
            'city': strcol(26)
        }
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
    assert folder.portal_type == 'seantis.dir.base.directory'

    # clear folder
    for id in folder.contentIds():
        del folder[id]

    for record in records:
        facility = createContentInContainer(
            folder,
            'seantis.dir.base.item',
            title=record['name'],
            description=record['description']
        )

        facility.opening_hours = record['opening_hours']

        facility.cat1 = record['types']
        facility.cat2 = [record['location']]
        facility.cat3 = record['subsidized'] and [u'Ja'] or [u'Nein']
        facility.cat4 = record['languages']

        facility.affix = record['affix']
        facility.spots = int(record['spots'])
        facility.address = record['address']
        facility.zipcode = record['zipcode']
        facility.city = record['city']
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
        facility.correspondence_city = record['correspondence'][
            'city'
        ]
        facility.image = None
        facility.notes = ''
        facility.contact = ''
        facility.infrastructure = ''
        facility.terms_of_use = ''

    transaction.commit()


# If this script lives in your source tree, then we need to use this trick so
# that five.grok, which scans all modules, does not try to execute the script
# while modules are being loaded on the start-up
if "app" in locals():

    import sys
    site_name = sys.argv[1]
    folder = sys.argv[2]
    xls = sys.argv[3]

    records = load_xls(xls)

    # access through locals to fool pylint
    run_import(locals()['app'], site_name, folder, records)
