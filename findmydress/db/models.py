import json
import os

import boto3
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('postgresql+psycopg2://localhost/findmydress', echo=True)
Session = sessionmaker()
Session.configure(bind=engine)


Base = declarative_base()


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    label = Column(String)
    detail_url = Column(String)

    images = relationship("ItemImage")

    def __repr__(self):
        return u'<Item (id={} label="{}" detail_url="{}")>'.format(
            self.id, self.label, self.detail_url,
            )


class ItemImage(Base):
    __tablename__ = 'item_images'

    id = Column(Integer, primary_key=True)
    original_url = Column(String)
    checksum = Column(String)
    position = Column(Integer)
    image_s3_url = Column(String, nullable=True)

    item_id = Column(Integer, ForeignKey('items.id'))
    item = relationship("Item", primaryjoin=item_id == Item.id)

    def __repr__(self):
        return u'<ItemImage (id={} position={} image_path="{}")>'.format(
            self.id, self.position, self.image_path,
            )


class ImageDerivative(Base):
    __tablename__ = 'image_derivatives'

    id = Column(Integer, primary_key=True)
    type = Column(String)
    original_image = Column(Integer, ForeignKey('item_images.id'))
    image_s3_url = Column(String)


def import_scraped_items(output_json_path, file_path_root):
    session = Session()

    items_json = json.load(open(output_json_path))
    for item_json in items_json:
        item = (session.query(Item)
               .filter(Item.detail_url==item_json['detail_url'])
               .one_or_none())

        if not item:
            item = Item(
                label=item_json['item_title'],
                detail_url=item_json['detail_url'],
                )
            session.add(item)
            session.commit()
        
        item_images = []
        for img, item_img in zip(item_json['images'], item_json['item_images']):
            if item_img['type'] != 'high-res':
                continue

            image = (session.query(ItemImage)
                    .filter(ItemImage.checksum==img['checksum'])
                    .one_or_none())
            if image:
                continue

            image_path = os.path.join(file_path_root, img['path'])
            s3_path = os.path.join('files/images/full', os.path.basename(image_path))
            image_s3_url = upload_image_file(image_path, s3_path)

            image = ItemImage(
                original_url=item_img['url'],
                position=item_img['position'],
                checksum=img['checksum'],
                image_s3_url=image_s3_url,
                item_id=item.id,
                )
            item_images.append(image)

        session.add_all(item_images)
        session.commit()


def upload_image_file(path, s3_path):
    if not os.path.isfile(path):
        raise ValueError("No file at path {}".format(path))

    bucket_name = 'findmydress'
    s3 = boto3.resource('s3')
    key = s3.Object(bucket_name, s3_path)
    key.put(Body=open(path, 'rb'))

    return 's3://{}'.format(os.path.join(bucket_name, s3_path))
