const fs = require('fs')
const products = require('./products')

const init = 'https://www.instagram.com/explore/tags/';

const data = products.map(product => {
	return init + product.split(' ').filter(x => !/[A-Z]/.test(x)).join('')
})

fs.writeFileSync('hash.json', JSON.stringify(data, null, 2))