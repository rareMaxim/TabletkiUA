from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

# --------- Simple models ---------


@dataclass(slots=True)
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

# --------- Search hints ---------


@dataclass(slots=True)
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


@dataclass(slots=True)
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


@dataclass(slots=True)
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

# --------- Product card ---------


@dataclass(slots=True)
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


@dataclass(slots=True)
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


@dataclass(slots=True)
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


@dataclass(slots=True)
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


@dataclass(slots=True)
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


@dataclass(slots=True)
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


@dataclass(slots=True)
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


@dataclass(slots=True)
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


@dataclass(slots=True)
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


@dataclass(slots=True)
class DeliveryDataInfo:
    priceMin: Optional[float]

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "DeliveryDataInfo":
        return DeliveryDataInfo(priceMin=d.get("priceMin"))


@dataclass(slots=True)
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


@dataclass(slots=True)
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


@dataclass(slots=True)
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

    # keep full payload
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
