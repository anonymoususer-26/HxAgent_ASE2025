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
        Object.keys(getEventListeners(node)).filter((k) => k === "click").length !=
        0 ||
        node.tagName?.toLowerCase() == "input" ||
        node.tagName?.toLowerCase() == "textarea" ||
        node.tagName?.toLowerCase() == "option" ||
        node.tagName?.toLowerCase() == "select" ||
        node.tagName?.toLowerCase() == "a" ||
        node.tagName?.toLowerCase() == "button" ||
        node.tagName?.toLowerCase() == "li"
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
    text = [];
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
    return text.join("\n");
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
    if (node_text != "") {
        obj.text = node_text;
    }
    obj.xpath = getPathTo(node);
    if (obj.tagName != "span") {
        spanclass = getIconClass(node);
        if (spanclass != "") obj.icon = spanclass;
    }
    if (!obj.hasOwnProperty("text")) {
        var infoNode = getInfoNode(node);
        if (!infoNode.isSameNode(node)) {
            if (isContainMultiClickable(infoNode))
                obj.belongTo = getParentInfo(infoNode);
            else if (obj.tagName != "span")
                obj.text = removeUnnecessarySpace(getText(infoNode));
        }
    }

    var attrs = node.attributes;
    if (attrs) {
        var length = attrs.length;
        var arr = (obj.attributes = {});
        for (var j = 0; j < length; j++) {
            attr_node = attrs.item(j);
            arr[attr_node.nodeName] = attr_node.nodeValue;
        }
    }
    return obj;
}
function removeUnnecessaryBelongTo(clickable) {
    var classnamedict = {};
    for (let i = 0; i < clickable.length; i++) {
        if (clickable[i].attributes.hasOwnProperty("class"))
            if (classnamedict.hasOwnProperty(clickable[i].attributes["class"]))
                classnamedict[clickable[i].attributes["class"]].push(i);
            else classnamedict[clickable[i].attributes["class"]] = [i];
    }
    var keeplist = [];
    for (const [key, value] of Object.entries(classnamedict)) {
        if (value.length > 1) keeplist = keeplist.concat(value);
    }
    for (let i = 0; i < clickable.length; i++) {
        if (clickable[i].hasOwnProperty("belongTo"))
            if (!keeplist.includes(i)) delete clickable[i].belongTo;
    }
}
function cleanClickable(clickable) {
    var contain = {};
    for (var i = 0; i < clickable.length; i++) {
        contain[i] = [];
        for (var j = i + 1; j < clickable.length; j++) {
            if (clickable[j]["xpath"].includes(clickable[i]["xpath"]))
                contain[i].push(j);
            else break;
        }
    }
    var dellist = [];
    for (var i = 0; i < clickable.length; i++) {
        if (clickable[i].hasOwnProperty("text")) {
            containallchildtext = -1;
            for (var j = 0; j < contain[i].length; j++) {
                if (clickable[contain[i][j]].hasOwnProperty("text")) {
                    if (containallchildtext == -1) containallchildtext = 1;
                    if (clickable[i]["text"] == clickable[contain[i][j]]["text"]) {
                        dellist = dellist.concat(contain[i]);
                        containallchildtext = 0;
                        break;
                    }
                    if (!clickable[i]["text"].includes(clickable[contain[i][j]]["text"]))
                        containallchildtext = 0;
                }
            }
            if (containallchildtext == 1) dellist.push(i);
        }
    }
    var result = [];
    for (let i = 0; i < clickable.length; i++)
        if (!dellist.includes(i)) result.push(clickable[i]);
    return result;
}
function getJSON() {
    var click = [...document.all].filter((d) => isClickable(d) && isVisible(d));
    click.splice(0, 1);
    var clickable = [];
    for (let i = 0; i < click.length; i++) {
        clickable.push(toJSONXPathKey(click[i]));
    }
    removeUnnecessaryBelongTo(clickable);
    return cleanClickable(clickable);
}
getJSON();