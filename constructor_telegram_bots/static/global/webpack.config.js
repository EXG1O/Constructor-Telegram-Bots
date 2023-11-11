const BundleTracker = require('webpack-bundle-tracker');

module.exports = {
	extends: './base.webpack.config.js',
	entry: {
		logout: `${__dirname}/src/ts/logout.ts`,
		login_via_telegram_modal: `${__dirname}/src/ts/login_via_telegram_modal.ts`,
	},
	output: {
		path: `${__dirname}/dist/js`,
		filename: '[name].bundle.min.js',
		clean: true,
	},
	plugins: [
		new BundleTracker({
			path: './',
			publicPath: '/static/global/dist/js/',
			filename: 'global.webpack.static.json',
		}),
	],
};