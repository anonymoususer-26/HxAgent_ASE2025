function toJSONWithHeadTags(node) {
    var obj = {};
    obj.element = toJSONXPathKey(node);
    obj.head = {
        title: document.title,
        canonical_link: window.location.href
    }
    const tags = getAllTagNames(obj.element);
    obj.tags = [...new Set(tags)]

    return obj;
} 

function toJSONXPathKey(node) {
  node = node || this;
  var obj = {};
  let is_space_text_node = isSpaceTextNode(node);

  if (!is_space_text_node && node.nodeName!="#text"){
      if (node.tagName) {
      obj.tagName = node.tagName.toLowerCase();
      } else if (node.nodeName) {
      obj.nodeName = node.nodeName;
      }
      if (node.nodeValue) {
      obj.nodeValue = node.nodeValue;
      }
      if (node.nodeType == 1) {
      style = window.getComputedStyle(node);
      obj["text"] = getText(node);
      }
  }

  var attrs = node.attributes;
  if (attrs) {
    var length = attrs.length;
    var arr = (obj.attributes = {});
    for (var i = 0; i < length; i++) {
      attr_node = attrs.item(i);
      arr[attr_node.nodeName] = attr_node.nodeValue;
    }
  }
  
  var obj_xpath = {};
  var childNodes = node.childNodes;
  if (childNodes && !is_space_text_node && node.nodeName!="#text") {
    length = childNodes.length;
    arr = new Array();
    for (i = 0; i < length; i++)
      arr.push(toJSONXPathKey(childNodes[i]));

    arr = arr.filter(element => Object.keys(element).length !== 0);

    if (arr.length == 0){
      arr = {};
    } else {
      arr = arr.reduce((acc, cur) => ({ ...acc, ...cur }));
    }


    obj.childNodes = arr;
    if (Object.keys(obj).length !== 0){
      var xpath = getPathTo(node);
      var xpath_last_element = getLastElementFromXPath(xpath);
      obj_xpath[xpath_last_element] = obj;
    }
  }

  return obj_xpath;
}

function getCSS(node) {
  var visual_cues = {};
  style = window.getComputedStyle(node);
  visual_cues["bounds"] = node.getBoundingClientRect();
  visual_cues["font-size"] = style.getPropertyValue("font-size");
  visual_cues["font-weight"] = style.getPropertyValue("font-weight");
  visual_cues["background-color"] = style.getPropertyValue("background-color");
  visual_cues["display"] = style.getPropertyValue("display");
  visual_cues["visibility"] = style.getPropertyValue("visibility");
  visual_cues["text"] = node.innerText;
  visual_cues["this_text"] = getText(node);
  visual_cues["className"] = node.className;
  visual_cues["contain_image"] = node.querySelector("img") != null || node.querySelector("svg") != null;
  if (node.hasAttribute("data-block-type")) {
    visual_cues["data-block-type"] = node.getAttribute("data-block-type");
  }
  if (node.hasAttribute("data-block")) {
    visual_cues["data-block"] = node.getAttribute("data-block");
  }
  return visual_cues;
}

function getPathTo(element) {
  if (element===document.body)
      return element.tagName;

  var ix= 0;
  var siblings= element.parentNode.childNodes;
  for (var i= 0; i<siblings.length; i++) {
      var sibling= siblings[i];
      if (sibling===element)
          return getPathTo(element.parentNode)+'/'+element.tagName+'['+(ix+1)+']';
      if (sibling.nodeType===1 && sibling.tagName===element.tagName)
          ix++;
  }
}

function toDOM(obj) {
  if (typeof obj == "string") {
    obj = JSON.parse(obj);
  }
  var node,
    nodeType = obj.nodeType;
  switch (nodeType) {
    case 1: //ELEMENT_NODE
      node = document.createElement(obj.tagName);
      var attributes = obj.attributes || [];
      for (var i = 0, len = attributes.length; i < len; i++) {
        var attr = attributes[i];
        node.setAttribute(attr[0], attr[1]);
      }
      break;
    case 3:
      node = document.createTextNode(obj.nodeValue);
      break;
    case 8:
      node = document.createComment(obj.nodeValue);
      break;
    case 9: 
      node = document.implementation.createDocument();
      break;
    case 10:
      node = document.implementation.createDocumentType(obj.nodeName);
      break;
    case 11: 
      node = document.createDocumentFragment();
      break;
    default:
      return node;
  }
  if (nodeType == 1 || nodeType == 11) {
    var childNodes = obj.childNodes || [];
    for (i = 0, len = childNodes.length; i < len; i++) {
      node.appendChild(toDOM(childNodes[i]));
    }
  }
  return node;
}

function getRecursiveBounds(element) {
  let bounds = element.getBoundingClientRect();
  if (element.children.length) {
    for (let child of element.children) {
      if (isVisible(child)) {
        let childBounds = getRecursiveBounds(child);
        bounds = mergeBounds(bounds, childBounds);
      }
    }
  }
  return bounds;
}

function getBoundingBox1level(element) {
  let bounds = element.getBoundingClientRect();
  if (element.children.length) {
    for (let child of element.children) {
      if (isVisible(child)) {
        // let childBounds = getRecursiveBounds(child);
        bounds = mergeBounds(bounds, child.getBoundingClientRect());
      }
    }
  }
  return bounds;
}

function mergeBounds(rect1, rect2) {
  let left = Math.min(rect1.left, rect2.left);
  let top = Math.min(rect1.top, rect2.top);
  let right = Math.max(rect1.right, rect2.right);
  let bottom = Math.max(rect1.bottom, rect2.bottom);
  let x = left;
  let y = top;
  let width = right - left;
  let height = bottom - top;
  return { x, y, width, height, top, right, bottom, left };
}

function isVisible(node) {
  if (node.nodeType == Node.TEXT_NODE) {
    return node.textContent.trim() != "";
  }
  if (node.nodeType == Node.ELEMENT_NODE) {
    invisibleTags = [
      "SCRIPT",
      "NOSCRIPT",
      "STYLE",
      "LINK",
      "META",
      "HEAD",
      "IFRAME",
      "OBJECT",
      "EMBED",
    ];

    if (invisibleTags.includes(node.tagName)) {
      return false;
    }

    let style = window.getComputedStyle(node);
    if (
      style.getPropertyValue("display") == "none" ||
      style.getPropertyValue("visibility") == "hidden" ||
      style.getPropertyValue("opacity") == "0" ||
      style.getPropertyValue("display").toString().includes("none")
    ) {
      return false;
    }

    if (node.nodeType == Node.TEXT_NODE) {
      return node.textContent.trim() != "";
    } else if (node.nodeType == Node.ELEMENT_NODE) {
      return !!(
        node.offsetWidth ||
        node.offsetHeight ||
        node.getClientRects().length
      );
    } else {
      return false;
    }
  }
}

function getText(node){
  let text = "";
  for (let child of node.childNodes) {
    if (child.nodeType == Node.TEXT_NODE) {
      text += child.textContent;
    }
  }
  text = text.replace(/\s+/g, " ").trim();
  return text;
}

function removeWhitespaceTextNodes(node) {
  for (var i = node.childNodes.length - 1; i >= 0; i--) {
      var childNode = node.childNodes[i];

      if (childNode.nodeType === 1) {
        removeWhitespaceTextNodes(childNode);
      } else if (childNode.nodeType === 3) {
        var textValue = childNode.nodeValue.trim();
        if (/^\s*$/.test(textValue)) node.removeChild(childNode);
      }
  }
}

function isSpaceTextNode(node){
  if (node.nodeType == 3) {
      var textValue = node.nodeValue.trim();
      if (/^\s*$/.test(textValue)) return true;
  }
  return false;
}

function getLastElementFromXPath(xpath) {
  const matches = xpath.match(/\/([^/[\]]+)\[([0-9]+)\]$/);
  if (matches && matches.length === 3) {
    const elementName = matches[1];
    const index = matches[2];
    return `${elementName}[${index}]`;
  }
  return xpath;
}

const getAllTagNames = (obj, tagNames = []) => {
  if (obj.tagName) tagNames.push(obj.tagName);

  if (typeof obj === 'object') {
    for (const key in obj) {
      if (key !== 'tagName') {
        getAllTagNames(obj[key], tagNames);
      }
    }
  }

  return tagNames;
};

return toJSONWithHeadTags(document.getElementsByTagName("BODY")[0]);
