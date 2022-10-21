const {saveItem} = require('crawlab-sdk')

async function run() {
    saveItem({'hello': 'world'})
}

run()
