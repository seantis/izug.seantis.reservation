from five import grok

from seantis.dir.base.interfaces import IDirectoryItem
from seantis.dir.base.item import DirectoryItemViewletManager
  
class ExtendedDirectoryItemViewlet(grok.Viewlet):
    grok.context(IDirectoryItem)
    grok.name('seantis.dir.base.item.detail')
    grok.require('zope2.View')
    grok.viewletmanager(DirectoryItemViewletManager)

    template = grok.PageTemplateFile('templates/listitem.pt')