import re
from .models import Category, Page, Revision, TextContent

from typing import Optional, List


def page_from_path(slugs: List[str]) -> Optional[Page]:
    """
    get-started/fundamentals/changing-a-course
    ['get-started', 'fundamentals', 'changing-a-course']

    moves to get-started (category)
        moves to fundamentals (category)
            returns changing-a-course (page)
    """
    if (not slugs or len(slugs) == 0): return 

    # iterate to the direct parent of the page, we dont grab the page directly because
    # iterating categories is pretty minimal in terms of cost and this way we can have
    # local slugs (two "basic" page slugs in different categories)
    parent = None
    for i in range(len(slugs)-1):
        try: 
            parent = Category.objects.get(parent=parent, slug=slugs[i])
        except Category.DoesNotExist:
            return

    try:
        return Page.objects.get(parent=parent, slug=slugs[-1]) # use last slug
    except Page.DoesNotExist:
        return 


def categories_from_page(page: Page) -> List[Category]:
    """
    recurses and returns list of parents from page
    """
    if (not page): return 
    parents = []

    current = page.parent
    while current:
        parents.append(current)
        current = current.parent

    return parents

    
def fetch_latest_revision(query_set) -> Optional[Revision]:
    revision_list = list(query_set)

    # try to get latest one
    if (len(revision_list) > 0):
        latest_rev = revision_list[0]
        current = latest_rev

        if (current.rollback):
            print ("Is Rollback")

            # iterate
            while current.rollback:
                current = current.rollback # set to latest

        return current

    return False


def revision_from_page(page: Page) -> Optional[Revision]:
    if (not page): return 

    try:
        query_set = page.revisions.order_by("-order")
        return fetch_latest_revision(query_set)

    except Revision.DoesNotExist:
        return 



def content_from_revision(revision: Revision) -> Optional[TextContent]:
    if (not revision): return 

    try:
        content = revision.content
        return content
        
    except TextContent.DoesNotExist:
        return
    

def text_from_content(content: TextContent) -> Optional[str]:
    if (content.flags == 0): 
        return content.text
    

def text_from_page(page) -> Optional[str]:
    revision = revision_from_page(page)
    if (not revision): return 

    content = content_from_revision(revision)
    if (not content): return 

    return text_from_content(content)


def text_from_path(path) -> Optional[str]:
    # the ultimate stack
    page = page_from_path(path)
    if (not page): return 

    # TODO rev was having some problems being fetched from page if manually created
    # something something order something?
    revision = revision_from_page(page)
    if (not revision): return 

    content = content_from_revision(revision)
    if (not content): return 

    return text_from_content(content)


def path_from_string(string: str, prefixes=1) -> str:
    # first letter is a root / generally
    return string[1:].split('/')[prefixes:]