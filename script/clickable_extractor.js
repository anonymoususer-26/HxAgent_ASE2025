function getXPath( el, customOptions) {
  const options = { ignoreId: true, ...customOptions };
  let nodeElem = el;
  if ( nodeElem && nodeElem.id && ! options.ignoreId ) {
      return "//*[@id=\"" + nodeElem.id + "\"]";
  }
  let parts = [];
  while ( nodeElem && Node.ELEMENT_NODE === nodeElem.nodeType ) {
      let nbOfPreviousSiblings = 0;
      let hasNextSiblings = false;
      let sibling = nodeElem.previousSibling;
      while ( sibling ) {
          if ( sibling.nodeType !== Node.DOCUMENT_TYPE_NODE &&
              sibling.nodeName === nodeElem.nodeName
          ) {
              nbOfPreviousSiblings++;
          }
          sibling = sibling.previousSibling;
      }
      sibling = nodeElem.nextSibling;
      while ( sibling ) {
          if ( sibling.nodeName === nodeElem.nodeName ) {
              hasNextSiblings = true;
              break;
          }
          sibling = sibling.nextSibling;
      }
      let prefix = nodeElem.prefix ? nodeElem.prefix + ":" : "";
      let nth = nbOfPreviousSiblings || hasNextSiblings
          ? "[" + ( nbOfPreviousSiblings + 1 ) + "]"
          : "";
      parts.push( prefix + nodeElem.localName + nth );
      nodeElem = nodeElem.parentNode;
  }
  return parts.length ? "/" + parts.reverse().join( "/" ) : "";
}

function makeid(length) {
  let result = '';
  const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  const charactersLength = characters.length;
  let counter = 0;
  while (counter < length) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength));
    counter += 1;
  }
  return result;
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
    let bound = node.getBoundingClientRect();
    topElt = document.elementFromPoint(
      bound.x + bound.width / 2,
      bound.y + bound.height / 2
    );
    if (
      style.getPropertyValue("display") == "none" ||
      style.getPropertyValue("visibility") == "hidden" ||
      style.getPropertyValue("opacity") == "0" ||
      style.getPropertyValue("display").toString().includes("none") ||
      bound.width == 0 ||
      bound.height == 0 ||
      bound.bottom == 0 ||
      bound.right == 0
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
function getPathTo(element) {
  if (element === document.body) return "html/" + element.tagName.toLowerCase();
  var ix = 0;
  var siblings = element.parentNode.childNodes;
  for (var i = 0; i < siblings.length; i++) {
    var sibling = siblings[i];
    if (sibling === element)
      if (
        ["body", "div", "button", "input", "textarea", "span"].includes(
          element.tagName.toLowerCase()
        )
      )
        return (
          getPathTo(element.parentNode) +
          "/" +
          element.tagName.toLowerCase() +
          "[" +
          (ix + 1) +
          "]"
        );
      else
        return (
          getPathTo(element.parentNode) +
          "/" +
          `*[name()='${element.tagName.toLowerCase()}']` +
          "[" +
          (ix + 1) +
          "]"
        );
    if (sibling.nodeType === 1 && sibling.tagName === element.tagName) ix++;
  }
}
function isClickable(node) {
  if (node.className && typeof node.className.includes !== 'undefined' && node.className.includes("ui-state-disabled"))
    return false;
  return (
    Object.keys(getEventListeners(node))
      .filter((k) => k === "click" || k === "tap").length != 0 ||
    node?.contentEditable == "true" ||
    node?.contentEditable == "plaintext" ||
    node.tagName?.toLowerCase() == "input" ||
    node.tagName?.toLowerCase() == "textarea" ||
    node.tagName?.toLowerCase() == "option" ||
    node.tagName?.toLowerCase() == "select" ||
    node.tagName?.toLowerCase() == "a" ||
    node.tagName?.toLowerCase() == "button"
  );
}
function getParentInfo(node) {
  child = node.querySelectorAll("*");
  info = {};
  for (let i = 0; i < child.length; i++) {
    if (
      removeUnnecessarySpace(getTextWithoutChildText(child[i])) != "" &&
      isVisible(child[i]) &&
      !isClickable(child[i])
    ) {
      info[child[i].className.replace("-", " ")] = removeUnnecessarySpace(
        getTextWithoutChildText(child[i])
      );
    }
  }
  return info;
}
function removeUnnecessarySpace(text) {
    if (typeof text === "undefined") return ""; 
  return text.trim().replace(/\s*\n\s*\n*\s*/g, "\n"); //.replace(/\s*/g, '\s')
}
function getIconClass(node) {
  span = [...node.getElementsByTagName("*")].filter(
    (d) => d.tagName.toLowerCase() == "span" && isVisible(d)
  );
  if (span.length == 1) {
    return span[0].className;
  }
  return "";
}
function getText(node, removeclickable = false) {
  let text = [];
  if (node.getElementsByTagName("*").length == 0) {
    if (isVisible(node) && !(removeclickable && isClickable(node))) {
      return node.innerText;
    }
  }
  node.childNodes.forEach(function check(child) {
    if (isVisible(child)) {
      if (!(removeclickable && isClickable(child))) {
        if (child.nodeType == Node.TEXT_NODE) {
          text.push(child.textContent);
        } else text.push(child.innerText);
      } else child.childNodes.forEach(check);
    }
  });
  return node.innerText;
}
function getTextWithoutChildText(node) {
  let text = "";
  for (let child of node.childNodes) {
    if (child.nodeType == Node.TEXT_NODE) {
      text += child.textContent;
    }
  }
  text = text.replace(/\s+/g, " ").trim();
  return text;
}
function getInfoNode(node) {
  var parent = node;
  while (true) {
    if (parent.parentElement.tagName.toLowerCase() != "body") {
      if (removeUnnecessarySpace(getText(parent, true)) != "") return parent;
      parent = parent.parentElement;
    } else return node;
  }
}
function isContainMultiClickable(node) {
  if (
    [...node.getElementsByTagName("*")].filter(
      (d) => isClickable(d) && isVisible(d)
    ).length > 1
  )
    return true;
  return false;
}
function toJSONXPathKey(node) {
  var obj = {};
  obj.tagName = node.tagName.toLowerCase();
  node_text = removeUnnecessarySpace(getText(node));
  //node_text = node_text.includes("\n") ? "" : node_text;
  // Replace all the new line characters with space
  node_text = node_text.replace(/\n/g, " ");
  if (node_text != "") {
    obj.text = node_text;
  }

  if (!node.id) {
    node.setAttribute("id", makeid(20));
  }

  obj.xpath = getXPath(node);
  if (obj.tagName != "span") {
    spanclass = getIconClass(node);
    if (spanclass != "") obj.icon = spanclass;
  }
  if (!obj.hasOwnProperty("text")) {
    var infoNode = getInfoNode(node);
    if (!infoNode.isSameNode(node)) {
      if (obj.tagName != "span")
        node_text = removeUnnecessarySpace(getText(infoNode));
        node_text = node_text.includes("\n") ? "" : node_text;
      }
  }

  var attrs = null;
  if (node?.ariaLabel) attrs = { 'aria-label': node.ariaLabel, 'placeholder': node.placeholder };
  if (node?.placeholder) {
    if (attrs) {
      attrs['placeholder'] = node.placeholder;
    } else {
      attrs = { 'placeholder': node.placeholder };
    }
  }

  if (attrs) {
    obj['attributes'] = attrs;
  }

  if (node.contentEditable == 'true' || node.contentEditable == 'plaintext-only') {
    obj['tagName'] = 'input';
  }

  if (obj['tagName'] == 'input' && (node.type == "checkbox" || node.type == "radio")) 
    obj['tagName'] = 'button';

  if (obj['tagName'] == 'input') {
    attrs = node.attributes;
    var length = attrs.length;
    var arr = (obj.attributes = {});
    for (var j = 0; j < length; j++) {
      attr_node = attrs.item(j);
      arr[attr_node.nodeName] = attr_node.nodeValue;
    }
  }

  
  return obj;
}

function cleanClickable(clickable) {
  var contain = {};
  for (var i = 0; i < clickable.length; i++) {
    contain[i] = [];
    for (var j = i + 1; j < clickable.length; j++) {
      if (clickable[j]["xpath"].includes(clickable[i]["xpath"]))
        contain[i].push(j);
    }
  }
  var dellist = [];
  for (var i = 0; i < clickable.length; i++) {
    if (clickable[i].hasOwnProperty("text")) {
      containallchildtext = -1;
      for (var j = 0; j < contain[i].length; j++) {
        if (clickable['tagName'] == 'input') break;
        if (clickable[contain[i][j]].hasOwnProperty("text")) {
          if (clickable[i]["text"].includes(clickable[contain[i][j]]["text"])) {
            containallchildtext = 1;
            break;
          }

          if (clickable[i]["text"] == clickable[contain[i][j]]["text"]) {
            containallchildtext = 1;
            break;
          }
        }
      }
      if (containallchildtext == 1) dellist.push(i);
    }
  }
  var result = [];
  for (let i = 0; i < clickable.length; i++)
    if (!dellist.includes(i)) 
      result.push(clickable[i]);
  return result;
}

function getJSON() {
  var click = [...document.all].filter((d) => isClickable(d) && isVisible(d));
  click.splice(0, 1);
  var clickable = [];
  for (let i = 0; i < click.length; i++) {
    clickable.push(toJSONXPathKey(click[i]));
  }
  // console.log(clickable);
  let result = cleanClickable(clickable);
  const url = window.location.toString()
  if (url.includes("youtube.com")) {
    const new_result = []
    for (let i = 0; i < result.length; i++) {
      if (result[i]['xpath'].startsWith("/html/body/ytd-app/div[1]"))
        new_result.push(result[i]);
    }
    result = new_result
  }

  return result.filter(e => Object.keys(e).length > 2);
}

getJSON();