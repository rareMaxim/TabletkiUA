from tabletkiua import TabletkiUA, DeviceProfile

ident = DeviceProfile.generate(lang="uk")
with TabletkiUA(app_api_token="", identity=ident) as client:
    # 1) location
    # also stores identity.location_header
    loc = client.location_by_ip()
    print(loc.name, loc.url)

    # 2) search by barcode or name
    hints = client.search_hints_v2(term="4820142437368")
    for grp in hints.group:
        for item in grp.searchItems:
            print(item.name, item.code)

    # 3) product card
    card = client.product_card(
        name="Акварінол з хлоргексидином для дітей спрей назальний по 70 мл у флак.",
        goods_int_code=1025098,
    )
    print(card.goodsName, card.priceMin, card.priceMax)
