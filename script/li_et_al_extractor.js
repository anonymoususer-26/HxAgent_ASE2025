function isVisible(node) {
    if (node.nodeType == Node.TEXT_NODE) {
        return node.textContent?.trim() != "";
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
        "PATH",
        "CIRCLE",
        "RECT"
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

function getLeafNodes(master) {
    var nodes = Array.prototype.slice.call(master.getElementsByTagName("*"), 0);
    var leafNodes = nodes.filter(function(elem) {
        if (!isVisible(elem)) {
            return false;
        }
        if (elem?.contentEditable == "true" || elem?.contentEditable == "plaintext" || elem?.tagName.toLowerCase() == "input" || elem?.tagName.toLowerCase() == "textarea")
            return true;
        if (elem?.tagName.toLowerCase() == "button" || elem?.tagName.toLowerCase() == "input" || elem?.tagName.toLowerCase() == "a") {
            return true;
        }
        if (elem.hasChildNodes()) {
            for (var i = 0; i < elem.childNodes.length; i++) {
                if (elem.childNodes[i].nodeType == 1) {
                    return false;
                }
            }
        }
        return true;
    });
    return leafNodes;
}

function getRepresentation(disable_ids) {
    var leafNodes = getLeafNodes(document.body);
    leafNodes = leafNodes.filter(function(elem) {
        return elem.tagName.toLowerCase() != "script" && elem.tagName.toLowerCase() != "noscript" && elem.tagName.toLowerCase() != "style" && elem.tagName.toLowerCase() != "link" && elem.tagName.toLowerCase() != "meta" && elem.tagName.toLowerCase() != "head" && elem.tagName.toLowerCase() != "iframe" && elem.tagName.toLowerCase() != "object" && elem.tagName.toLowerCase() != "embed" && elem.tagName.toLowerCase() != "path" && elem.tagName.toLowerCase() != "circle" && elem.tagName.toLowerCase() != "rect";
    });
    var representation = [];
    for (let i = 0; i < leafNodes.length; i++) {
        const elem = leafNodes[i];
        const cloneNode = elem.cloneNode(true);
        let ariaLabel = cloneNode.getAttribute("aria-label");
        let role = cloneNode.getAttribute("role");
        while (cloneNode.attributes.length > 0) {
            cloneNode.removeAttribute(cloneNode.attributes[0].name);
        }
        cloneNode.ariaLabel = ariaLabel;
        cloneNode.role = role;
        cloneNode.class = null;
        if (!disable_ids.includes(i+1)){
            cloneNode.id = i+1;
            elem.setAttribute("hxagentidentity", i+1);
        }
        cloneNode.innerText = cloneNode.innerText?.trim();
        representation.push(cloneNode.outerHTML);
    };
    return representation.join("\n");
}

getRepresentation([]);