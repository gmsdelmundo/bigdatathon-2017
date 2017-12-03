const fs = require('fs')
const keywords = require('./keywords')

const brands = {};

const data = keywords.map(keyword => {
	const words = keyword.split(' ');

	let found = false;

	const result = {
		brand: '',
		product: ''
	}

	for (const word of words) {
		if (found) {
			result.product += ` ${word}`;
			continue;
		}

		if (/[a-z]/.test(word)) {
			found = true;
			result.product += `${word}`
		} else {
			result.brand += `${word} `;
		}
	}
	result.brand = result.brand.trim()

	if (!brands[result.brand]) {
		brands[result.brand] = []
	} else {
		brands[result.brand].push(result.product)
	}

	return result;
});

const final = Object.keys(brands).map(brand => {
	// return [
	// 	brand,
	// 	...brands[brand]
	// ];
	return brands[brand]
})
.reduce((acc, d) => acc.concat(d), [])
.filter(d => Boolean(d));

fs.writeFileSync('products.json', JSON.stringify(final, null, 2))