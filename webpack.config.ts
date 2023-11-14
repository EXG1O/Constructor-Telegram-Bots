import {Configuration} from 'webpack';
import * as MiniCssExtractPlugin from 'mini-css-extract-plugin';
import * as BundleTracker from 'webpack-bundle-tracker';

const mainAppStaticDirPath =  `${__dirname}/constructor_telegram_bots/static`;
const defaultEntryDirPath = `${mainAppStaticDirPath}/default/src/ts/entry`;

const baseConfig: Configuration = {
	entry: {
		main: `${defaultEntryDirPath}/main.ts`,
		user_is_auth: `${defaultEntryDirPath}/user_is_auth.ts`,
		user_is_not_auth: `${defaultEntryDirPath}/user_is_not_auth.ts`,
	},
	output: {
		filename: 'js/[name].min.js',
		clean: true,
	},
	module: {
		rules: [
			{
				test: /\.(ts|tsx)$/,
				loader: 'ts-loader',
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
			default_entry: defaultEntryDirPath,
			global_modules: `${mainAppStaticDirPath}/global_modules/`,
		},
	},
	plugins: [
		new MiniCssExtractPlugin({
			filename: 'css/[name].min.css',
		}),
	],
	optimization: {
		splitChunks: {
			chunks: 'all',
		},
	},
}

function generateConfig(
	appName: string,
	configName: string,
	extraConfig?: Configuration,
): Configuration {
	return {
		...baseConfig,
		...extraConfig,
		output: {
			...baseConfig.output,
			...(extraConfig?.output || {}),
			path: `${__dirname}/${appName}/static/${configName}/dist`,
			publicPath: `/static/${configName}/dist/`,
		},
		plugins: [
			...baseConfig.plugins as any[],
			...(extraConfig?.plugins || []),
			new BundleTracker({
				path: './',
				filename: `${configName}.webpack.stats.json`,
			}),
		],
	}
}

export default [
	generateConfig('constructor_telegram_bots', 'default'),
	generateConfig('home', 'home', {
		entry: {
			...baseConfig.entry as object,
			main: `${__dirname}/home/static/home/src/ts/main.ts`,
		},
	}),
]