# tabletkiua.py
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

import uuid
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


DEFAULT_UA = (
    "Dalvik/2.1.0 (Linux; U; Android 16; Pixel 8 Pro Build/BP41.250822.010)"
)


@dataclass
class DeviceProfile:
    """Опис мобільного профілю, який формує обов'язкові заголовки."""
    adid: str
    device_id: str
    user_id: str
    user_agent: str = DEFAULT_UA
    device_os: str = "android"
    device_os_version: str = "36"
    app_version: str = "4.1.674"
    lang: str = "uk"
    is_new_user: bool = True
    location_header: str = ""

    @classmethod
    def generate(
        cls,
        *,
        user_agent: str = DEFAULT_UA,
        device_os: str = "android",
        device_os_version: str = "36",
        app_version: str = "4.1.674",
        lang: str = "uk",
        is_new_user: bool = True,
        location_header: str = "",
        adid: Optional[str] = None,
        device_id: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> "DeviceProfile":
        return cls(
            adid=adid or str(uuid.uuid4()),
            device_id=device_id or str(uuid.uuid4()),
            user_id=user_id or str(uuid.uuid4()),
            user_agent=user_agent,
            device_os=device_os,
            device_os_version=device_os_version,
            app_version=app_version,
            lang=lang,
            is_new_user=is_new_user,
            location_header=location_header,
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DeviceProfile":
        return cls(**data)

    def headers(self, app_api_token: str) -> Dict[str, str]:
        """Сформувати базові заголовки для всіх запитів."""
        return {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "adid": self.adid,
            "AppApiToken": app_api_token,
            "appVersion": self.app_version,
            "deviceID": self.device_id,
            "deviceOS": self.device_os,
            "deviceOSversion": self.device_os_version,
            "isNewUser": "1" if self.is_new_user else "0",
            "Lang": self.lang,
            "Location": self.location_header,
            "User-Agent": self.user_agent,
            "UserID": self.user_id,

        }


@dataclass
class Location:
    areaId: str
    id: str
    name: str
    nameRu: Optional[str]
    nameUk: Optional[str]
    name2: Optional[str]
    name3: Optional[str]
    name4: Optional[str]
    northEastLat: float
    northEastLng: float
    southWestLat: float
    southWestLng: float
    url: str
    urlRu: Optional[str]
    urlUk: Optional[str]
    index: bool
    priority: int

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Location":
        return Location(
            areaId=d.get("areaId", ""),
            id=d.get("id", ""),
            name=d.get("name", ""),
            nameRu=d.get("nameRu"),
            nameUk=d.get("nameUk"),
            name2=d.get("name2"),
            name3=d.get("name3"),
            name4=d.get("name4"),
            northEastLat=float(d.get("northEastLat", 0.0)),
            northEastLng=float(d.get("northEastLng", 0.0)),
            southWestLat=float(d.get("southWestLat", 0.0)),
            southWestLng=float(d.get("southWestLng", 0.0)),
            url=d.get("url", ""),
            urlRu=d.get("urlRu"),
            urlUk=d.get("urlUk"),
            index=bool(d.get("index", False)),
            priority=int(d.get("priority", 0)),
        )


@dataclass
class SearchItem:
    image: Optional[str]
    icon: Optional[str]
    description: Optional[str]
    url: Optional[str]
    canBeDelivered: Optional[bool]
    utmData: Optional[Any]
    highlight: Optional[Any]
    name: Optional[str]
    screenViewType: Optional[str]
    code: Optional[str]

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "SearchItem":
        return SearchItem(
            image=d.get("image"),
            icon=d.get("icon"),
            description=d.get("description"),
            url=d.get("url"),
            canBeDelivered=d.get("canBeDelivered"),
            utmData=d.get("utmData"),
            highlight=d.get("highlight"),
            name=d.get("name"),
            screenViewType=d.get("screenViewType"),
            code=d.get("code"),
        )


@dataclass
class SearchGroup:
    name: str
    searchItems: List[SearchItem]

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "SearchGroup":
        return SearchGroup(
            name=d.get("name", ""),
            searchItems=[SearchItem.from_dict(x)
                         for x in d.get("searchItems", [])],
        )


@dataclass
class SearchHintsResponse:
    tagGroup: Optional[Any]
    group: List[SearchGroup]
    canBeDelivered: Optional[bool]
    code: int
    description: Optional[str]

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "SearchHintsResponse":
        return SearchHintsResponse(
            tagGroup=d.get("tagGroup"),
            group=[SearchGroup.from_dict(g) for g in d.get("group", [])],
            canBeDelivered=d.get("canBeDelivered"),
            code=int(d.get("code", 0)),
            description=d.get("description"),
        )
# --- ДОДАЙ до tabletkiua.py ---


# ======= Models for Product Card =======

@dataclass
class ImageAsset:
    id: Optional[str]
    type: Optional[str]
    url: Optional[str]
    bigUrl: Optional[str]
    previewUrl: Optional[str]
    order: Optional[int]
    goodsname: Optional[str]

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ImageAsset":
        return ImageAsset(
            id=d.get("id") or d.get("Id"),
            type=d.get("type"),
            url=d.get("url"),
            bigUrl=d.get("bigUrl"),
            previewUrl=d.get("previewUrl"),
            order=d.get("order"),
            goodsname=d.get("goodsname"),
        )


@dataclass
class CharacteristicValue:
    id: Optional[str]
    name: Optional[str]
    code: Optional[str]
    screenViewType: Optional[str]
    image: Optional[str]
    urlName: Optional[str]

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "CharacteristicValue":
        return CharacteristicValue(
            id=d.get("id"),
            name=d.get("name"),
            code=d.get("code"),
            screenViewType=d.get("screenViewType"),
            image=d.get("image"),
            urlName=d.get("urlName"),
        )


@dataclass
class Characteristic:
    id: str
    name: str
    values: List[CharacteristicValue]
    order: Optional[int]

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Characteristic":
        return Characteristic(
            id=str(d.get("id", "")),
            name=d.get("name", ""),
            values=[CharacteristicValue.from_dict(
                v) for v in d.get("values", [])],
            order=d.get("order"),
        )


@dataclass
class HtmlSection:
    id: str
    title: str
    anchor: Optional[str]
    order: Optional[int]
    html: str

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "HtmlSection":
        return HtmlSection(
            id=str(d.get("id", "")),
            title=d.get("title", ""),
            anchor=d.get("anchor"),
            order=d.get("order"),
            html=d.get("html", ""),
        )


@dataclass
class FaqItem:
    title: str
    text: str
    priority: Optional[int]
    anchor: Optional[str]

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "FaqItem":
        return FaqItem(
            title=d.get("title", ""),
            text=d.get("text", ""),
            priority=d.get("priority"),
            anchor=d.get("anchor"),
        )


@dataclass
class FaqGroup:
    title: str
    priority: Optional[int]
    items: List[FaqItem]

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "FaqGroup":
        return FaqGroup(
            title=d.get("title", ""),
            priority=d.get("priority"),
            items=[FaqItem.from_dict(x) for x in d.get("items", [])],
        )


@dataclass
class DosageInfo:
    inputType: Optional[int]
    count: Optional[float]
    nameRu: Optional[str]
    nameUk: Optional[str]
    titleRu: Optional[str]
    titleUk: Optional[str]

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "DosageInfo":
        return DosageInfo(
            inputType=d.get("inputType"),
            count=d.get("count"),
            nameRu=d.get("nameRu"),
            nameUk=d.get("nameUk"),
            titleRu=d.get("titleRu"),
            titleUk=d.get("titleUk"),
        )


@dataclass
class AboutProduction:
    producersName: Optional[str]
    code: Optional[str]
    logo: Optional[str]
    factoriesInfo: Optional[Any]
    descriptions: Optional[Any]

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AboutProduction":
        return AboutProduction(
            producersName=d.get("producersName"),
            code=d.get("code"),
            logo=d.get("logo"),
            factoriesInfo=d.get("factoriesInfo"),
            descriptions=d.get("descriptions"),
        )


@dataclass
class WaitlistInfo:
    goodsIntCode: Optional[int]
    showButton: Optional[bool]
    canAdd: Optional[bool]
    description: Optional[str]

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "WaitlistInfo":
        return WaitlistInfo(
            goodsIntCode=d.get("goodsIntCode"),
            showButton=d.get("showButton"),
            canAdd=d.get("canAdd"),
            description=d.get("description"),
        )


@dataclass
class DeliveryDataInfo:
    priceMin: Optional[float]

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "DeliveryDataInfo":
        return DeliveryDataInfo(priceMin=d.get("priceMin"))


@dataclass
class HintData:
    waitlistInfo: Optional[WaitlistInfo]
    deliveryDataInfo: Optional[DeliveryDataInfo]

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "HintData":
        if not d:
            return HintData(None, None)
        return HintData(
            waitlistInfo=WaitlistInfo.from_dict(d.get("waitlistInfo", {}))
            if d.get("waitlistInfo") is not None
            else None,
            deliveryDataInfo=DeliveryDataInfo.from_dict(
                d.get("deliveryDataInfo", {}))
            if d.get("deliveryDataInfo") is not None
            else None,
        )


@dataclass
class DFP:
    GOODS: Optional[str]
    CLASSGOODS: Optional[str]
    CLASSGOODS2: Optional[str]
    ATC: List[str]
    ATCFull: List[str]
    URL: Optional[str]
    CATEGORIES: List[str]
    TownId: Optional[str]

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "DFP":
        return DFP(
            GOODS=d.get("GOODS"),
            CLASSGOODS=d.get("CLASSGOODS"),
            CLASSGOODS2=d.get("CLASSGOODS2"),
            ATC=d.get("ATC", []) or [],
            ATCFull=d.get("ATCFull", []) or [],
            URL=d.get("URL"),
            CATEGORIES=[str(x) for x in d.get("CATEGORIES", [])],
            TownId=d.get("TownId"),
        )


@dataclass
class ProductCard:
    # core ids/names
    goodsName: Optional[str]
    goodsId: Optional[str]
    goodsIntCode: Optional[str]
    tradeName: Optional[str]
    tradenameLink: Optional[str]
    tradeNameIntCode: Optional[str]
    topTradeNameIntCode: Optional[str]

    # booleans / flags
    isDrugs: Optional[bool]
    isTradeName: Optional[bool]
    isSingleSku: Optional[bool]
    canBeDelivered: Optional[bool]
    hasInstruction: Optional[bool]
    hasFaq: Optional[bool]

    # prices/urls
    priceMin: Optional[float]
    priceMax: Optional[float]
    shareUrl: Optional[str]
    canonicalUrl: Optional[str]
    analyticsUrl: Optional[str]

    # collections
    images: List[ImageAsset]
    characteristics: List[Characteristic]
    descriptionByParts: List[HtmlSection]
    instructionByParts: List[HtmlSection]
    faqs: List[FaqGroup]

    # misc
    aboutProduction: Optional[AboutProduction]
    dosageInfo: Optional[DosageInfo]
    hintData: Optional[HintData]
    dfp: Optional[DFP]
    priceHistory: Dict[str, float]

    # keep full payload if потрібно
    raw: Dict[str, Any]

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ProductCard":
        return ProductCard(
            goodsName=d.get("goodsName"),
            goodsId=d.get("goodsId"),
            goodsIntCode=str(d.get("goodsIntCode")) if d.get(
                "goodsIntCode") is not None else None,
            tradeName=d.get("tradeName"),
            tradenameLink=d.get("tradenameLink"),
            tradeNameIntCode=d.get("tradeNameIntCode"),
            topTradeNameIntCode=d.get("topTradeNameIntCode"),
            isDrugs=d.get("isDrugs"),
            isTradeName=d.get("isTradeName"),
            isSingleSku=d.get("isSingleSku"),
            canBeDelivered=d.get("canBeDelivered"),
            hasInstruction=d.get("hasInstruction"),
            hasFaq=d.get("hasFaq"),
            priceMin=d.get("priceMin"),
            priceMax=d.get("priceMax"),
            shareUrl=d.get("shareUrl"),
            canonicalUrl=d.get("canonicalUrl"),
            analyticsUrl=d.get("analyticsUrl"),
            images=[ImageAsset.from_dict(x) for x in d.get("images", [])],
            characteristics=[Characteristic.from_dict(
                x) for x in d.get("characteristics", [])],
            descriptionByParts=[HtmlSection.from_dict(
                x) for x in d.get("descriptionByParts", [])],
            instructionByParts=[HtmlSection.from_dict(
                x) for x in d.get("instructionByParts", [])],
            faqs=[FaqGroup.from_dict(x) for x in d.get("faqs", [])],
            aboutProduction=AboutProduction.from_dict(
                d.get("aboutProduction", {})) if d.get("aboutProduction") else None,
            dosageInfo=DosageInfo.from_dict(
                d.get("dosageInfo", {})) if d.get("dosageInfo") else None,
            hintData=HintData.from_dict(
                d.get("hintData", {})) if d.get("hintData") else None,
            dfp=DFP.from_dict(d.get("dfp", {})) if d.get("dfp") else None,
            priceHistory={k: float(v) for k, v in (
                d.get("priceHistory") or {}).items()},
            raw=d,
        )


class TabletkiUA:
    """
    Клієнт до API app.tabletki.ua із сесією, ретраями та інкапсульованою ідентифікацією.
    """

    def __init__(
        self,
        app_api_token: str,
        *,
        identity: Optional[DeviceProfile] = None,
        base_url: str = "https://app.tabletki.ua/api/app/v1",
        timeout: int = 15,
        retries: int = 3,
        backoff_factor: float = 0.5,
        status_forcelist: tuple[int, ...] = (429, 500, 502, 503, 504),
        cookies: Optional[Dict[str, str]] = None,
        proxies: Optional[Dict[str, str]] = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.app_api_token = app_api_token
        self.identity = identity or DeviceProfile.generate()
        self.timeout = timeout

        # HTTP сесія з ретраями
        self.session = requests.Session()
        retry = Retry(
            total=retries,
            connect=retries,
            read=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
            allowed_methods={"GET", "POST", "PUT", "PATCH", "DELETE"},
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

        if proxies:
            self.session.proxies.update(proxies)
        if cookies:
            self.session.cookies.update(cookies)

    # --- низькорівневий запит ---
    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        url = f"{self.base_url}/{path.lstrip('/')}"
        hdrs = self.identity.headers(self.app_api_token)
        if headers:
            hdrs.update(headers)

        resp = self.session.request(
            method=method.upper(),
            url=url,
            params=params,
            json=json,
            headers=hdrs,
            timeout=self.timeout,
            verify=False,
        )
        try:
            resp.raise_for_status()
        except requests.HTTPError as e:
            # Покажемо тіло відповіді для зручного дебагу
            try:
                detail = resp.json()
            except Exception:
                detail = resp.text[:500]
            raise requests.HTTPError(f"{e} | detail={detail}") from e

        return resp.json()

    # --- Перший публічний метод ---
    def location_by_ip(self, *, store: bool = True) -> Location:
        """
        GET /Locations/locationByIp — визначити локацію за IP.
        Якщо store=True (за замовчуванням) — зберігає self.identity.location_header = loc.id
        """
        data = self._request("GET", "Locations/locationByIp")
        loc = Location.from_dict(data)
        if store:
            self.identity.location_header = loc.id  # <— використовуємо поле 'id'
        return loc

    def search_hints_v2(
        self,
        term: str,
        *,
        transliterate: int | bool = 0,
        type: str = "DEFAULT",
        # можна й не передавати — візьмемо з identity
        location: Optional[str] = None,
    ) -> SearchHintsResponse:
        """
        POST /Search/searchHintsV2
        Тіло: {"term": "...", "transliterate": 0|1, "type": "DEFAULT"}
        Заголовок Location: параметр `location` або self.identity.location_header (якщо є).
        """
        payload = {
            "term": term,
            "transliterate": 1 if str(transliterate) in {"1", "True", "true"} else 0,
            "type": type,
        }
        # Перевага явному параметру, інакше — використаємо збережену локацію
        location_to_use = location or self.identity.location_header
        extra_headers = {
            "Location": location_to_use} if location_to_use else None

        data = self._request(
            "POST",
            "Search/searchHintsV2",
            json=payload,
            headers=extra_headers,
        )
        return SearchHintsResponse.from_dict(data)

    def product_card(
        self,
        *,
        name: str,
        goods_int_code: str | int,
        with_content_plus: bool = True,
    ) -> ProductCard:
        """
        GET /ProductCard/card?name=...&id=...&withContentPlus=true
        Повертає картку товару з характеристиками, фото, секціями HTML тощо.
        """
        params = {
            "name": name,
            "id": str(goods_int_code),
            "withContentPlus": "true" if with_content_plus else "false",
        }
        data = self._request("GET", "ProductCard/card", params=params)
        return ProductCard.from_dict(data)


# --- приклад використання ---
if __name__ == "__main__":
    ident = DeviceProfile.generate(lang="uk")
    client = TabletkiUA(
        app_api_token="08965AEC-A4BC-42E6-A874-0FAB51376745",
        identity=ident,
    )
    loc = client.location_by_ip()
    print(loc.name, loc.url)
    res = client.search_hints_v2(term="4820142437368")
    print(res.code, res.group[0].searchItems[0].name)

    card = client.product_card(
        name=res.group[0].searchItems[0].name,
        goods_int_code=res.group[0].searchItems[0].code,
    )
    print(card.goodsName, card.priceMin, "грн", "Зображень:", len(card.images))
