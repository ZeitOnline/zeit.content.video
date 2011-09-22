# Copyright (c) 2010-2011 gocept gmbh & co. kg
# See also LICENSE.txt

import unittest2 as unittest  # XXX
import zeit.solr.interfaces
import zope.component


class TestSolrIndexing(zeit.content.video.testing.TestCase):

    def setUp(self):
        super(TestSolrIndexing, self).setUp()
        self.solr = zope.component.getUtility(
            zeit.solr.interfaces.ISolr)
        self.solr.reset_mock()

    def get_test(self, name):
        # A test "generator"
        from zeit.content.video.video import Video
        video = Video()
        # Yield the video to the outer scope
        yield video
        # Receive the expected value from the outer scope
        expected = yield
        self.repository['123'] = video
        video = self.repository['123']
        updater = zeit.solr.interfaces.IUpdater(video)
        updater.update()
        element_add = self.solr.update_raw.call_args_list[0][0][0]
        self.assertEquals(
            [expected],
            element_add.xpath("/add/doc/field[@name='%s']"% name))

    def test_flv_url_should_be_indexed(self):
        test = self.get_test('h264_url')
        video = test.next()  # get prepared test object
        video.flv_url = u'http://flvurl'
        test.send(u'http://flvurl')  # Send expected result

    def test_banner_should_be_indexed(self):
        test = self.get_test('banner')
        video = test.next()
        video.banner = True
        test.send(True)

    def test_banner_id_should_be_indexed(self):
        test = self.get_test('banner_id')
        video = test.next()
        video.banner_id = '32kcdc'
        test.send('32kcdc')