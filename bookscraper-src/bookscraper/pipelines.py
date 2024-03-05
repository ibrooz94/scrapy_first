# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re
import logging
from itemadapter import ItemAdapter
from .database import db_connect, create_table, create_session, ChartaData

logger = logging.getLogger('FIRST')

def clean_email(input_string):
    if not input_string: return None 
    
    # Define the regex pattern to match <a> and <span> tags
    pattern_a = r'<a\s*[^>]*>(.*?)<\/a>'
    pattern_span = r'<span\s*[^>]*>(.*?)<\/span>'

    # Substitute <a> and <span> tags with an empty string
    result = re.sub(pattern_a, r'\1', input_string)
    result = re.sub(pattern_span, r'\1', result)

    return result

class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter =  ItemAdapter(item)

        # Experiment item cleaning
        url_field = 'url'
        adapter[url_field] = adapter.get(url_field)[3:]

        return item
    
class ChartascraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()

        # strip all whitespaces from strings
        for field_name in field_names:
            value = adapter.get(field_name)
            adapter[field_name] = value.strip() if value else None

        # clean email 
        email_string = clean_email(adapter.get('email'))
        adapter['email'] = email_string

        # clean website
        website = adapter.get('website')
        if website:
            # Standardize protocol:
            if not website.startswith('http'):
                website = f'https://{website}'
            elif website.startswith('http://'):
                # Explicitly change http to https
                website = f'https{website[4:]}'

            adapter['website'] = website.lower()

        return item

class SaveToDatabasePipeline:

    def __init__(self):
        """
        Initializes database connection and sessionmaker
        Creates tables
        """
        engine = db_connect()
        create_table(engine)
        self.Session = create_session()


    def process_item(self, item, spider):
        session = self.Session()

        # Check for duplicate using url
        existing_url = session.query(ChartaData).filter_by(url=item["url"]).first()
    
        if existing_url:
            spider.logger.info(f"Skipping duplicate item with url: {item['url']}")
        else:
            # Create and save new item
            new_item = ChartaData(**item)
            session.add(new_item)
            session.commit()

        session.close()

        return item
        



        