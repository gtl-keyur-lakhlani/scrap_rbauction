import scrapy
import requests, json

from rbauction.items import RbauctionItem
from scrapy_splash import SplashRequest


class RbAuctionSpider(scrapy.Spider):
    name = "rbauction"
    http_user = 'a77f8d9112a14cd6bfc4e3734261b2aa'
    # start_urls = ["https://www.rbauction.com/2014-CATERPILLAR--LGP-CRAWLER-TRACTORCTR?invId=10782064&id=ci&auction=EDMONTON-AB-2018226"]
    start_urls = ["https://www.rbauction.com/"]
    global url
    url = "https://www.rbauction.com"

    def parse(self, response):
        link = response.xpath("//li[contains(@class, 'cc-bottom-margin')]/a//@href").extract()
        page_id_list = []
        for page_id in link:
            page_id = page_id.split('=')[1]
            page_id_list.append(page_id)
        # one_page = url + page
        k = 0
        while k != len(page_id_list):
            path = requests.get(
                "https://www.rbauction.com/rba-msapi/search?keywords=&searchParams=%7B%22category%22%3A%22"+str(page_id_list[k])+"%22%7D&page=0&maxCount=48&trackingType=2&withResults=true&withFacets=true&withBreadcrumbs=true&catalog=ci&locale=en_US")
            data = path.json()
            for m in range(0, 48):
                details_url = data["response"]["results"][m]["url"]
                thumbnails_url = data["response"]["results"][m]["img"]
                equipment_id = data["response"]["results"][m]["equipmentId"]
                equipment_id = equipment_id.split('_')[0]
                base_url = "https://www.rbauction.com/rba-msapi/search/breadcrumb?catalog=ci&locale=en_US&equipmentId="
                api_url = base_url + str(equipment_id)
                path_2 = requests.get(api_url)
                data_2 = path_2.json()
                category = data_2["breadcrumb"][0]["name"]
                sub_category = data_2["breadcrumb"][1]["name"]
                thumbnail_url = url + thumbnails_url
                listing_url = url + details_url
                yield scrapy.Request(listing_url, callback=self.parse_dir_contents, meta={'thumbnail_url': thumbnail_url,
                                                                                          'listing_url': listing_url,
                                                                                          'category': category,
                                                                                          'sub_category': sub_category})
            k = k + 1

    def parse_dir_contents(self, response):
        item = RbauctionItem()
        item['Category'] = response.meta['category']
        item['Sub_Category'] = response.meta['sub_category']
        item['Thumbnail_URL'] = response.meta['thumbnail_url']
        item['Listing_URL'] = response.meta['listing_url']
        listing_title = response.xpath(".//*[@id='page-title']/h1/text()").extract_first()
        item['Listing_Title'] = listing_title.strip()
        image_list = []
        images = response.xpath(
            "//div[contains(@class , 'rba-carousel-slides rba-media-viewer-play-small')]//@data-loadsrc").extract()
        for img in images:
            image = url + img
            image_list.append(image)
        item['Images_URL'] = image_list
        label_data = response.xpath(
            "//div[contains(@class, 'rba-content-column rba-content-column-w-40')]/div[contains(@class, 'value-label')]/text()").extract()

        value = response.xpath(
            "//div[contains(@class, 'rba-content-column rba-content-column-w-60')]/div[contains(@class, 'static-value')]/text()").extract()

        parameter_array = ['In Yard', 'Year', 'Model', 'Make', 'Model Modifier', 'Asset Type', 'Manufacturer',
                           'Hrs/Mil/kms', 'Serial Number or VIN', 'Serial No.', 'In yard', 'Meter reads (unverified)']

        table_param = []

        for detail in label_data:
            detail = detail.replace(':', '')
            table_param.append(detail)

        i = 0
        while i != len(table_param):
            for param_value in parameter_array:
                if table_param[i] == param_value:
                    if table_param[i] == 'Asset Type':
                        item['AssetType'] = value[i]
                    elif table_param[i] == 'Hrs/Mil/kms' or 'Meter' in table_param[i]:
                        item['Hours'] = value[i]
                    elif table_param[i] == 'In Yard' or table_param[i] == 'In yard':
                        item['InYard'] = value[i]
                    elif table_param[i] == 'Model Modifier':
                        item['ModelModifier'] = value[i]
                    elif table_param[i] == 'Manufacturer':
                        item['Make'] = value[i]
                    elif 'Serial' in table_param[i]:
                        item['SerialNumber'] = value[i]
                    else:
                        item[param_value] = value[i]
            i = i + 1
        yield item
