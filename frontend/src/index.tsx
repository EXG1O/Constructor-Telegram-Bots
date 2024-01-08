import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.min.css';

import React from 'react';
import { createRoot } from 'react-dom/client';
import { createBrowserRouter, RouterProvider, Params, redirect } from 'react-router-dom';

import { UserAPI } from 'services/api/users/main';

const router = createBrowserRouter([
	{
		id: 'root',
		path: '/',
		async lazy() {
			const module = await import('./routes/Root');

			return {
				Component: module.default,
				loader: module.loader,
			};
		},
		shouldRevalidate: () => true,
		children: [
			{
				async lazy() {
					const module = await import('./routes/ErrorBoundary');

					return { ErrorBoundary: module.default };
				},
				children: [
					{
						id: 'home',
						index: true,
						async lazy() {
							const module = await import('./routes/Home');

							return {
								Component: module.default,
								loader: module.loader,
							}
						},
					},
					{
						id: 'team',
						path: 'team/',
						async lazy() {
							const module = await import('./routes/Team');

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
								id: 'donation-index',
								index: true,
								async lazy() {
									const module = await import('./routes/Donation/Index');

									return {
										Component: module.default,
										loader: module.loader,
									}
								},
							},
							{
								path: 'completed/',
								async lazy() {
									const module = await import('./routes/Donation/Completed');

									return { Component: module.default };
								},
							},
						],
					},
					{
						id: 'instruction',
						path: 'instruction/',
						async lazy() {
							const module = await import('./routes/Instruction');

							return {
								Component: module.default,
								loader: module.loader,
							}
						},
					},
					{
						async lazy() {
							const module = await import('./routes/AuthRequired/Root');

							return { Component: module.default };
						},
						children: [
							{
								path: 'personal-cabinet/',
								async lazy() {
									const module = await import('./routes/AuthRequired/PersonalCabinet');

									return { Component: module.default };
								},
							},
							{
								path: 'telegram-bot-menu/:telegramBotID/',
								async lazy() {
									const module = await import('./routes/AuthRequired/TelegramBotMenu/Root');

									return { Component: module.default };
								},
								children: [
									{
										index: true,
										async lazy() {
											const module = await import('./routes/AuthRequired/TelegramBotMenu/Index');

											return { Component: module.default };
										},
									},
									{
										path: 'variables/',
										async lazy() {
											const module = await import('./routes/AuthRequired/TelegramBotMenu/Variables');

											return { Component: module.default };
										},
									},
									{
										path: 'users/',
										async lazy() {
											const module = await import('./routes/AuthRequired/TelegramBotMenu/Users');

											return { Component: module.default };
										},
									},
									{
										path: 'constructor/',
										async lazy() {
											const module = await import('./routes/AuthRequired/TelegramBotMenu/Constructor');

											return { Component: module.default };
										},
									},
								],
							},
						],
					},
				],
			},
		],
	},
	{
		path: '/login/:userID/:confirmCode/',
		loader: async ({ params }: { params: Params<'userID' | 'confirmCode'> }): Promise<Response> => {
			if (params.userID !== undefined && params.confirmCode !== undefined) {
				const response = await UserAPI.login({
					user_id: Number.parseInt(params.userID),
					confirm_code: params.confirmCode,
				});

				if (response.ok) {
					return redirect('/personal-cabinet/');
				}
			}

			return redirect('/');
		},
	},
]);

createRoot(document.querySelector<HTMLDivElement>('#root')!).render(<RouterProvider router={router} />);