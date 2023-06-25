@register.tag(name="get_header")
def get_header(parser, token):
    try:
        tag_name, page_id = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires a single argument" % token.contents.split()[0]
        )
    return HeaderNode(page_id)
