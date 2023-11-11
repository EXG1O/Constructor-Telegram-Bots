module.exports = {
	module: {
		rules: [
			{
				test: /\.(ts|tsx)$/,
				loader: "ts-loader",
			},
		],
	},
	externals: {
		bootstrap: 'bootstrap',
	},
	resolve: {
		extensions: ['.tsx', '.ts', '.js'],
	},
};