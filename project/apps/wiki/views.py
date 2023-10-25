from django.http import HttpResponse, HttpRequest
from django.template import loader

from .fetch import slug_from_path, page_from_slug, text_from_page, H
from .renderer.run import render_to_html, markdown_builder

prefix = '/wiki'

md = markdown_builder()
h = H()

def index(request):
    return HttpResponse("Hello, world. You're at the wiki index.")

def content(request: HttpRequest):
    slug = slug_from_path(request.path, prefixes=1)
    page = page_from_slug(slug)
    text = text_from_page(page)

    if (text):
        rendered_page_text = render_to_html(md, text)

        context = {
            "page_title": page.title, 
            "sections": rendered_page_text.sections,
            "content": rendered_page_text.content,
            "hierarchy": h.get(),
            "edit_page_url": prefix + '/edit/' + slug,
        }
        template = loader.get_template("wiki/content.html")

        return HttpResponse(template.render(context, request))
    return HttpResponse('404')