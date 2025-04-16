from ..types import URL, Client, AsyncClient, Args, Kwargs

__all__: list[str] = ["get_client", "get_async_client"]

def get_client(base_url: URL, *args: Args, **kwargs: Kwargs) -> Client:
    return Client(base_url=base_url)

def get_async_client(base_url: URL, *args: Args, **kwargs: Kwargs) -> AsyncClient:
    return AsyncClient(base_url=base_url)
