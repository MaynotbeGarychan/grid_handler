import xml.dom.minidom as md

def make_one_info_amitex_fftp(root,head_str,item_list):
    info = root.createElement(head_str)
    for item in item_list:
        info.setAttribute(item[0], item[1])
    return info