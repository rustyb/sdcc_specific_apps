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
    dds = dom.cssselect('dl.details-list dd')
       
    post = {
        'reg_ref': str(aps_json[i]['reg_ref']),
        'date_recieved': dds[2].text_content(),
        'last_action': dds[3].text_content(),
        'application_type': dds[4].text_content(),
        'submission_type': dds[5].text_content(),
        'applicant': dds[7].text_content(),
        'location': dds[8].text_content(),
        'proposed_dev': dds[9].text_content(),
        'decision_due': dds[10].text_content(),
        'decision_date': dds[11].text_content(),
        'decision': dds[12].text_content(),
        'final_grant_date': dds[13].text_content()
    }
    scraperwiki.sql.save(unique_keys, post)
