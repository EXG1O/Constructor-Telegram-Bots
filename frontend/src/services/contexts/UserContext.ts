import { createContext } from 'react';

import { User } from 'services/api/users/types';

export type UserContextProps = User | null;

const UserContext = createContext<UserContextProps | undefined>(undefined);

export default UserContext;