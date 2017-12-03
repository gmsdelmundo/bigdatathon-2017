const googleTrends = require('google-trends-api');
const lodash = require('lodash');

let search = require('./search.json')
const products = require('./products.json')
const brands = require('./brands.json')

const other = {
	startTime: new Date('2016-01-01'),
	endTime: new Date('2017-11-01'),
	resolution: 'CITY'
};

async function main(keyword) {
	try {
		const promises = [
			googleTrends.interestOverTime(Object.assign(other, {keyword})),
			googleTrends.interestByRegion(Object.assign(other, {keyword})),
		]
		const values = await Promise.all(promises)
		const result = values.map(
			value => {
				const parse = JSON.parse(value);
				parse.keyword = keyword;
				return parse;
			}
		)
		return result
	} catch(error) {
		throw(error)
	}
}

function timer() {
	return new Promise((resolve, reject) => {
		setTimeout(() => {
			resolve(undefined)
		}, 2000)
	})
}

async function index() {
	for (const s of search) {
		for (const keyword of s) {
			await timer();

			(function (k) {
				if (!k) return
				main(k)
					.then(result => {
						console.log(JSON.stringify(result, null, 2) + ',')
					})
					.catch(console.error)
			}(keyword));
		}
	}
}

async function dataIndex(data) {
	const head = data.shift(1);
	const chunks = lodash.chunk(data, 4);
	const final = chunks.map(chunk => chunk.concat(head));
	for (const keyword of final) {
			await timer();

			(function (k) {
				if (!k) return
				main(k)
					.then(result => {
						console.log(JSON.stringify(result, null, 2) + ',')
					})
					.catch(console.error)
			}(keyword));
	}
}

// index()
dataIndex(brands)
// dataIndex(products)
	.then(() => undefined)
	.catch(console.error)
