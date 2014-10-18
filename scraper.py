import scraperwiki
import requests
import lxml.html
import json

aps = requests.get("http://api.morph.io/rustyb/sdcc_planning_apps/data.json?key=qOxgzwsMrnI6coobFe4z&query=select%20%22reg_ref%22%20from%20'data'")
aps_json = json.loads(aps.content)

unique_keys = [ 'reg_ref' ]
for i in range(len(aps_json)):
    html = requests.get("http://www.sdublincoco.ie/index.aspx?pageid=144&regref=%s" % str(aps_json[i])).content
    print "App: %s" % i
    dom = lxml.html.fromstring(html)
       
    for entry in dom.cssselect('.details-list'):
            post = {
                'reg_ref': str(aps_json[i]),
                'date_recieved': entry.cssselect('dd')[2].text_content(),
                'last_action': entry.cssselect('dd')[3].text_content(),
                'application_type': entry.cssselect('dd')[4].text_content(),
                'submission_type': entry.cssselect('dd')[5].text_content(),
                'applicant': entry.cssselect('dd')[7].text_content(),
                'location': entry.cssselect('dd')[8].text_content(),
                'proposed_dev': entry.cssselect('dd')[9].text_content(),
                'decision_due': entry.cssselect('dd')[10].text_content()
            }
            scraperwiki.sql.save(unique_keys, post)
