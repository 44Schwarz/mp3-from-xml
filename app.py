#!/usr/bin/env python3
import os
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError
from datetime import datetime
from urllib.request import urlretrieve
from urllib.parse import urlparse

SAVE_DIR = '/tmp/podcasts'
XML_FILE_PATH = 'http://rss.dw.com/xml/DKpodcast_dwn1_en'


def parse_xml(root):
    for l1 in root:
        for l2 in l1:
            if not l2.tag == 'item':
                continue
            for l3 in l2:
                if not l3.tag == 'enclosure':
                    continue
                url = l3.attrib.get('url')
                filename = retrieve_filename(url)
                if os.path.splitext(filename)[-1] == '.mp3' or l3.attrib.get('type') == 'audio/mpeg':
                    filepath = os.path.join(SAVE_DIR, filename or datetime.now().isoformat())
                    if os.path.exists(filepath):
                        print("File {} already exists".format(filename))
                        continue
                    urlretrieve(url, filepath)


def retrieve_filename(url):
    path = urlparse(url).path
    return os.path.basename(path)


if __name__ == '__main__':
    xml_file = urlretrieve(XML_FILE_PATH, os.path.join('/tmp', retrieve_filename(XML_FILE_PATH) + '.xml'))[0]
    try:
        tree = ET.parse(xml_file)
    except FileNotFoundError:
        print("File can't be downloaded")
        exit(1)
    except ParseError:
        print("Incorrect file. Are you sure it is in xml format?")
        exit(1)

    os.makedirs(SAVE_DIR, exist_ok=True)

    parse_xml(tree.getroot())
