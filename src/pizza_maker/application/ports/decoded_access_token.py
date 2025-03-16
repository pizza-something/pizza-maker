from abc import ABC, abstractmethod

from pizza_maker.entities.access.access_token import AccessToken


type DecodedAccessToken = AccessToken


class DecodedAccessTokenWhen[EncodedAccessTokenT](ABC):
    @abstractmethod
    async def __call__(
        self, *, encoded_access_token: EncodedAccessTokenT
    ) -> AccessToken | None: ...
