# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

import zeit.cms.testing
import zeit.content.video.testing


def video_factory(self):
    from zeit.content.video.video import Video
    with zeit.cms.testing.site(self.getRootFolder()):
        with zeit.cms.testing.interaction():
            video = Video()
            yield video
            self.repository['video'] = video
    yield self.repository['video']


class KeywordTest(zeit.cms.testing.SeleniumTestCase):

    layer = zeit.brightcove.testing.selenium_layer
    skin = 'vivi'

    def setUp(self):
        from zeit.cms.tagging.tag import Tag
        import transaction
        import zeit.cms.tagging.interfaces
        import zope.component
        super(KeywordTest, self).setUp()
        with zeit.cms.testing.site(self.getRootFolder()):
            whitelist = zope.component.getUtility(
                zeit.cms.tagging.interfaces.IWhitelist)
            whitelist['test1'] = Tag('test1')
            whitelist['test2'] = Tag('test2')
        video_factory(self).next()
        transaction.commit()

    def test_autocomplete_and_save(self):
        self.open('/repository/video/@@checkout')
        s = self.selenium
        s.waitForElementPresent('css=input.autocomplete')
        s.typeKeys('css=input.autocomplete', 't')
        s.waitForVisible('css=.ui-autocomplete')
        s.assertText('css=.ui-autocomplete a', 'test1')
        #s.click('css=.ui-autocomplete a:contains(test1)')
        # down arrow
        s.keyDown('css=input.autocomplete', r'\40')
        # return
        s.keyDown('css=input.autocomplete', r'\13')
        s.waitForElementPresent('css=.objectsequencewidget li h3')
        s.assertText('css=.objectsequencewidget li h3', 'test1')
        s.click('id=form.actions.apply')
        s.waitForElementPresent('css=.objectsequencewidget li h3')
        s.assertText('css=.objectsequencewidget li h3', 'test1')


class TestThumbnail(zeit.cms.testing.BrowserTestCase):

    layer = zeit.content.video.testing.Layer

    def test_view_should_redirect_to_video_thumbnail_url(self):
        import urllib2
        factory = video_factory(self)
        video = factory.next()
        video.thumbnail = 'http://thumbnailurl'
        factory.next()
        self.browser.open('http://localhost/++skin++vivi/repository/video/')
        self.browser.mech_browser.set_handle_redirect(False)
        with self.assertRaises(urllib2.HTTPError) as e:
            self.browser.open('@@thumbnail')
        self.assertEqual('HTTP Error 303: See Other', str(e.exception))
        self.assertEqual('http://thumbnailurl',
                         e.exception.hdrs.get('location'))


class TestPlaylist(zeit.cms.testing.BrowserTestCase):

    layer = zeit.content.video.testing.Layer

    def test_playlist_should_be_viewable(self):
        from zeit.content.video.playlist import Playlist
        pls = Playlist()
        with zeit.cms.testing.site(self.getRootFolder()):
            with zeit.cms.testing.interaction():
                self.repository['453'] = pls
        self.browser.open('http://localhost/++skin++vivi/repository/453')
        self.assert_ellipsis("""...
<...
   <label for="form.__name__">
           <span>File name</span>
         </label>...
        <div class="widget">453</div>...
                             """)