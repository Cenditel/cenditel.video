"""Definition of the video content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from plone.registry.interfaces import IRegistry

from cenditel.video.interfaces import Ivideo
from cenditel.video.config import PROJECTNAME

# -*- Message Factory Imported Here -*-
from cenditel.video import videoMessageFactory as _

# -*- FileSystemStorage Import here -*-
from iw.fss.FileSystemStorage import FileSystemStorage

#validator imports
from Products.validation.config import validation
from Products.validation import V_REQUIRED
from cenditel.video.validators import ContentTypeValidator, TranscodeVideoValidator

videoSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.FileField(
        name='video',
        widget=atapi.FileWidget(
            label=_(u"Video"),
            description=_(u"The File to be uploaded")
        ),
        required=True,
        searchable=True,
        storage=FileSystemStorage(),
        validators=(
            ('checkFileMaxSize',V_REQUIRED),
            (ContentTypeValidator()),
            (TranscodeVideoValidator()),
        ),
    )
))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

videoSchema['title'].storage = atapi.AnnotationStorage()
videoSchema['description'].storage = atapi.AnnotationStorage()
videoSchema['description'].widget = atapi.RichWidget(label=_(u"Description"))

schemata.finalizeATCTSchema(videoSchema, moveDiscussion=False)

class video(base.ATCTContent):
    """it's video file with streming using html5"""
    implements(Ivideo)
    _at_rename_after_creation = True
    meta_type = "video"
    schema = videoSchema
    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    
atapi.registerType(video, PROJECTNAME)
