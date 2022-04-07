from typing import Dict
from urllib import parse

from bs4 import BeautifulSoup
from loguru import logger

from .sessions import session


async def google_search(content: str) -> Dict[str, str]:
    result: Dict[str, str] = {}
    async with session.get(
        f"https://www.google.com/search?q={parse.quote(content)}", timeout=9.9
    ) as resp:
        if resp.status == 200:
            soup = BeautifulSoup(await resp.text(), 'lxml')
            for p in soup.find_all('h3'):
                if p.parent.has_attr('href'):
                    result[p.text] = p.parent.attrs.get('href')
                    logger.info(f"Google | Searching | {result[p.text]}")
            return result

        resp.raise_for_status()
