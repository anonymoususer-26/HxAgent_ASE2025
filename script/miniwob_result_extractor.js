let obj = {};
obj.reward = document.querySelectorAll('div[class="info"]')[0].childNodes[3].textContent
obj.avg10 = document.querySelectorAll('div[class="info"]')[1].childNodes[3].textContent
obj.ep = document.querySelectorAll('div[class="info"]')[3].childNodes[3].textContent
return obj