const scrolls = 8
let scrollCount = 0

const scrollInterval = setInterval(() => {
    window.scrollTo(0, document.body.scrollHeight)
    scrollCount++

    if (scrollCount == scrolls){
        clearInterval(scrollInterval)
    }

}, 500)