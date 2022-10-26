# -*- coding: utf-8 -*-

# from xml.etree import ElementTree as ET
import json
import copy
import random
import alp.core as core


class Item(object):
    def __init__(self, **kwargs):
        self.title = kwargs.pop("title", "")
        self.subtitle = kwargs.pop("subtitle", "")
        self.uid = kwargs.pop("uid", "{0}.{1}".format(core.bundle(), random.getrandbits(40)))
        if "valid" in kwargs.keys():
            if kwargs["valid"] == True:
                self.valid = "yes"
            elif kwargs["valid"] == False:
                self.valid = "no"
            else:
                self.valid = kwargs["valid"]
            kwargs.pop("valid")
        else:
            self.valid = None
        self.autocomplete = kwargs.pop("autocomplete", None)
        self.icon = kwargs.pop("icon", "icon.png")
        self.fileIcon = kwargs.pop("fileIcon", False)
        self.fileType = kwargs.pop("fileType", False)
        self.arg = kwargs.pop("arg", None)
        self.type = kwargs.pop("type", None)

    def copy(self):
        return copy.copy(self)

    def get(self):
        content = {
            "title": self.title,
            "subtitle": self.subtitle,
            "icon": self.icon,
            "fileIcon": self.fileIcon,
            "fileType": self.fileType
        }
        attrib = {
            "uid": self.uid,
            "valid": self.valid,
        }
        if self.autocomplete:
            attrib["autocomplete"] = self.autocomplete
        if self.arg:
            attrib["arg"] = self.arg
        if self.type:
            attrib["type"] = self.type

        data = {"attrib": attrib, "content": content}

        return data

def feedback(items):
    feedback_items = []

    def processItem(item):
        itemToAdd_dict = {}

        data = item.get()

        for (k, v) in data["attrib"].items():
            if v is None:
                continue
            itemToAdd_dict[k] = v

        for (k, v) in data["content"].items():
            if v is None:
                continue
            if k != "fileIcon" and k != "fileType":
                itemToAdd_dict[k] = v
            if k == "icon":
                if "fileIcon" in data["content"].keys():
                    if data["content"]["fileIcon"] == True:
                        itemToAdd_dict[k] = v
                if "fileType" in data["content"].keys():
                    if data["content"]["fileType"] == True:
                        itemToAdd_dict[k] = v

        feedback_items.append(itemToAdd_dict)

    if isinstance(items, list):
        for anItem in items:
            processItem(anItem)
    else:
        processItem(items)

    print(json.dumps({'items': feedback_items}))
