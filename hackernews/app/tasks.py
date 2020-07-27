from app.database import db
from app.database.models import Post
from app.utils.hn_scrapper import get_news_list
import logging

logger = logging.getLogger()


def fetch_data():
    """ Update DB """
    for f in get_news_list():
        logger.debug(f'Looking for post with ID={f["id"]}')
        if not Post.query.filter_by(id_hn=f['id']).first():
            logger.debug('Create new post')
            instance = Post(id_hn=f['id'],
                            title=f['title'],
                            created_hn=f['approx_created_at'],
                            url=f['url'])
            db.session.add(instance)

    db.session.commit()
