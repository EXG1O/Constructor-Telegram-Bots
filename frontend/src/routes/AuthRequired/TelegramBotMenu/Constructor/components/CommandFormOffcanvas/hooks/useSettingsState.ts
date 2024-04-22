import { Dispatch, SetStateAction, useState } from 'react';

import { Data, defaultData } from '../components/SettingsBlock';

function useSettingsState(initialData: Data = defaultData): [Data, Dispatch<SetStateAction<Data>>] {
	return useState<Data>(initialData);
}

export default useSettingsState;