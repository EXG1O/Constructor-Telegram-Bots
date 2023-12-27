import { Configuration } from 'webpack';
import MiniCssExtractPlugin from 'mini-css-extract-plugin';
import BundleTracker from 'webpack-bundle-tracker';

const config: Configuration = {
	entry: './src/index.tsx',
	output: {
		clean: true,
		path: `${__dirname}/dist/frontend`,
		publicPath: '/static/frontend/',
		filename: '[name].[contenthash].bundle.js',
		chunkFilename: '[name].[contenthash].chunk.js',
	},
	module: {
		rules: [
			{
				test: /\.(tsx?|jsx?)$/,
				exclude: /node_modules/,
				use: 'babel-loader',
			},
			{
				test: /\.css$/,
				use: [MiniCssExtractPlugin.loader, 'css-loader'],
			},
		],
	},
	resolve: {
		extensions: ['.js', '.ts', '.tsx', '.css'],
		alias: {
			components: `${__dirname}/src/components/`,
			routes: `${__dirname}/src/routes/`,
			services: `${__dirname}/src/services/`,
			utils: `${__dirname}/src/utils/`,
		},
	},
	plugins: [
		new MiniCssExtractPlugin({
			filename: '[name].[contenthash].css',
		}),
		new BundleTracker({
			path: './',
			filename: 'webpack.stats.json',
		}),
	],
}

export default config;