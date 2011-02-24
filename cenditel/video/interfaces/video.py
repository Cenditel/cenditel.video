from zope.interface import Interface
# -*- Additional Imports Here -*-
from plone.theme.interfaces import IDefaultPloneLayer


class Ivideo(Interface):
    """it's video file with streming using html5"""

    # -*- schema definition goes here -*-
class IvideoSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 skin layer 
       for this product."""