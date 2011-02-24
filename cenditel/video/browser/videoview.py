#######################################
#python imports
import urlparse
#######################################
#Zope and Plone imports
from zope.interface import implements, Interface
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
###############################################3
from Acquisition import aq_inner
from zope.component import getMultiAdapter
#utility control panel imports
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from Acquisition import interfaces
##########################################
#Products Imports
from cenditel.video import videoMessageFactory as _
from cenditel.transcodedeamon.convert import MFN as MFNI
from cenditel.transcodedeamon.convert import newtrans_init_
from cenditel.transcodedeamon.convert import MTD as MTDI
#from cenditel.transcodedeamon.convert import ServiceList
from cenditel.transcodedeamon import manipulatefilename

##########################################
#Options Imports
from cenditel.transcodedeamon.interfaces import ITranscodeSetings


class IvideoView(Interface):
    """
    video view interface
    """

    def test():
        """ test method"""

class videoView(BrowserView):
    """
    video browser view
    """
    implements(IvideoView)
    
    def __init__(self, context, request):
	self.context = context
	self.request = request
	#self.VariableEjemplo = ""
	self.MyTitle = ""
	self.MyTitleWhitOutSpace = ""
	self.filename = ""
	self.newfilename = ""
	self.filenamesaved= ""
	self.folderfile = ""
	self.StatusOfFile = ""
	self.filesize = ""
	self.SERVER = ""
	self.folderfileOGG=""
	self.PathOfFile=""
	self.STORAGE=""
	self.AbsoluteServerPath=""
	self.variable=""
	#print self.request.items()


    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

	
    def SALUDO(self, nombre):
        return "hola"+ str(nombre)

    def Hola(self):
	J = convert.HelloWorld()
	return J.HolaMundo()

    def VariableDeEjemplo(self):
	self.VariableEjemplo="Hola-----------Mundo"
	return self.VariableEjemplo

    def RemoveSlash(self, path):
	reverse=path[::-1]
	newpath=""
	if reverse[0]=='/':
	    for x in cadena[:-1]:
		newcadena=newcadena+x
	    return newpath
	else:
	    return path

    def PlayingVideoType(self):
	import pdb; pdb.set_trace()
	registry = getUtility(IRegistry)
	settings = registry.forInterface(ITranscodeSetings)
	self.SERVER = self.RemoveSlash(settings.adress_of_streaming_server)
	PARAMETRES_TRANSCODE = settings.ffmpeg_parameters_video_line
	self.STORAGE = self.RemoveSlash(settings.mount_point_fss)
	self.MyTitle = self.context.Title()
	idvideo=self.context.getId()
	"""
	virtualobject=self.context.getAudio()
	self.filenamesaved=virtualobject.filename
	"""
	self.MyTitleWhitOutSpace = MFNI.TitleDeleteSpace(self.MyTitle) 
	self.filename = MFNI.DeleteSpaceinNameOfFolderFile(self.MyTitleWhitOutSpace)
	url = self.context.absolute_url()
	self.PathOfFile = MFNI.ReturnPathOfFile(url)
	self.filenamesaved = MFNI.ReturnFileNameOfFileSaved(self.STORAGE, self.PathOfFile)
	#print "IT IS THE NAME OF THE FILE SAVED " + self.filenamesaved
	self.MyTitleWhitOutSpace = MFNI.DeleteSpaceinNameOfFolderFile(self.MyTitleWhitOutSpace)
	newtrans_init_(self.STORAGE, self.PathOfFile, self.filenamesaved, PARAMETRES_TRANSCODE, idvideo)
	self.folderfileOGG=MTDI.newname(self.PathOfFile+'/' + self.filenamesaved)
	self.AbsoluteServerPath = self.SERVER + MTDI.nginxpath(self.folderfileOGG)
	self.variable=MTDI.nginxpath(self.STORAGE+self.folderfileOGG)
	#################
	#import pdb; pdb.set_trace()
	##########(Verificar valores pasados a available)
	self.StatusOfFile = ServiceList.available(idvideo, self.variable)
	#print "El STATUS OF FILE IN THE VIEW "+ str(self.StatusOfFile)
	if self.StatusOfFile == True:
	    self.newfilename=MTDI.newname(self.filenamesaved)
	else:
	    self.newfilename=_('The file is not ready yet, please contact site administration')
	return 

    def GETFileSize(self):
	self.filesize = MFNI.ReturnFileSizeOfFileInHardDrive(self.variable)
	thefilesize = self.filesize
	return thefilesize 

    def GETAdressOfVideoFromApache(self):
	TheFilePath = self.AbsoluteServerPath
	return TheFilePath

    def GETStatusOfFile(self):
	TheStatus = self.StatusOfFile
	str(TheStatus)
	return TheStatus


    def GETNewNameVideo(self):

	TheNewName = self.newfilename
	return TheNewName

    def GETfolderfile(self):
	TheFolderFile = self.AbsoluteServerPath 
	return TheFolderFile 


    def GETMyTitle(self):
	MyTitleWhitOutSpace  = self.MyTitleWhitOutSpace
	return MyTitleWhitOutSpace

    def ExternalMethodforURL(self):
	return self.context.absolute_url()


    def URLElement(self):
	url = self.context.absolute_url()
	self.PathOfFile = MFNI.ReturnPathOfFile(url)
	return self.PathOfFile

