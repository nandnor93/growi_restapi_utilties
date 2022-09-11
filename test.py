from email.mime import base
import pprint
from utils import *

if __name__ == '__main__':
    base_url = 'https://<wiki domain>'
    api_token = 'API Token'
    growi = GrowiAPI(base_url=base_url, api_token=api_token)

    body = '# Test\nThis page is created automatically.'
    res = growi.create_page('/test/hoge', body)
    pprint.pprint(res)

    body = '# Test\nThis page is created automatically :tada:  \nThis page is created automatically.  \nThis page is created automatically.'
    res = growi.update_page('/test/hoge', body)
    pprint.pprint(res)

    res = growi.rename_page('/test/hoge', '/test/hoge2')
    pprint.pprint(res)

    res = growi.get_tag_list()
    pprint.pprint(res)

    res = growi.get_tags_by_page("/test/hoge2")
    pprint.pprint(res)

    res = growi.get_page_info('/test/hoge2')
    pprint.pprint(res)
