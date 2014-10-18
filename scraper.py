import scraperwiki
import requests
import lxml.html
import json

aps = requests.get("http://api.morph.io/rustyb/sdcc_planning_apps/data.json?key=qOxgzwsMrnI6coobFe4z&query=select%20%22reg_ref%22%20from%20'data'")
aps_json = json.loads(aps.content)

unique_keys = [ 'reg_ref' ]
for i in range(len(aps_json)):
    html = requests.get("http://www.sdublincoco.ie/index.aspx?pageid=144&regref=%s" % str(aps_json[i]['reg_ref'])).content
    print "App: %s" % str(aps_json[i]['reg_ref'])
    dom = lxml.html.fromstring(html)
       
    for entry in dom.cssselect('.details-list'):
            post = {
                'reg_ref': str(aps_json[i]['reg_ref']),
                'date_recieved': entry[0].cssselect('dd')[2].text_content(),
                'last_action': entry[0].cssselect('dd')[3].text_content(),
                'application_type': entry[0].cssselect('dd')[4].text_content(),
                'submission_type': entry[0].cssselect('dd')[5].text_content(),
                'applicant': entry[0].cssselect('dd')[7].text_content(),
                'location': entry[0].cssselect('dd')[8].text_content(),
                'proposed_dev': entry[0].cssselect('dd')[9].text_content(),
                'decision_due': entry[0].cssselect('dd')[10].text_content(),
                'decision_date': entry[1].cssselect('dd')[0].text_content(),
                'decision': entry[1].cssselect('dd')[1].text_content(),
                'final_grant_date': entry[1].cssselect('dd')[2].text_content()
            }
            scraperwiki.sql.save(unique_keys, post)
