import { useContext } from 'react';

import UserContext, { UserContextProps } from 'services/contexts/UserContext';

function useUser(): UserContextProps {
	const user = useContext<UserContextProps | undefined>(UserContext);

	if (user === undefined) {
		throw new Error('useUser must be used with a UserProvider!');
	}

	return user;
}

export default useUser;