from foo_get_posts_handler import FooGetPostsHandler
from foo_get_post_handler import FooGetPostHandler
from foo_write_post_handler import FooWritePostHandler
from foo_handler import FooHandler
from api_utils import ApiEntrypoint


def handler(event, context=None):

    entry_point = (
        ApiEntrypoint()
        .with_handler(FooHandler())
        .with_handler(FooWritePostHandler())
        .with_handler(FooGetPostHandler())
        .with_handler(FooGetPostsHandler())
    )

    return entry_point.handle(event, context)
