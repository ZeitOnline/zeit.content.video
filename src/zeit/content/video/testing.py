# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

import doctest
import pkg_resources
import plone.testing
import zeit.cms.testing
import zeit.solr.testing
import zeit.workflow.testing


product_config = """\
<product-config zeit.content.video>
    source-serie file://{0}
</product-config>
""".format(
    pkg_resources.resource_filename(__name__, 'tests/serie.xml'))


ZCML_LAYER = zeit.cms.testing.ZCML_Layer(
    'ftesting.zcml',
    product_config=(
        zeit.cms.testing.cms_product_config +
        zeit.solr.testing.product_config +
        zeit.workflow.testing.product_config +
        product_config))


LAYER = plone.testing.Layer(
    bases=(ZCML_LAYER, zeit.solr.testing.SOLR_MOCK_LAYER),
    name='Layer', module=__name__)


class TestCase(zeit.cms.testing.FunctionalTestCase):

    layer = LAYER


def FunctionalDocFileSuite(*args, **kw):
    kw.setdefault('layer', LAYER)
    kw['package'] = doctest._normalize_module(kw.get('package'))
    return zeit.cms.testing.FunctionalDocFileSuite(*args, **kw)


def playlist_factory(self):
    from zeit.content.video.playlist import Playlist
    with zeit.cms.testing.site(self.getRootFolder()):
        with zeit.cms.testing.interaction():
            playlist = Playlist()
            yield playlist
            self.repository['pls'] = playlist
    yield self.repository['pls']


def video_factory(self):
    from zeit.content.video.video import Video
    with zeit.cms.testing.site(self.getRootFolder()):
        with zeit.cms.testing.interaction():
            video = Video()
            yield video
            self.repository['video'] = video
    yield self.repository['video']
