import requests
import urllib.parse
import config

icscontent = requests.get(config.CALENDAR_URL, auth=(config.USER, config.PASSWORD)).text

with open(config.TARGET_ALL, 'w') as alleics:
    alleics.write(icscontent)

def prep_links(event):
    summary = ''
    desc = False
    for line in event:
        if line.startswith('SUMMARY'):
            summary = line[8:]
        if line.startswith('DESCRIPTION'):
            #check for description field
            desc = True
    for line in event:
        if line.startswith('DESCRIPTION'):
            desc = True
            url = line[12:]
            if url:
                line = 'DESCRIPTION:<a href="{}">{}</a>'.format(url, summary)
            else:
                line = 'DESCRIPTION:<b>{}</b>'.format(summary)
        if line.startswith('SUMMARY') and not desc:
            #insert description
            yield 'DESCRIPTION:<b>{}</b>'.format(summary)
        yield line

public_ics = []
in_event = False
events = []
current_event = []
current_is_public = False
current_summary = ''

for line in icscontent.splitlines():
    line = line.strip()
    if line.startswith('BEGIN:VEVENT'):
        in_event = True
    if in_event:
        current_event.append(line)
    else:
        public_ics.append(line)
    if line.startswith('CLASS:PUBLIC'):
        current_is_public = True
    if line.startswith('END:VEVENT'):
        in_event = False
    if current_event and not in_event and current_is_public:
        current_event = prep_links(current_event)
        public_ics.append('\n'.join(current_event))
        current_event = []
        current_is_public = False
    elif current_event and not in_event and not current_is_public:
        current_event = []

with open(config.TARGET_PUBLIC, 'w') as pubics:
    pubics.write('\n'.join(public_ics))
