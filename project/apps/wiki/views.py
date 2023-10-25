from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.template import loader

from .fetch import page_from_slug, text_from_page, create_heirarchy

from .renderer.run import render_to_html, markdown_builder

prefix = '/wiki'

class H:
    def __init__(self) -> None:
        self.update()
    
    def update(self):
        # TODO allow elements to update this instead of reconstructing
        # ie pass in nullable category and nullable page and add 
        self.hierarchy = create_heirarchy()

md = markdown_builder()
h = H()

def index(request):
    return HttpResponse("Hello, world. You're at the wiki index.")

def edit(request):
    path = path_from_string(request.path, prefixes=2)
    page = page_from_path(path)
    text = text_from_page(page)

    if (text):
        rendered_page_text = render_to_html(md, text)

        context = {
            "page_title": page.title, 
            "sections": rendered_page_text.sections,
            "content": rendered_page_text.content,
            "hierarchy": h.hierarchy,
            "edit_page_url": prefix + '/edit/' + '/'.join(path)
        }
        template = loader.get_template("wiki/edit/base.html")

        return HttpResponse(template.render(context, request))
    return HttpResponse('404')


def content(request: HttpRequest):
    slug = request.path.split('/')[1:]
    page = page_from_slug(slug)
    text = text_from_page(page)

    if (text):
        rendered_page_text = render_to_html(md, text)

        context = {
            "page_title": page.title, 
            "sections": rendered_page_text.sections,
            "content": rendered_page_text.content,
            "hierarchy": h.hierarchy,
            "edit_page_url": prefix + '/edit/' + '/'.join(path)
        }
        template = loader.get_template("wiki/content.html")

        return HttpResponse(template.render(context, request))
    return HttpResponse('404')