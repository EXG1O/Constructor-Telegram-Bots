WEBPACK_CONFIGS=(
	./constructor_telegram_bots/static/global/webpack.config.js
)

for WEBPACK_CONFIG in $WEBPACK_CONFIGS; do
	webpack --mode=production -c $WEBPACK_CONFIG
done