from .models import Category, Page, Revision, TextContent

from typing import Optional, List


def page_from_slug(slug: str) -> Optional[Page]:
    """
    get-started/fundamentals/changing-a-course
    ['get-started', 'fundamentals', 'changing-a-course']

    moves to get-started (category)
        moves to fundamentals (category)
            returns changing-a-course (page)
    """
    if (not slug or slug == ''): return 

    try:
        return Page.objects.get(slug=slug)
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
    """ May take upto X seconds depending on location of content """
    if (content.flags == 0): 
        return content.text
    

def text_from_page(page) -> Optional[str]:
    revision = revision_from_page(page)
    if (not revision): return 

    content = content_from_revision(revision)
    if (not content): return 

    return text_from_content(content)


class CategoryWrapper:
    def __init__(self, node):
        self.node = node
        self.wrappers = []
        self.pages = []

def create_heirarchy() -> List[CategoryWrapper]:
    """ 
    Expensive operation - handle with care

    heirarchy: List[CategoryWrapper]

    CategoryWrapper
    -> 
    node = Category
    [CategoryWrapper, CategoryWrapper]
    [Page1, Page2, Page3, Page4]
    """

    def to_wrapper(pc: Category):
        w = CategoryWrapper(pc)

        # set pages
        w.pages = list(pc.child_pages.all())

        # set categories
        child_categories = list(pc.child_categories.all())
        w.wrappers = [to_wrapper(c) for c in child_categories]

        return w

    primary_categories = list(Category.objects.filter(parent=None))
    heirarchy = [to_wrapper(pc) for pc in primary_categories]

    
    return heirarchy
        