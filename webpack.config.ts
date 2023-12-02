import { Configuration } from 'webpack';
import MiniCssExtractPlugin from 'mini-css-extract-plugin';
import BundleTracker from 'webpack-bundle-tracker';
import MonacoWebpackPlugin from 'monaco-editor-webpack-plugin';

const mainAppStaticDirPath =  `${__dirname}/constructor_telegram_bots/static`;
const defaultEntryFilePath = `${mainAppStaticDirPath}/default/src/ts/main.ts`;

const baseConfig: Configuration = {
	entry: [defaultEntryFilePath],
	output: {filename: 'js/[name].min.js', clean: true},
	module: {
		rules: [
			{test: /\.(ts|tsx)$/, use: ['ts-loader']},
			{test: /\.css$/, use: [MiniCssExtractPlugin.loader, 'css-loader']},
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
	plugins: [new MiniCssExtractPlugin({filename: 'css/[name].min.css'})],
	optimization: {splitChunks: {chunks: 'all'}},
}

function generateConfig(outputPath: string, statsFileName: string, extraConfig?: Configuration): Configuration {
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
			new BundleTracker({path: './webpack_stats/', filename: `${statsFileName}.webpack.stats.json`}),
		],
	}
}

namespace TelegramBotMenu {
	const staticDirRelativePath = 'telegram_bot/frontend/static/telegram_bot_menu';
	const staticDirAbsolutePath = `${__dirname}/${staticDirRelativePath}`;
	const animationEntryFilePath = `${staticDirAbsolutePath}/animation/main.ts`;
	const defaultEntryFilesPath = [...baseConfig.entry as string[], `${staticDirAbsolutePath}/default/src/css/main.css`];

	export const configs: Configuration[] = [
		generateConfig(`${staticDirRelativePath}/default/dist`, 'default.telegram-bot-menu', {
			entry: defaultEntryFilesPath,
		}),
		generateConfig(`${staticDirRelativePath}/index/dist`, 'index.telegram-bot-menu', {
			entry: [...defaultEntryFilesPath, `${staticDirAbsolutePath}/index/src/ts/main.tsx`],
		}),
		generateConfig(`${staticDirRelativePath}/variables/dist`, 'variables.telegram-bot-menu', {
			entry: [...defaultEntryFilesPath, `${staticDirAbsolutePath}/variables/src/ts/main.ts`],
		}),
		generateConfig(`${staticDirRelativePath}/users/dist`, 'users.telegram-bot-menu', {
			entry: [...defaultEntryFilesPath, animationEntryFilePath, `${staticDirAbsolutePath}/users/src/ts/main.ts`],
		}),
		generateConfig(`${staticDirRelativePath}/database/dist`, 'database.telegram-bot-menu', {
			entry: [...defaultEntryFilesPath, animationEntryFilePath, `${staticDirAbsolutePath}/database/src/ts/main.ts`],
			plugins: [new MonacoWebpackPlugin()],
		}),
	]
}

export default [
	generateConfig('constructor_telegram_bots/static/default/dist', 'default'),
	generateConfig('home/static/home/index/dist', 'index.home', {
		entry: [...baseConfig.entry as string[], `${__dirname}/home/static/home/index/src/css/main.css`],
	}),
	generateConfig('team/static/team/index/dist', 'index.team', {
		entry: [...baseConfig.entry as string[], `${__dirname}/team/static/team/index/src/css/main.css`],
	}),
	generateConfig('personal_cabinet/static/personal_cabinet/index/dist', 'index.personal-cabinet', {
		entry: [...baseConfig.entry as string[], `${__dirname}/personal_cabinet/static/personal_cabinet/index/src/ts/main.tsx`],
	}),
	...TelegramBotMenu.configs,
]