import os
import yaml

ORDER = 999
PAINTINGS_PATH = 'paintings/'


def preBuild(site):
    """
    Every painting is defined by a YAML file.
    This function:
        - Loads the variables defined by these files
        - Converts these to a list of dicts representing all paintings
        - Makes them available for use across the site
    """

    PAINTINGS = []

    # Build all the paintings
    for page in site.pages():
        if page.path.startswith(PAINTINGS_PATH) and page.path.endswith('.yml'):

            ctx = yaml.load(page.data())

            # Build a context for each post
            paintingContext = {}
            paintingContext['name'] = ctx['name']
            paintingContext['width'] = ctx['width']
            paintingContext['height'] = ctx['height']
            paintingContext['materials'] = ctx['materials']
            paintingContext['date_added'] = ctx['date_added']
            paintingContext['main_image'] = site.config.get("gh-pages-prefix", "") + site.get_url_for_static(ctx['main_image'])
            paintingContext['short_description'] = ctx['short_description']
            PAINTINGS.append(paintingContext)
    PAINTINGS = sorted(PAINTINGS, key=lambda x: x['date_added'], reverse=True)

    for idx, p in enumerate(PAINTINGS):
        p['id'] = idx

    setattr(site, 'paintings', PAINTINGS)


def preBuildPage(site, page, context, data):
    """
    Add the list of posts to every page context so we can
    access them from wherever on the site.

    Determine how many items we add per column on the homepage
    """
    paintings = site.paintings
    paintings_first_col = [paintings[i] for i in range(len(paintings) // 2)]
    paintings_second_col = [paintings[i] for i in range(len(paintings) // 2, len(paintings))]
    context['paintings_first_col'] = paintings_first_col
    context['paintings_second_col'] = paintings_second_col
    context['paintings'] = paintings

    return context, data
