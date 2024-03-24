import { createContext } from 'react';

import { APIResponse } from 'services/api/telegram_bots/types';

export interface VariablesContextProps {
	variables: APIResponse.VariablesAPI.Get.Pagination['results'];
	updateVariables: (limit?: number, offset?: number) => Promise<void>;
}

const VariablesContext = createContext<VariablesContextProps | undefined>(undefined);

export default VariablesContext;