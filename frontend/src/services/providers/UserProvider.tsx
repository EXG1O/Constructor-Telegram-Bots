import React, { ReactNode, useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import Cookies from 'js-cookie';

import Spinner from 'react-bootstrap/Spinner';

import UserContext, { UserContextProps } from 'services/contexts/UserContext';

import { UserAPI } from 'services/api/users/main';

export interface UserProviderProps {
	children: ReactNode
}

function UserProvider({ children }: UserProviderProps): ReactNode {
	let location = useLocation();

	const [user, setUser] = useState<UserContextProps | undefined>(undefined);

	useEffect(() => {
		const authToken = Cookies.get('auth-token');

		async function getUser(): Promise<void> {
			const response = await UserAPI.get();

			if (response.ok) {
				setUser(response.json);
			} else {
				Cookies.remove('auth-token');

				setUser(null);
			}
		}

		if (authToken !== undefined) {
			getUser();
		} else {
			setUser(null);
		}
	}, [location]);

	return user === undefined ? (
		<Spinner
			animation='border'
			className='m-auto'
			style={{
				width: '4rem',
				height: '4rem',
				borderWidth: '0.5rem',
			}}
		/>
	) : (
		<UserContext.Provider value={user}>
			{children}
		</UserContext.Provider>
	);
}

export default UserProvider;