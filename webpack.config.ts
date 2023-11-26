import { Configuration } from 'webpack';
import * as MiniCssExtractPlugin from 'mini-css-extract-plugin';
import * as BundleTracker from 'webpack-bundle-tracker';
import * as MonacoWebpackPlugin from 'monaco-editor-webpack-plugin';

const mainAppStaticDirPath =  `${__dirname}/constructor_telegram_bots/static`;
const defaultEntryFilePath = `${mainAppStaticDirPath}/default/src/ts/main.ts`;

const baseConfig: Configuration = {
	entry: [defaultEntryFilePath],
	output: {
		filename: 'js/[name].min.js',
		clean: true,
	},
	module: {
		rules: [
			{
				test: /\.(ts|tsx)$/,
				use: ['ts-loader'],
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
			global_modules: `${mainAppStaticDirPath}/global_modules/`,
			telegram_bot_api: `${__dirname}/telegram_bot/api/static/telegram_bot/api/`,
			telegram_bot_frontend: `${__dirname}/telegram_bot/frontend/static/telegram_bot/frontend/`,
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
	outputPath: string,
	statsFileName: string,
	extraConfig?: Configuration,
): Configuration {
	return {
		...baseConfig,
		...extraConfig,
		output: {
			...baseConfig.output,
			...(extraConfig?.output || {}),
			path: `${__dirname}/${outputPath}`,
			publicPath: `/static${outputPath.split('static')[1]}/`,
		},
		plugins: [
			...baseConfig.plugins as any[],
			...(extraConfig?.plugins || []),
			new BundleTracker({
				path: './',
				filename: `${statsFileName}.webpack.stats.json`,
			}),
		],
	}
}

const telegramBotMenuStaticDirPath = `${__dirname}/telegram_bot/frontend/static/telegram_bot_menu`;
const telegramBotMenuAnimationFilePath = `${telegramBotMenuStaticDirPath}/animation/main.ts`;
const telegramBotMenuDefaultEntryFilesPath = [...baseConfig.entry as string[], `${telegramBotMenuStaticDirPath}/default/src/css/main.css`];

export default [
	generateConfig('constructor_telegram_bots/static/default/dist', 'default'),
	generateConfig('home/static/home/dist', 'home', {
		entry: [...baseConfig.entry as string[], `${__dirname}/home/static/home/src/css/main.css`],
	}),
	generateConfig('telegram_bot/frontend/static/telegram_bot_menu/default/dist', 'default.telegram-bot-menu', {
		entry: telegramBotMenuDefaultEntryFilesPath,
	}),
	generateConfig('telegram_bot/frontend/static/telegram_bot_menu/index/dist', 'index.telegram-bot-menu', {
		entry: [...telegramBotMenuDefaultEntryFilesPath, `${telegramBotMenuStaticDirPath}/index/src/ts/main.ts`],
	}),
	generateConfig('telegram_bot/frontend/static/telegram_bot_menu/variables/dist', 'variables.telegram-bot-menu', {
		entry: [...telegramBotMenuDefaultEntryFilesPath, `${telegramBotMenuStaticDirPath}/variables/src/ts/main.ts`],
	}),
	generateConfig('telegram_bot/frontend/static/telegram_bot_menu/database/dist', 'database.telegram-bot-menu', {
		entry: [...telegramBotMenuDefaultEntryFilesPath, telegramBotMenuAnimationFilePath, `${telegramBotMenuStaticDirPath}/database/src/ts/main.ts`],
		plugins: [new MonacoWebpackPlugin()],
	}),
]