#!/usr/bin/env python

import json
import html
import os
from sys import argv
from datetime import datetime

convert_datestring_to_datetime_object = lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%fZ')
format_datetime_object_to_evernote_format = lambda x: x.strftime('%Y%m%dT%H%M%SZ')

AUTHOR = 'John'
current_time = format_datetime_object_to_evernote_format(datetime.utcnow())
file = '<?xml version="1.0" encoding="UTF-8"?>\n' \
              '<!DOCTYPE en-export SYSTEM "http://xml.evernote.com/pub/evernote-export3.dtd">\n' \
              '<en-export export-date="{}" application="Evernote" version="Evernote on Linux">'.format(current_time)


def format_string_date(date_string):
    """
    convert date string to a specific isoformat
    e.g. '2020-03-08T20:33:18.044Z' becomes '20200308T203318Z'
    """
    dto = convert_datestring_to_datetime_object(date_string)
    return format_datetime_object_to_evernote_format(dto)


def text_from_html(text):
    """Parse text to html"""
    temp_text = html.escape(text)
    temp_text = temp_text.replace('\n', '<br>')
    return temp_text


def process_items(data, file):
    for key, item in enumerate(data['items']):
        if 'title' in item['content'] and 'text' in item['content']:
            # print('found item')
            title = item['content']['title']
            text = item['content']['text']
            created_ts = format_string_date(item['created_at'])
            updated_ts = format_string_date(item['updated_at'])
            text = text_from_html(text)
            file += '<note><title>{title}</title>' \
                    '<content><![CDATA[<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">' \
                    '<en-note>{text}</en-note>]]></content>' \
                    '<created>{created}</created>' \
                    '<updated>{updated}</updated>' \
                    '<note-attributes><author>{author}</author><source></source>' \
                    '<reminder-order>0</reminder-order></note-attributes>' \
                    '</note>'.format(title=title, text=text, created=created_ts, updated=updated_ts, author=AUTHOR)

    file += '\n</en-export>'
    return file

# TODO: add argparse


if __name__ == "__main__":
    if len(argv) > 1 and os.path.isfile(argv[1]):
        source = argv[1]
        data = json.load(open(source))
        target_file = process_items(data, file)
        with open("notes_2.enex", "w") as text_file:
            text_file.write(target_file)
    else:
        print('You must call this script with a fully qualified and valid file as its only argument')