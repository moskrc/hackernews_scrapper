from flask_restx import reqparse
from flask import current_app


def request_parser():
    """
    Pagination parser - extract limit and page from request parameters
    :return: dict - parsed arguments
    """
    limit_offset_order_request_parser = reqparse.RequestParser()
    limit_offset_order_request_parser.add_argument(
        "order",
        type=str,
        dest="order",
        location="args",
        help="Column used for ordering",
        choices=['title', 'url', 'created', 'id'],
        default=current_app.config['PAGINATION_DEFAULT_ORDER']
    )
    limit_offset_order_request_parser.add_argument(
        "dir",
        type=str,
        dest="dir",
        location="args",
        help="Reverse",
        choices=['asc', 'desc', ],
        default=current_app.config['PAGINATION_DEFAULT_ORDER_DIRECTION']
    )
    limit_offset_order_request_parser.add_argument(
        'limit',
        type=int,
        help='Records per page',
        default=current_app.config['PAGINATION_DEFAULT_LIMIT']
    )
    limit_offset_order_request_parser.add_argument(
        'offset',
        type=int,
        help='Offset',
        default=current_app.config['PAGINATION_DEFAULT_OFFSET']
    )
    args = limit_offset_order_request_parser.parse_args()

    # Ensure parameters do not exceed maximum limit
    if args['limit'] > current_app.config['PAGINATION_MAX_LIMIT']:
        args['limit'] = current_app.config['PAGINATION_MAX_LIMIT']

    return args
