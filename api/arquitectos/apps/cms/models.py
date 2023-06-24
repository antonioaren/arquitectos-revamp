from django.db import models

from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.core.models import Page
from wagtail.documents.models import AbstractDocument
from wagtail.images.models import AbstractImage, AbstractRendition
from wagtail.images.models import Image as DefaultImage


class CustomImage(AbstractImage):
    """
    Extends the default Wagtail image object to add an "alt" field which is
    often required for SEO purposes.
    """

    alt = models.CharField(
        max_length=1000,
        help_text=_("Default alt text for image."),
        default="",
        blank=True,
    )

    admin_form_fields = (
        *DefaultImage.admin_form_fields,
        "alt",
    )

    class Meta(AbstractImage.Meta):
        verbose_name = _("image")
        verbose_name_plural = _("images")
        permissions = [
            ("choose_image", _("Can choose image")),
        ]


class CustomRendition(AbstractRendition):
    """
    Custom rendition model because we have a custom image model and it's
    mandatory to make the rendition go with it
    """

    image = models.ForeignKey(
        CustomImage,
        related_name="renditions",
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = (("image", "filter_spec", "focal_point_key"),)


class CustomDocument(AbstractDocument):
    """
    Extends the default document object. Does nothing for now but if one day
    you want to add another field to this model then it's going to be much
    easier. Otherwise just let it here.
    """

    admin_form_fields = ("title", "file", "collection", "tags")

    class Meta(AbstractDocument.Meta):
        permissions = [
            ("choose_document", _("Can choose document")),
        ]


class CTAButtonDefault(models.Model):
    label = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Label"),
        help_text=_("Label for the button"),
    )

    link = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Link"),
        help_text=_("Link for the button"),
    )

    page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Page"),
        help_text=_("Page to link to"),
    )


class HomePage(Page):
    """
    Home page, expected to be the root of the website. There is already a
    migration that will replace Wagtail's default root page by this. All you
    need to do is add fields there (if needed!).
    """

    parent_page_types = ["wagtailcore.Page"]

    class Meta:
        verbose_name = _("Home Page")
        verbose_name_plural = _("Home Pages")


class GalleryPage(Page):
    """
    Gallery page, expected to be a child of the home page. It's a simple page which contains a list of details images
    with their description.
    """
    parent_page_types = ["Homepage"]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["items"] = DetailsGalleryPage.objects.live().public().all()
        if context["items"] is None:
            context["items"] = []
        return context

    class Meta:
        verbose_name = _("Gallery Page")
        verbose_name_plural = _("Gallery Pages")


class DetailsGalleryPage(Page):
    """
    Details Gallery page, expected to be a child of the gallery page. It's a simple page which contains the details of
    an image like caption, description and the image itself.
    """

    parent_page_types = ["GalleryPage"]

    image = models.ForeignKey(
        CustomImage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Image"),
    )

    caption = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Caption"),
        help_text=_("Caption for the image at Gallery Page"))

    description = models.TextField(
        blank=True,
        verbose_name=_("Description"),
    )

    content_panels = Page.content_panels + [
        FieldPanel("image"),
        FieldPanel("caption"),
        FieldPanel("description"),
    ]

    class Meta:
        verbose_name = _("Details Gallery Page")
        verbose_name_plural = _("Details Gallery Pages")
