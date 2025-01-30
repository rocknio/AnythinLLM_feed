# -*- coding: utf-8 -*-

import logging
from pathlib import Path
from typing import List
from urllib.parse import quote

import requests

from settings import Settings


def get_workspace_slug(workspace_name: str) -> str:
    return workspace_name.replace(" ", "-")


def upload_books(txt_file_list: List[str]) -> List[str]:
    try:
        settings = Settings()
        url = f"{settings.AnythingLLM['ApiUrl']}/v1/document/upload"

        files = [
            ('file', (quote(Path(txt_file).name), open(txt_file, 'rb'), 'text/plain'))
            for txt_file in txt_file_list
        ]

        headers = {
            "Authorization": f"Bearer {settings.AnythingLLM['ApiKey']}"
        }

        response = requests.post(url, headers=headers, files=files)
        if response.status_code == 200:
            data = response.json()
            return [item["location"] for item in data["documents"]]
        else:
            logging.error(f"Req:{url} - {txt_file_list}, Error: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        logging.error(f"Req: {txt_file_list}, Error: {e}")
        return []


def workspace_update_embeddings(file_location_list: List[str]):
    try:
        settings = Settings()
        slug = get_workspace_slug(settings.workspace_name)
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


def do_feed_books(txt_file_list: List[str]):
    file_location_list = upload_books(txt_file_list)
    if file_location_list:
        workspace_update_embeddings(file_location_list)
