import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.min.css';

import React, { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { createBrowserRouter, RouterProvider, Params, redirect } from 'react-router-dom';

import { UserAPI } from 'services/api/users/main';

const router = createBrowserRouter([
	{
		path: '/',
		async lazy() {
			const module = await import('./routes/root/App');

			return { Component: module.default };
		},
		children: [
			{
				index: true,
				async lazy() {
					const module = await import('./routes/home/App');

					return {
						Component: module.default,
						loader: module.loader,
					}
				},
			},
			{
				path: 'team/',
				async lazy() {
					const module = await import('./routes/team/App');

					return {
						Component: module.default,
						loader: module.loader,
					}
				},
			},
			{
				path: 'donation/',
				children: [
					{
						index: true,
						async lazy() {
							const module = await import('./routes/donation/index/App');

							return {
								Component: module.default,
								loader: module.loader,
							}
						},
					},
					{
						path: 'completed/',
						async lazy() {
							const module = await import('./routes/donation/completed/App');

							return { Component: module.default };
						},
					},
				],
			},
			{
				path: 'personal-cabinet/',
				async lazy() {
					const module = await import('./routes/personal_cabinet/App');

					return {
						Component: module.default,
						loader: module.loader,
					}
				},
			},
			{
				path: 'telegram-bot-menu/:telegramBotID/',
				async lazy() {
					const module = await import('./routes/telegram_bot_menu/root/App');

					return { Component: module.default };
				},
				children: [
					{
						index: true,
						async lazy() {
							const module = await import('./routes/telegram_bot_menu/index/App');

							return { Component: module.default };
						},
					},
					{
						path: 'variables/',
						async lazy() {
							const module = await import('./routes/telegram_bot_menu/variables/App');

							return { Component: module.default };
						},
					},
					{
						path: 'users/',
						async lazy() {
							const module = await import('./routes/telegram_bot_menu/users/App');

							return { Component: module.default };
						},
					},
					{
						path: 'database/',
						async lazy() {
							const module = await import('./routes/telegram_bot_menu/database/App');

							return { Component: module.default };
						},
					},
				],
			},
		],
	},
	{
		path: '/login/:userID/:confirmCode/',
		loader: async ({ params }: { params: Params<'userID' | 'confirmCode'> }): Promise<Response> => {
			if (params.userID === undefined || params.confirmCode === undefined) {
				throw new Error('');
			}

			const response = await UserAPI.login({
				user_id: Number.parseInt(params.userID),
				confirm_code: params.confirmCode,
			});

			if (response.ok) {
				return redirect('/personal-cabinet/');
			}

			return redirect('/');
		},
	},
]);

createRoot(document.querySelector<HTMLDivElement>('#root')!).render(
	<StrictMode>
		<RouterProvider router={router} />
	</StrictMode>
);