from lxml import html
import requests
#import threading
from multiprocessing import Process
#(prodid, brand, price, description, color, styleid, img)

def threadWorker(category, filename, writefilename):
    #itemname = "SALVATORE FERRAGAMO weave knit scarf"
    with open(filename, "r") as fl:
        itemlist = fl.read().split("\n")
    finalitemlist = []
    for itemname in itemlist:
        listlink = "https://www.farfetch.com/hk/shopping/"+category+"/search/items.aspx?q="+itemname+"&ffref=lp_srs"

        pagebody = html.fromstring(requests.get(listlink).text)

        firstshit = pagebody.xpath("//div[@class='listing-item-image']/a/@href")[0]
        firstshit = "https://www.farfetch.com" + firstshit

        resultbody = html.fromstring(requests.get(firstshit).text)
        try:
            #get them attributes
            brand = str(resultbody.xpath("//div[@class='detail-product pt10-sm pt10-xs']//a[@itemprop='brand']")[0].text)
            price = str(resultbody.xpath("//div[@class='detail-product pt10-sm pt10-xs']//div[@class='pdp-price']//span[@class='listing-price js-price']")[0].text)
            description = str(resultbody.xpath("//div[@class='accordion accordion-xl product-detail baseline col12 alpha omega mb20']//p[@itemprop='description']")[0].text.strip())
            color = str(resultbody.xpath("//div[@class='accordion accordion-xl product-detail baseline col12 alpha omega mb20']//span[@itemprop='color']")[0].text.strip())
            styleid = str(resultbody.xpath("//div[@class='accordion accordion-xl product-detail baseline col12 alpha omega mb20']//p[@class='designer-style-id']/span")[0].text)
            prodid = str(resultbody.xpath("//div[@class='accordion accordion-xl product-detail baseline col12 alpha omega mb20']//p[@class='item-id']/span[@itemprop='sku']")[0].text)
            imglink = str(resultbody.xpath("//div[@class='sliderProductModule']//img[@class='noscriptImg__slide']/@src")[0])
            #designer-style-id
            finalitemlist.append((prodid, brand, price, description, color, styleid, imglink))
            print("Done with ", (prodid, brand, price, description, color, styleid, imglink))
        except:
            print("error")
            pass
    with open(writefilename, "w+") as wf:
        wf.write("\n".join(["%s,%s,%s,%s,%s,%s" % x for x in finalitemlist]))

"""
cfwtuples = [
    {"category": "men", "filename":"data/malefashioncsv.csv", "writefilename":"malefashionout.csv"},
    {"category":"women", "filename":"data/femalefashioncsv.csv", "writefilename":"femalefashionout.csv"}
]

"""
cfwtuples = [
    ("kids", "data/kidsfashioncsv.csv", "kidsfashionout.csv"),
    ("women", "data/luxurybagscsv.csv", "luxurybagsout.csv")
#    {"category": "men", "filename": "data/accessoriescsv.csv", "writefilename": "accessoriesmenout.csv"},
#    {"category": "women", "filename": "data/accessoriescsv.csv", "writefilename": "accessorieswomenout.csv"}
]

#threading.Thread(target=threadWorker, kwargs=cfwtuples[0]).start()
#threading.Thread(target=threadWorker, kwargs=cfwtuples[1]).start()

for t in cfwtuples:
    print("Started thread!!!!")
    Process(target=threadWorker, args=t).start()



