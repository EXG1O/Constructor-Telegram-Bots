import { ReactNode, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

import useUser from 'services/hooks/useUser';

export interface AuthRequiredProviderProps {
	children: ReactNode
}

function AuthRequiredProvider({ children }: AuthRequiredProviderProps): ReactNode {
	const location = useLocation();
	const navigation = useNavigate();

	const user = useUser();

	useEffect(() => {
		if (!user) {
			navigation('/');
		}
	}, [location]);

	return children;
}

export default AuthRequiredProvider;