const puppeteer = require('puppeteer')
const net = require('net')

const browserPool = []

const getBrowser = async () => {
    if (browserPool.length > 0) {
        return browserPool.pop()
    }
    return await puppeteer.launch({
        headless: true,
        args: ['--js-flags=--jitless', '--no-sandbox', '--disable-setuid-sandbox', '--allow-running-insecure-content']
    })
}

const returnBrowser = (browser) => {
    browserPool.push(browser)
}


const visitSubmission = async (url) => {
    console.log("Visiting:", url);
    const browser = await getBrowser()
    const page = await browser.newPage()
    try {
        await page.goto(url, { waitUntil: 'networkidle2', timeout: 5000 })
    }
    catch (e) {
        console.log(e)
    }
    await page.close()
    returnBrowser(browser)
}

setInterval(() => {
    while (browserPool.length > 0) {
        const browser = browserPool.pop()
        browser.close()
    }
}, 5 * 60 * 1000)

const server = net.createServer((socket) => {
    socket.on('data', async (data) => {
        const id = data.toString()
        await visitSubmission(id)
    })
})

server.listen(3001, () => {
    console.log('Listening on port 3001')
})