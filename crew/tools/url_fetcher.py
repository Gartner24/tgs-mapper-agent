import ipaddress
import socket
from typing import Type
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup
from crewai.tools import BaseTool
from loguru import logger
from pydantic import BaseModel, Field

_PRIVATE_NETWORKS = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),
]


def _is_private_host(hostname: str) -> bool:
    try:
        ip = ipaddress.ip_address(socket.gethostbyname(hostname))
        return any(ip in net for net in _PRIVATE_NETWORKS)
    except Exception:
        return True


class UrlFetcherInput(BaseModel):
    content: str = Field(description="URL to fetch and extract readable text from")


class UrlFetcherTool(BaseTool):
    name: str = "url_fetcher"
    description: str = "Fetches a URL and returns its main readable text content, stripping HTML tags."
    args_schema: Type[BaseModel] = UrlFetcherInput

    def _run(self, content: str) -> str:
        url = content.strip()
        parsed = urlparse(url)
        if not parsed.scheme in ("http", "https"):
            return "Error: solo se permiten URLs con esquema http o https."
        if _is_private_host(parsed.hostname or ""):
            return "Error: URL no permitida."
        try:
            with httpx.Client(timeout=15, follow_redirects=True, max_redirects=5) as client:
                response = client.get(url, headers={"User-Agent": "TGSMapperAgent/0.1"})
                response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()
            text = soup.get_text(separator="\n", strip=True)
            text = "\n".join(line for line in text.splitlines() if line.strip())
            logger.info(f"URL fetched: {url} -> {len(text)} chars")
            return text[:12000] if len(text) > 12000 else text
        except httpx.HTTPStatusError as exc:
            logger.error(f"HTTP error fetching {url}: {exc.response.status_code}")
            return f"Error HTTP {exc.response.status_code} al acceder a {url}"
        except Exception as exc:
            logger.error(f"Failed to fetch {url}: {exc}")
            return f"Error al acceder a la URL: {exc}"
