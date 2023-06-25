from django.utils.translation import gettext_lazy as _
from wagtail.core import blocks
from wagtail.core.blocks import StreamBlock
from variables import AUTHOR_CHOICES

class HeaderSubcategoryBlock(blocks.StructBlock):
    title = blocks.CharBlock(label='Título', max_length=100)

    author = blocks.ChoiceBlock(
        choices=AUTHOR_CHOICES,
        label='Autor',
        default=AUTHOR_CHOICES[0][0],
    )


class HeaderCategoryBlock(blocks.StructBlock):
    """
    Header block with a title and a category
    """
    title = blocks.CharBlock(label='Título', max_length=100)
    category_page = blocks.PageChooserBlock(label='Categoría')
    subcategories = StreamBlock(
        [("subcategory", HeaderSubcategoryBlock())],
        block_counts={"anchors": {"min_num": 1, "max_num": 4}},
        label=_("sub-categoras"),
    )

    class Meta:
        template = 'cms/blocks/header_category_block.html'
        icon = 'fa fa-list'
        label = 'Cabecera de Categoría'
