import pprint
from pygrowi.utils import *

if __name__ == '__main__':
    base_url = 'https://<wiki domain>'
    api_token = 'API Token'
    growi = GrowiAPI(base_url=base_url, api_token=api_token)

    body = '# Test\nThis page is created automatically.'
    res = growi.create_page('/test/hoge', body)
    pprint.pprint(res)

    res = growi.add_attachment_from_file('/test/hoge', "cameraman.png")
    attach_path = res["attachment"]["filePathProxied"]
    pprint.pprint(res)

    # attach_file = ("cameraman.png", open("cameraman.png", "rb").read(), "image/png")
    # res = growi.add_attachment('/test/hoge', attach_file)
    # attach_path = res["attachment"]["filePathProxied"]
    # pprint.pprint(res)

    body = f'# Test\nThis page is created automatically :tada:  \nThis page is created automatically.\n\n![/test/hoge/cameraman.png]({attach_path})'
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
