# -*- coding: utf-8 -*-
import json
import logging
from typing import List

import requests

from book_utils.book_detail import BookInfo
from settings import Settings


def get_workspace_slug(workspace_name: str) -> str:
    return workspace_name.replace(" ", "-")


def upload_books(book_info_list: List[BookInfo]) -> List[str]:
    try:
        settings = Settings()
        url = f"{settings.AnythingLLM['ApiUrl']}/v1/document/raw-text"

        headers = {
            "Authorization": f"Bearer {settings.AnythingLLM['ApiKey']}",
            "Content-Type": "application/json"
        }

        ret = []
        for book_info in book_info_list:
            data = {
                "textContent": book_info.content(),
                "metadata": {
                    "title": book_info.title(),
                    "docAuthor": book_info.author()
                }
            }

            payload = json.dumps(data, ensure_ascii=False)

            response = requests.post(url, headers=headers, data=payload)
            if response.status_code == 200:
                data = response.json()
                ret.append(data["documents"][0]["location"])
            else:
                continue

        return ret
    except Exception as e:
        logging.error(f"Req: {book_info_list}, Error: {e}")
        return []


def workspace_update_embeddings(file_location_list: List[str]):
    try:
        settings = Settings()
        slug = get_workspace_slug(settings.AnythingLLM['WorkspaceName'])
        url = f"{settings.AnythingLLM['ApiUrl']}/v1/workspace/{slug}/update-embeddings"
        headers = {
            "Authorization": f"Bearer {settings.AnythingLLM['ApiKey']}"
        }

        data = {
            "adds": file_location_list,
        }

        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            logging.info(f"Success: {response.text}")
        else:
            logging.error(f"Req:{url} - {file_location_list}, Error: {response.status_code} - {response.text}")
    except Exception as e:
        logging.error(f"Req: {file_location_list}, Error: {e}")


def do_feed_books(book_info_list: List[BookInfo]):
    file_location_list = upload_books(book_info_list)
    if file_location_list:
        workspace_update_embeddings(file_location_list)
