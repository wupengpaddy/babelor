# coding=utf-8
# Copyright 2019 StrTrek Team Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
from xml.etree import ElementTree

ROOT_TAG = 'root'
CODING = 'utf-8'


def dict2json(dt: dict):
    return json.dumps(dt, ensure_ascii=False)


def json2dict(js: str):
    return json.loads(js)


def etree2dict(root: ElementTree.Element):
    dt = {}
    lt = []
    ini_tag = None
    for child in root:
        if ini_tag is None:
            ini_tag = child.tag
        if ini_tag == child.tag:
            if len(child.getchildren()) > 0:
                child_dt = etree2dict(child)
                child_dt.update(child.attrib)
            else:
                child_dt = child.text
            lt.append(child_dt)
        else:
            dt[ini_tag] = lt
            ini_tag = child.tag
            if len(child.getchildren()) > 0:
                child_dt = etree2dict(child)
                child_dt.update(child.attrib)
            else:
                child_dt = child.text
            lt = [child_dt]
    if ini_tag is not None:
        dt[ini_tag] = lt
    return dt


def xml2json(xml: str):
    return dict2json(etree2dict(ElementTree.fromstring(xml.strip())))


def xml2dict(xml: str):
    return etree2dict(ElementTree.fromstring(xml.strip()))


def dict2etree(dt: dict, tag=ROOT_TAG, parent=None):
    if tag == ROOT_TAG:
        root = ElementTree.Element(tag)
    else:
        root = ElementTree.SubElement(parent, tag)
    for key in dt:
        if isinstance(dt[key], list):
            for lt_child in dt[key]:
                if isinstance(lt_child, dict):
                    dict2etree(lt_child, key, root)
                else:
                    child = ElementTree.SubElement(root, key)
                    child.text = lt_child
        else:
            root.attrib[key] = dt[key]
    return root


def json2xml(js: str):
    return ElementTree.tostring(dict2etree(json2dict(js)), encoding=CODING).decode(CODING)


def dict2xml(dt: dict):
    return ElementTree.tostring(dict2etree(dt), encoding=CODING).decode(CODING)