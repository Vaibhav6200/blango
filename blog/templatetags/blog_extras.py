from django.contrib.auth import get_user_model
from django import template
from django.utils.html import escape, format_html
from django.utils.safestring import mark_safe
from blog.models import Post


user_model = get_user_model()
register = template.Library()


@register.filter
def author_details(author, current_user=None):
    if not isinstance(author, user_model):
        return ""

    if author == current_user:
        return format_html("<strong>Me</strong>")

    if author.first_name == "" and author.last_name == "":
        name = author.username

    else:
        name = escape(author.first_name) + " " + author.last_name


    if author.email !=  "":
        # METHOD1
        # email = escape(author.email)
        # prefix = f"<a href='mailto:{email}'>"

        # METHOD 2: Instead of first escaping HTML and then creating our HTML both can be done simultaneously
        prefix = format_html("<a href='mailto:{}'>", author.email)
        suffix = format_html("</a>")
    else:
        prefix = ""
        suffix = ""

    result = f"{prefix}{name}{suffix}"

    return mark_safe(result)


# mark_safe: Exact same as "safe" filter -> marks your string safe so if it contains HTML then it will be executed
# escape: <script> -> &lt;script&gt;   = our code will be displayed but wont be executed -> convertes HTML into text


@register.simple_tag        # to be safe, simple_tags automatically escape their output.
def row(extra_classes=""):
    return format_html('<div class="row {}">', extra_classes)


@register.simple_tag
def endrow():
    return format_html('</div>')


@register.simple_tag
def col(extra_classes=""):
    return format_html('<div class="col {}">', extra_classes)


@register.simple_tag
def endcol():
    return format_html("</div>")



# Template tag that takes no argument (using Context variable)
@register.simple_tag(takes_context=True)
def author_details_tag(context):
    request = context["request"]
    current_user = request.user
    post = context["post"]
    author = post.author

    if author == current_user:
        return format_html("<strong>me</strong>")

    if author.first_name and author.last_name:
        name = f"{author.first_name} {author.last_name}"
    else:
        name = f"{author.username}"

    if author.email:
        prefix = format_html('<a href="mailto:{}">', author.email)
        suffix = format_html("</a>")
    else:
        prefix = ""
        suffix = ""

    return format_html("{}{}{}", prefix, name, suffix)



# Benefit of using inclusion tag: A post object is passed to the recent_posts template tag. Now the template tag can access any information in the Post object
@register.inclusion_tag('blog/post-list.html')
def recent_posts(post):
    posts = Post.objects.exclude(pk=post.pk)[:5]
    return {'title': "Recent Posts", "posts": posts}