import collections
import inspect
import re
from django.core.management.base import BaseCommand
import urls


def guess_wrapper(cells):
    # look through the funciton closure for cells that look
    # like wrapped functions. for multuple functions,
    # attempt to guess which is the more likely candidate

    # we add points for
    # * non-lambda
    # * 'request' in arg list

    functions = collections.defaultdict(list)
    for cell in cells:
        contents = cell.cell_contents
        if not inspect.isfunction(contents):
            continue

        score = 0
        if contents.__name__ != '<lambda>':
            score += 1
        if 'request' in inspect.getargspec(contents).args:
            score += 1

        functions[score].append(contents)

    for score in reversed(sorted(functions.keys())):
        return functions[score][0]
    return None


def unwrap_and_compare(kwargs_provided, callback, description):
    # if the callback is decorated, unwrap to find the
    # original view

    # if we have a decorated function, the "wrapped"
    # function should b in the closure of the decorator
    # so we look for functions in the closure, guessing
    # if neccessary.

    if callback is not None:
        while callback.func_closure:
            compare(kwargs_provided, callback, description)
            cells = callback.func_closure
            guess = guess_wrapper(cells)
            if guess:
                callback = guess
            else:
                # nothing in the closure was a function, so give up
                break
        compare(kwargs_provided, callback, description)


def compare(kwargs_provided, callback, description):
    spec = inspect.getargspec(callback)

    args = spec.args
    defaults = spec.defaults
    if defaults:
        required_args = args[:-len(defaults)]
    else:
        required_args = args

    missing_kwargs = set(required_args) - kwargs_provided
    if missing_kwargs:
        print "%s: view requires kwargs %s not in the url kwargs" % (
            description, list(missing_kwargs))


    if spec.keywords:
        # signature contains **kwargs, so can't do second check
        return

    extra_kwargs = kwargs_provided - set(args)
    if extra_kwargs:
        print "%s: url provides kwargs %s not in the view signature" % (
            description, list(extra_kwargs))



def check_resolver(entry, prefix):
    effective_regex = re.compile(prefix + entry.regex.pattern)

    # skip the admin
    if effective_regex.pattern.startswith('^admin/'):
        return

    description = (getattr(entry, 'name', None) or effective_regex.pattern)

    kwargs_provided = set(['request'] + getattr(entry, 'default_args', {}).keys())
    kwargs_provided.update(effective_regex.groupindex.keys())

    unwrap_and_compare(kwargs_provided, entry.callback, description)




def show_urls(urllist, prefix=''):
    for entry in urllist:
        check_resolver(entry, prefix)

        if hasattr(entry, 'url_patterns'):
            show_urls(entry.url_patterns, prefix + entry.regex.pattern)


class Command(BaseCommand):
    help = "Inspect urlpatterns and their views looking for mismatched arguments"

    def handle(self, *labels, **options):

        show_urls(urls.urlpatterns)
