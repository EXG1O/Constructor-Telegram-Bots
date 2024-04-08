import { createContext } from 'react';

import { User } from 'services/api/telegram_bots/types';

interface Filter {
	search: string;
}

export interface UsersContextProps {
	users: User[];
	filter: Filter;
	updateUsers: (limit?: number, offset?: number, search?: string) => Promise<void>;
}

const UsersContext = createContext<UsersContextProps | undefined>(undefined);

export default UsersContext;