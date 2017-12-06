'use strict';

const fs = require('fs');
const lodash = require('lodash');
const brands = require('./brands');
const products = require('./products')

function fml(data) {
	return Object.keys(data).reduce(
		(acc, key) => Object.assign(acc, {
			[key]: data[key].reduce(
				(a, v) => Object.assign(a, v.data),
				{}
			)
		}),
		{}
	)
}

function gg(data) {
	const result = data.map(x => {
		return x.map(b => {
			const keys = Object.keys(b.default)
			if (keys.includes('timelineData')) {
				const { timelineData } = b.default
				return timelineData.map(t => {
					const {
					value,
						time
				} = t
					const data = lodash.zipObject(b.keyword, value)
					return {
						time,
						data
					}
				})
			}

			if (keys.includes('geoMapData')) {
				const { geoMapData } = b.default
				return geoMapData.map(g => {
					const {
					value,
						geoName: location
				} = g;
					const data = lodash.zipObject(b.keyword, value)
					return {
						location,
						data
					}
				})
			}
		});
	});

	const final = lodash.flattenDeep(result)

	const locationData = lodash.groupBy(final.filter(f => f.location), 'location')
	const timeData = lodash.groupBy(final.filter(f => f.time), 'time')

	return {
		location: fml(locationData),
		time: fml(timeData)
	}
}

fs.writeFileSync('gg.json', JSON.stringify({
		brands: gg(brands),
		products: gg(products)
	}, null, 2)
)
