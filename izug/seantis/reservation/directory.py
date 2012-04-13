from five import grok

from seantis.dir.base.directory import IDirectory
from seantis.dir.base.directory import DirectoryViewletManager

class ExtendedDirectoryViewlet(grok.Viewlet):
    grok.context(IDirectory)
    grok.name('seantis.dir.base.directory.detail')
    grok.require('zope2.View')
    grok.viewletmanager(DirectoryViewletManager)

    template = grok.PageTemplateFile('templates/directorydetail.pt')