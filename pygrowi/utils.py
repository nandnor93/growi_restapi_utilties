# For Growi v4.2.10

import json
import pathlib
import requests
import mimetypes
from typing import Dict, List, Optional, Tuple, Union


# Growi Rest API向けのError
class GrowiAPIError(Exception):
    def __init__(self, description, status_code=None):
        super().__init__()
        self.description = description
        self.status_code = status_code
    
    def __repr__(self):
        if self.status_code is not None:
            return f'({self.description}, {self.status_code})'
        else:
            return str(self.description)

    def __str__(self):
        if self.status_code is not None:
            return f'({self.description}, {self.status_code})'
        else:
            return str(self.description)


class GrowiAPI(object):
    """Abstraction layer for GROWI API v3"""

    def __init__(self, base_url: str, api_token: str):
        super().__init__()
        self.base_url = base_url
        self.api_token = api_token

    def exist_page(self, page_path: str) -> bool:
        """
        [Experiment] check existance of the spcified page
        """
        try:
            res = self.get_page_info(page_path)
            return res.get("page") is not None
        except GrowiAPIError as e:
            if e.status_code == 404:
                return False
            else:
                raise e

        # if res.status_code == 200:
        #     return json.loads(res.text)['ok']
        # else:
        #     raise GrowiAPIError(res.text)


    def get_page_info(self, page_path: str) -> dict:
        """
        get page information
        """
        req_url = '{}{}'.format(self.base_url, '/_api/v3/page')
        params={'access_token': f'{self.api_token}', 'path': page_path}
        res = requests.get(req_url, params=params)

        if res.status_code == 200:
            return json.loads(res.text)
        else:
            raise GrowiAPIError(res.text, res.status_code)

    def get_page_info_by_id(self, page_id: str) -> dict:
        """
        get page information
        """
        req_url = '{}{}'.format(self.base_url, '/_api/v3/page')
        params={'access_token': f'{self.api_token}', 'pageId': page_id}
        res = requests.get(req_url, params=params)

        if res.status_code == 200:
            return json.loads(res.text)
        else:
            raise GrowiAPIError(res.text, res.status_code)



    def get_page_list_by_page(self, page_path: str, limit:Union[int, None]=None) -> dict:
        """
        get page list under the specified page path
        """
        req_url = '{}{}'.format(self.base_url, '/_api/pages.list')
        limit = 1e10 if limit is None else limit
        queries = {
            'access_token': f'{self.api_token}',
            'path': page_path,
            'limit': limit,
        }
        res = requests.get(req_url, params=queries)
        if res.status_code == 200:
            return json.loads(res.text)['pages']
        else:
            raise GrowiAPIError(res.text, res.status_code)


    def get_page_list_by_user(self, user: str, limit:Union[int, None]=None) -> dict:
        """
        get page list owned by specified user
        """
        req_url = '{}{}'.format(self.base_url, '/_api/pages.list')
        limit = 1e10 if limit is None else limit
        queries = {
            'access_token': f'{self.api_token}',
            'user': user,
            'limit': limit,
        }
        res = requests.get(req_url, params=queries)
        if res.status_code == 200:
            return json.loads(res.text)['pages']
        else:
            raise GrowiAPIError(res.text, res.status_code)


    ##### Create Page #####

    def create_page(self, page_path: str, body: str, grant: int=1) -> dict:
        """
        create page
        """
        req_url = '{}{}'.format(self.base_url, '/_api/v3/pages')
        params = {
            'access_token': f'{self.api_token}',
        }

        payloads = {
            'path': page_path,
            'body': body,
            'grant': grant,
        }

        res = requests.post(req_url, data=payloads, params=params)
        if res.status_code == 201:
            return json.loads(res.text)
        elif res.status_code == 400:
            raise GrowiAPIError(f'Page already exists ({res.text})', res.status_code)
        else:
            raise GrowiAPIError(res.text, res.status_code)


    def update_page(self, page_path: str, body: str, grant: int=1, page_id: Optional[str] = None) -> dict:
        """
        update page
        """
        # ページの存在しない場合get_page_infoはstatus_code=404で失敗し、get_page_infoが例外を投げる
        if not ((page_path is not None and page_id is None) or (page_path is None and page_id is not None)):
            raise GrowiAPIError("Specify either page_path or page_id.")
        if page_path is not None:
            res = self.get_page_info(page_path) # ページの存在しない場合get_page_infoはstatus_code=404で失敗し、get_page_infoが例外を投げる
        else:
            res = self.get_page_info_by_id(page_id)

        page_info = res['page']
        page_id = page_info['_id']
        revision_id = page_info['revision']['_id']

        req_url = '{}{}'.format(self.base_url, '/_api/pages.update')
        params = {
            'access_token': f'{self.api_token}',
        }

        payloads = {
            'path': page_path,
            'body': body,
            'page_id': str(page_id),
            'revision_id': str(revision_id),
            'grant': grant,
        }

        res = requests.post(req_url, data=payloads, params=params)
        if res.status_code == 200:
            return json.loads(res.text)
        else:
            raise GrowiAPIError(res.text, res.status_code)

    def get_page(self, page_path: str, page_id: Optional[str] = None) -> dict:
        """
        update page
        """

        params = {
            'access_token': f'{self.api_token}',
        }

        # ページの存在しない場合get_page_infoはstatus_code=404で失敗し、get_page_infoが例外を投げる
        if not ((page_path is not None and page_id is None) or (page_path is None and page_id is not None)):
            raise GrowiAPIError("Specify either page_path or page_id.")
        if page_path is not None:
            params["path"] = page_path
        else:
            params["pageId"] = page_id

        req_url = '{}{}'.format(self.base_url, '/_api/v3/page')

        res = requests.get(req_url, params=params)
        if res.status_code == 200:
            # print(res.text)
            return json.loads(res.text)
        else:
            raise GrowiAPIError(res.text, res.status_code)



    #### Delete Page #####

    # ページの削除はRestAPIではできない模様
    # 厳密にはログイン状態を維持した状態でRest APIを叩かないと削除できない(Seleniumやbeautifusoupを駆使すれば削除は可能)
    """
    def delete_page(self, page_path: str, recursively: bool=True, completely: bool=True) -> dict:
        page_info = self.get_page_info(page_path)
        page_id = page_info['_id']
        revision_id = page_info['revision']['_id']

        req_url = '{}{}'.format(self.base_url, '/_api/pages.remove')
        params = {
            'access_token': f'{self.api_token}',
        }

        payloads = {
            'page_id': str(page_id),
            'revision_id': str(revision_id),
            'recursively': recursively,
            'completely': completely,
        }

        res = requests.post(req_url, data=payloads, params=params)
        if res.status_code == 200:
            return json.loads(res.text)
        else:
            raise GrowiAPIError(res.text)
    """


    ##### Rename Page #####

    def rename_page(self, src_page_path: str, target_page_path: str, is_remain_meta_data: bool=True, src_page_id: Optional[str] = None) -> dict:
        """
        rename page (change page path)
        """

        if not (src_page_path is not None and src_page_id is None) or (src_page_path is None and src_page_id is not None):
            raise GrowiAPIError("Specify either src_page_path or src_page_id.")
        if src_page_path is not None:
            res = self.get_page_info(src_page_path) # ページの存在しない場合get_page_infoはstatus_code=404で失敗し、get_page_infoが例外を投げる
        else:
            res = self.get_page_info_by_id(src_page_id)
        
        page_info = res['page']
        page_id = page_info['_id']
        revision_id = page_info['revision']['_id']

        req_url = '{}{}'.format(self.base_url, '/_api/v3/pages/rename')
        params = {
            'access_token': f'{self.api_token}',
        }

        # all queries required
        payloads = {
            'pageId': page_id,
            'revisionId': revision_id,
            'path': src_page_path,
            'newPagePath': target_page_path,
            'isRemainMetadata': 'true' if is_remain_meta_data else 'false',
        }

        res = requests.put(req_url, data=payloads, params=params)
        if res.status_code == 200:
            return json.loads(res.text)
        else:
            raise GrowiAPIError(res.text, res.status_code)


    ##### Attach files #####

    def add_attachment(self, page_path: str, data: Tuple[str, bytes, str], attach_path: Optional[str] = None, page_id: Optional[str] = None) -> dict:
        """
        Attach a file to a page.
        `data` must be a tuple of (file name, file data, MIME type).
        To use the attached file in a page, refer to `result['attachment']['filePathProxied']`.
        If using the page id, leave page_path None.
        """
        
        # APIリファレンスにある pathの効力がないように見える。また、["url"]返り値もない。

        if not ((page_path is not None and page_id is None) or (page_path is None and page_id is not None)):
            raise GrowiAPIError("Specify either page_path or page_id.")
        if page_path is not None:
            res = self.get_page_info(page_path) # ページの存在しない場合get_page_infoはstatus_code=404で失敗し、get_page_infoが例外を投げる
        else:
            res = self.get_page_info_by_id(page_id)

        page_info = res['page']
        page_id = page_info['_id']

        req_url = '{}{}'.format(self.base_url, '/_api/attachments.add')
        params = {
            'access_token': f'{self.api_token}',
        }

        payloads = {
            'page_id': str(page_id),
        }
        files = {
            'file': data,
        }
        if attach_path is not None:
            payloads['path'] = attach_path

        res = requests.post(req_url, data=payloads, params=params, files=files)
        if res.status_code == 200:
            res_json = json.loads(res.text)
            if res_json['ok']:
                return res_json
            else:
                raise GrowiAPIError(f"Cannot attach the file ({res.text})", res.status_code)
        else:
            raise GrowiAPIError(res.text, res.status_code)

    def add_attachment_from_file(self, page_path: str, file: Union[str, pathlib.Path], file_name: Optional[str] = None, attach_path: Optional[str] = None, page_id: Optional[str] = None) -> dict:
        """
        Attach a file to a page.
        file must be a file path or a pathlib.Path-like object.
        To use the attached file in a page, refer to `result['attachment']['filePathProxied']`.
        """

        file = pathlib.Path(file)
        if file_name is None:
            file_name = file.name
        file_data = (
            file_name,
            file.open('rb').read(),
            mimetypes.guess_type(file)[0] or 'application/octet-stream'
        )
        return self.add_attachment(page_path, file_data, attach_path, page_id=page_id)
    

    ##### Get Tag #####

    def get_tag_list(self) -> Dict:
        """
        get tag list
        """
        req_url = '{}{}'.format(self.base_url, '/_api/tags.list')
        params = {
            'access_token': f'{self.api_token}',
        }

        res = requests.get(req_url, params=params)
        if res.status_code == 200:
            return json.loads(res.text)['data']
        else:
            raise GrowiAPIError(res.text, res.status_code)

    def get_tags_by_page(self, page_path: str) -> List[str]:
        """
        get tags annotated on specified pate
        """
        res = self.get_page_info(page_path)
        
        page_id = res['page']['_id']

        req_url = '{}{}'.format(self.base_url, '/_api/pages.getPageTag')
        params = {
            'access_token': f'{self.api_token}',
            'pageId': page_id
        }

        res = requests.get(req_url, params=params)
        if res.status_code == 200:
            return json.loads(res.text)['tags']
        else:
            raise GrowiAPIError(res.text, res.status_code)
