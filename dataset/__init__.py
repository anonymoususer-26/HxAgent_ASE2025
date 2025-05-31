from dataset.popularsite import get_popular_task_factory_by_id, get_all_popular_task_factories

from dataset.task_factory import MiniwobTaskFatory
from error import CannotOpenTaskError
import os

tasks = [
    "click-button",
    "click-checkboxes",
    "click-checkboxes-large",
    "click-checkboxes-soft",
    "click-collapsible",
    "click-option",
    "click-dialog",
    "click-dialog-2",
    "click-link",
    "click-scroll-list",
    "click-tab",
    "click-test",
    "click-test-2",
    "click-widget",
    "enter-password",
    "enter-text",
    "enter-text-2",
    "enter-text-dynamic",
    "focus-text",
    "focus-text-2",
    "grid-coordinate",
    "login-user",
    "multi-layouts",
    "multi-orderings",
    "read-table",
    "social-media-all",
    "social-media-some",
    "click-menu-2",
    "click-pie",
    "navigate-tree",
    "click-collapsible-2",
    "click-tab-2",
    "click-tab-2-hard",
    "social-media",
    "search-engine",
    "email-inbox",
    "email-inbox-forward-nl",
    "email-inbox-forward-nl-turk",
    "email-inbox-nl-turk",
    "use-spinner",
    "guess-number",
    "choose-date",
    "book-flight-nodelay",
]

flight_tasks = [
    "flight.Alaska",
    "flight.Alaska-auto",
    "flight.AA"
]


cur_path_dir = os.path.dirname(os.path.realpath('__file__'))
miniwob_dir = os.path.join(cur_path_dir, "dataset", "miniwob", "miniwob")
base_url = "file:///{}".format(miniwob_dir)
urls = list(map(lambda task, base_url=base_url: [task, "{}/{}.html".format(base_url, task)], tasks)) 
miniwob_task_factories = [MiniwobTaskFatory(url[0], url[1], url[0]) for url in urls]
flight_miniwob_dir = os.path.join(cur_path_dir, "dataset", "miniwob", "flight")
flight_base_url = "file:///{}".format(flight_miniwob_dir)
flight_urls = list(map(lambda task: [task, "{}/{}/wrapper.html".format(flight_base_url, task.split(".")[1])], flight_tasks)) 
flight_miniwob_task_factories = [MiniwobTaskFatory(url[0], url[1], url[0]) for url in flight_urls]
miniwob_task_factories = miniwob_task_factories + flight_miniwob_task_factories
urls = urls + flight_urls

def get_miniwob_task_factory_by_id(task_id):
    for miniwob_task in miniwob_task_factories:
        if miniwob_task.id == task_id:
            return miniwob_task
    raise CannotOpenTaskError()

def get_all_miniwob_task_factories():
    return miniwob_task_factories