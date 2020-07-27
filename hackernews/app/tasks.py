from app.database import db
from app.database.models import Post
from app.utils.hn_scrapper import get_news_list


def fetch_data():
    """ Update DB """
    for f in get_news_list():
        if not Post.query.filter_by(id_hn=f['id']).first():
            instance = Post(id_hn=f['id'],
                            title=f['title'],
                            created_hn=f['approx_created_at'],
                            url=f['url'])
            db.session.add(instance)

    db.session.commit()
