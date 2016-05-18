from zeit.cms.content.browser.form import CommonMetadataFormBase
from zeit.cms.i18n import MessageFactory as _
import gocept.form.grouped
import zeit.cms.related.interfaces
import zeit.cms.workflow.interfaces
import zeit.content.video.interfaces
import zope.dublincore.interfaces
import zope.formlib.form


class Edit(zeit.cms.browser.form.EditForm):

    title = _('Video')

    form_fields = zope.formlib.form.FormFields(
        zeit.content.video.interfaces.IVideo,
        zeit.cms.related.interfaces.IRelatedContent,
        zeit.cms.workflow.interfaces.IPublishInfo,
        zope.dublincore.interfaces.IDCTimes,
        render_context=zope.formlib.interfaces.DISPLAY_UNWRITEABLE
    ).select(
        'supertitle', 'title', 'subtitle', 'teaserText',
        'product', 'ressort', 'keywords', 'serie',
        'dailyNewsletter', 'banner', 'banner_id',
        'breaking_news', 'has_recensions', 'commentsAllowed',
        'related', 'channels', 'lead_candidate', 'transcript',
        # remaining:
        '__name__',
        'created', 'date_first_released', 'modified', 'expires',
        'thumbnail', 'video_still', 'flv_url')

    field_groups = (
        gocept.form.grouped.Fields(
            _("Texts"),
            ('supertitle', 'title', 'teaserText', 'transcript'),
            css_class='wide-widgets column-left'),
        gocept.form.grouped.Fields(
            _("Navigation"),
            ('product', 'ressort', 'keywords', 'serie'),
            css_class='column-right'),
        gocept.form.grouped.Fields(
            _("Options"),
            ('dailyNewsletter', 'banner', 'banner_id',
             'breaking_news', 'has_recensions', 'commentsAllowed'),
            css_class='column-right checkboxes'),
        CommonMetadataFormBase.auto_cp_fields,
        gocept.form.grouped.Fields(
            _('Teaser elements'),
            ('related',),
            'wide-widgets'),
    )


class Thumbnail(zeit.cms.browser.view.Base):

    @property
    def thumbnail_url(self):
        return self.context.thumbnail

    def __call__(self):
        return self.redirect(self.thumbnail_url, trusted=True)


class ThumbnailURL(zope.traversing.browser.absoluteurl.AbsoluteURL):

    def __str__(self):
        if self.context.thumbnail_url:
            return self.context.thumbnail_url
        raise TypeError("No Thumbnail")


class Still(zeit.cms.browser.view.Base):

    @property
    def video_still_url(self):
        return self.context.video_still

    def __call__(self):
        return self.redirect(self.video_still_url, trusted=True)


class StillURL(zope.traversing.browser.absoluteurl.AbsoluteURL):

    def __str__(self):
        if self.context.video_still_url:
            return self.context.video_still_url
        raise TypeError("No still url")


class PlaylistDisplayForm(zeit.cms.browser.form.DisplayForm):

    title = _('View playlist')

    form_fields = zope.formlib.form.FormFields(
        zeit.content.video.interfaces.IPlaylist)
