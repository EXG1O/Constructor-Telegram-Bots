import { createContext } from 'react';

import { APIResponse } from 'services/api/telegram_bots/types';

export interface UsersContextProps {
	users: APIResponse.UsersAPI.Get.Pagination['results'];
	updateUsers: (limit?: number, offset?: number, search?: string) => Promise<void>;
}

const UsersContext = createContext<UsersContextProps | undefined>(undefined);

export default UsersContext;