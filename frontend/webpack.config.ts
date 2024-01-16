import { Configuration } from 'webpack';
import MiniCssExtractPlugin from 'mini-css-extract-plugin';
import CssMinimizerPlugin from 'css-minimizer-webpack-plugin';
import HtmlWebpackPlugin from 'html-webpack-plugin';
import Dotenv from 'dotenv-webpack';

const config: Configuration = {
	entry: './src/index.tsx',
	output: {
		clean: true,
		path: `${__dirname}/dist/frontend`,
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
				test: /\.s?css$/,
				use: [MiniCssExtractPlugin.loader, 'css-loader', 'sass-loader'],
			},
		],
	},
	resolve: {
		extensions: ['.js', '.jsx', '.ts', '.tsx', '.css'],
		alias: {
			styles: `${__dirname}/src/styles/`,
			components: `${__dirname}/src/components/`,
			routes: `${__dirname}/src/routes/`,
			services: `${__dirname}/src/services/`,
			utils: `${__dirname}/src/utils/`,
		},
	},
	optimization: {
		minimizer: [
			'...',
			new CssMinimizerPlugin(),
		],
	},
	plugins: [
		new Dotenv(),
		new HtmlWebpackPlugin({
			template: './src/index.html',
			publicPath: '/static/frontend/',
		}),
		new MiniCssExtractPlugin({
			filename: '[name].[contenthash].css',
		}),
	],
}

export default config;